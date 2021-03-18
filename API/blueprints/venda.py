import datetime

from flask import Blueprint, jsonify, Response
from flask_restplus import Api, Resource, fields

from API.models import Cliente, Proprietario, Vendedor, Imovel, db, Venda, Financiamento, Banco

venda_blueprint = Blueprint('venda_bp', __name__, url_prefix='/api/ns5')
api = Api(venda_blueprint, doc='/docs/venda',
          version="1.0",
          title="Venda Admin",
          description="Gerencia os dados referentes às vendas")

name_space = api.namespace("venda", descrption="Compras API")

venda_fields = api.model('Venda', {
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
    "tipo_venda": fields.String(enum=['à vista', 'financiamento'], required=True, description="Tipo da compra",
                                 help="Tipo da venda não pode ficar em branco"),
})

financiamento_fields = api.model('Financiamento', {
    "id_venda": fields.Integer(required=True, description="ID da compra",
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
class VendaCollection(Resource):
    @name_space.expect(venda_fields, validate=True)
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

                antigo_proprietario = Proprietario.query.filter_by(id_pessoa=data["id_proprietario"]).first()
                atual_cliente = Cliente.query.filter_by(id_pessoa=data["id_cliente"]).first()
                atual_vendedor = Vendedor.query.filter_by(id_pessoa=data["id_vendedor"]).first()

                new_data = {"id_imovel": data["id_imovel"], "id_proprietario": antigo_proprietario.id_proprietario,
                            "id_cliente": atual_cliente.id_cliente, "id_vendedor": atual_vendedor.id_vendedor,
                            "valor": data["valor"], "tipo_venda":data["tipo_venda"]}

                venda = Venda(**new_data)
                db.session.add(venda)
                db.session.commit()

                cliente = Cliente.query.filter_by(id_pessoa=data["id_cliente"]).first()
                novo_proprietario = Proprietario(id_pessoa=cliente.id_pessoa)
                db.session.add(novo_proprietario)
                db.session.commit()

                imovel = Imovel.query.filter_by(id_imovel=data["id_imovel"]).first()
                imovel.id_proprietario = novo_proprietario.id_proprietario
                imovel.data_posse_proprietario = datetime.date.today()
                db.session.commit()

                return jsonify(venda)

        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Could not save information", statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not save information", statusCode="400")

    @name_space.doc(responses={200: 'OK'})
    def get(self):
        vendas = Venda.query.order_by(Venda.id_venda).all()

        vendas_com_ids = []
        for venda in vendas:
            proprietario = Proprietario.query.filter_by(id_proprietario=venda.id_proprietario).first()
            cliente = Cliente.query.filter_by(id_cliente=venda.id_cliente).first()
            vendedor = Vendedor.query.filter_by(id_vendedor=venda.id_vendedor).first()
            venda_com_id = dict(
                {"id_imovel":venda.id_imovel ,"id_venda": venda.id_venda, "valor": venda.valor, "tipo_venda": venda.tipo_venda})
            venda_com_id["id_proprietario"] = proprietario.id_pessoa
            venda_com_id["id_cliente"] = cliente.id_pessoa
            venda_com_id["id_vendedor"] = vendedor.id_pessoa
            vendas_com_ids.append(venda_com_id)
        return jsonify(vendas_com_ids)


@name_space.route('/<int:id>', methods=['GET', 'DELETE'])
class VendaEntity(Resource):
    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def get(self, id):
        venda = Venda.query.filter_by(id_compra=id).first()
        if venda:
            proprietario = Proprietario.query.filter_by(id_proprietario=venda.id_proprietario).first()
            cliente = Cliente.query.filter_by(id_cliente=venda.id_cliente).first()
            vendedor = Vendedor.query.filter_by(id_vendedor=venda.id_vendedor).first()
            venda_com_id = dict(
                {"id_venda": venda.id_venda, "valor": venda.valor, "tipo_venda": venda.tipo_venda})
            venda_com_id["id_proprietario"] = proprietario.id_pessoa
            venda_com_id["id_cliente"] = cliente.id_pessoa
            venda_com_id["id_vendedor"] = vendedor.id_pessoa
            return jsonify(venda_com_id)
        return Response(status=404)

    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def delete(self, id):
        venda = Venda.query.filter_by(id_compra=id).first()
        if venda:
            db.session.delete(venda)
            db.session.commit()
            return Response(status=200)
        return Response(status=404)


@name_space.route('/financiamento', methods=['POST', 'GET'])
class VendaFinanciamentoCollection(Resource):
    @name_space.expect(financiamento_fields, validate=True)
    @name_space.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: "Not Found"})
    def post(self):
        data = name_space.payload
        try:
            compra = Venda.query.filter_by(id_compra=data.get("id_compra")).first()
            banco = Banco.query.filter_by(id_banco=data.get("id_banco")).first()
            if compra is not None and banco is not None:
                if compra.tipo_venda == "à vista":
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
