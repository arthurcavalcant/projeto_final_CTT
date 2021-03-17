import datetime

from flask import Blueprint, jsonify, Response
from flask_restplus import Api, Resource, fields

from API.models import Cliente, Proprietario, Vendedor, Imovel, db, Compra, Financiamento, Banco

compra_blueprint = Blueprint('compra_bp', __name__, url_prefix='/api/ns5')
api = Api(compra_blueprint, doc='/docs/compra',
          version="1.0",
          title="Compra Admin",
          description="Gerencia os dados referentes às compras")

name_space = api.namespace("compra", descrption="Compras API")

imovel_fields = api.model('Compra', {
    "id_imovel": fields.Integer(required=True, description="ID do imóvel",
                                help="Imóvel deve ter sido previamente cadastrado."),
    "id_proprietario": fields.Integer(required=True, description="ID do proprietário",
                                      help="Proprietário deve ter sido previamente cadastrado."),
    "id_cliente": fields.Integer(required=True, description="ID do cliente",
                                 help="Cliente deve ter sido previamente cadastrado."),
    "id_vendedor": fields.Integer(required=True, description="ID do vendedor",
                                  help="Vendedor deve ter sido previamente cadastrado."),
    "valor": fields.Float(required=True, description="Valor da compra", min=0.0,
                          help="Valor da compra não pode ser negativo."),
    "tipo_compra": fields.String(enum=['à vista', 'financiamento'], required=True, description="Tipo da compra",
                                 help="Tipo da compra não pode ficar em branco"),
})

financiamento_fields = api.model('Finaciamento', {
    "id_compra": fields.Integer(required=True, description="ID da compra",
                                help="Compra deve ter sido previamente registrada."),
    "id_banco": fields.Integer(required=True, description="ID do banco",
                               help="Banco deve ter sido previamente cadastrado."),
    "parcelas": fields.Integer(required=True, description="Número de parcelas do financiamento", min=1,
                               help="Número de parcelas deve ser igual ou superior a 1."),
    "entrada_porcentagem": fields.Integer(required=True, description="Entrada do financiamento (em porcentagem)", min=0,
                                          help="Entrada do financiamento deve ser igual ou maior igual a 0 (em "
                                               "porcentagem).")
})


@name_space.route('/', methods=['POST', 'GET'])
class CompraCollection(Resource):
    @name_space.expect(imovel_fields, validate=True)
    @name_space.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: 'Not Found'})
    def post(self):
        data = name_space.payload
        try:
            if Proprietario.query.filter_by(id_pessoa=data["id_proprietario"]).first() is None or \
                    Cliente.query.filter_by(id_pessoa=data["id_cliente"]).first() is None or \
                    Vendedor.query.filter_by(id_pessoa=data["id_vendedor"]).first() is None or \
                    Imovel.query.filter_by(id_imovel=data["id_imovel"]).first() is None:
                return Response(status=404)
            else:
                compra = Compra(**data)
                db.session.add(compra)
                db.session.commit()

                cliente = Cliente.query.filter_by(id_pessoa=data["id_cliente"]).first()
                novo_proprietario = Proprietario(id_pessoa=cliente.id_pessoa)
                db.session.add(novo_proprietario)
                db.session.commit()

                imovel = Imovel.query.filter_by(id_imovel=data["id_imovel"]).first()
                imovel.id_proprietario = novo_proprietario.id_proprietario
                imovel.data_posse_proprietario = datetime.date.today()
                db.session.commit()

                return jsonify(compra)

        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Could not save information", statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not save information", statusCode="400")

    @name_space.doc(responses={200: 'OK'})
    def get(self):
        compras = Compra.query.order_by(Compra.id_compra).all()

        return jsonify([compras])


@name_space.route('/<int:id>', methods=['GET', 'DELETE'])
class CompraEntity(Resource):
    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def get(self, id):
        """Returns list of blog categories."""
        compra = Compra.query.filter_by(id_compra=id).first()
        if compra:
            return jsonify(compra)
        return Response(status=404)

    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def delete(self, id):
        compra = Compra.query.filter_by(id_compra=id).first()
        if compra:
            db.session.delete(compra)
            db.session.commit()
            return Response(status=200)
        return Response(status=404)


@name_space.route('/financiamento', methods=['POST', 'GET'])
class CompraFinanciamentoCollection(Resource):
    @name_space.expect(financiamento_fields, validate=True)
    @name_space.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: "Not Found"})
    def post(self):
        data = name_space.payload
        try:
            compra = Compra.query.filter_by(id_compra=data.get("id_compra")).first()
            banco = Banco.query.filter_by(id_banco=data.get("id_banco")).first()
            if compra is not None and banco is not None:
                if compra.tipo_compra == "à vista":
                    return Response(status=400)

                financiamento = Financiamento(**data)
                db.session.add(financiamento)
                db.session.commit()
                return jsonify(financiamento)
            return Response(status=404)

        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Could not save information", statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not save information", statusCode="400")

    @name_space.doc(responses={200: 'OK'})
    def get(self):
        financiamentos = Financiamento.query.order_by(Financiamento.id_financiamento).all()

        return jsonify([financiamentos])


@name_space.route('/<int:id>/financiamento', methods=['GET', 'DELETE'])
class CompraFinanciamentoEntity(Resource):
    @name_space.expect(financiamento_fields, validate=True)
    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def get(self, id):
        financiamento = Financiamento.query.filter_by(id_compra=id).first()
        if financiamento:
            return jsonify(financiamento)
        return Response(status=404)

    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def delete(self, id):
        financiamento = Financiamento.query.filter_by(id_compra=id).first()
        if financiamento:
            db.session.delete(financiamento)
            db.session.commit()
            return Response(status=200)
        return Response(status=404)
