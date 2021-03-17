from flask import Blueprint, jsonify, Response
from flask_restplus import Api, Resource, fields

from API.models import Proprietario, Imovel, db

imovel_blueprint = Blueprint('imovel_bp', __name__, url_prefix="/api/ns4")
api = Api(imovel_blueprint, doc='/docs/imovel',
          version="1.0",
          title="Imovel Admin",
          description="Gerencia os dados referentes aos imóveis")

name_space = api.namespace("imovel", descrption="Imóveis API")

imovel_fields = api.model('Imovel', {
    "id_proprietario": fields.Integer(required=True, description="ID do proprietário",
                                      help="Proprietário deve ter sido previamente cadastrado."),
    "tipo_imovel": fields.String(enum=['apartamento', 'casa', 'kitnet'], required=True, description="Tipo do imóvel",
                                 help="Tipo do imóvel não pode ficar em branco"),
    "rua": fields.String(max_length=70, required=True,
                         description="Rua em que o imóvel se encontra", help="Rua não pode ficar em branco."),
    "numero": fields.Integer(required=True, description="Número do imóvel",
                             help="Número do imóvel não pode ficar em branco."),
    "andar": fields.Integer(required=False, description="Andar do imóvel, caso tenha"),
    "bloco": fields.String(max_length=25, required=False, description="Bloco do imóvel, caso tenha"),
    "cep": fields.String(max_length=8, min_length=8, required=True,
                         description="CEP da rua/cidade", help="CEP deve conter 8 dígitos."),
    "cidade": fields.String(max_length=50, required=True,
                            description="Cidade em que o imóvel se encontra", help="Cidade não pode ficar em branco."),
    "uf": fields.String(max_length=25, required=True,
                        description="UF da cidade", help="UF deve conter 2 letras."),
    "data_posse_proprietario": fields.Date(required=True,
                                           description="Data em que o proprietário obteve a posse do imóvel",
                                           help="Data de posse no padrão dd/mm/yyyy."),
})

imovel_dto = api.model('ImovelDTO', {
    "numero": fields.Integer(required=False, description="Número do imóvel")})


@name_space.route('/', methods=['POST', 'GET'])
class ImovelColection(Resource):
    @name_space.expect(imovel_fields, validate=True)
    @name_space.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: 'Not Found'})
    def post(self):
        data = name_space.payload
        try:
            if Proprietario.query.filter_by(id_proprietario=data["id_proprietario"]).first() is not None:
                imovel = Imovel(**data)
                db.session.add(imovel)
                db.session.commit()
                return jsonify(imovel)
            else:
                return Response(status=404)

        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Could not save information", statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not save information", statusCode="400")

    @name_space.doc(responses={200: 'OK'})
    def get(self):
        imoveis = Imovel.query.order_by(Imovel.id_imovel).all()

        return jsonify([imoveis])


@name_space.route('/<int:id>', methods=['POST', 'GET', 'PUT'])
class ImovelEntity(Resource):
    @name_space.expect(imovel_dto, validate=True)
    @name_space.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: "Not Found"})
    def post(self, id):
        data = name_space.payload
        try:
            if Imovel.query.filter_by(id_imovel=id).first() is not None:
                imovel = Imovel.query.filter_by(id_imovel=id).first()
                if data.get("numero") is not None:
                    imovel.numero = data["numero"]
                db.session.commit()
                return jsonify(imovel)
            return Response(status=404)

        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Could not save information", statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not save information", statusCode="400")

    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def get(self, id):
        imovel = Imovel.query.filter_by(id_imovel=id).first()
        if imovel:
            return jsonify(imovel)
        return Response(status=404)

    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def put(self, id):
        imovel = Imovel.query.filter_by(id_imovel=id).first()
        if imovel:
            db.session.delete(imovel)
            db.session.commit()
            return Response(status=200)
        return Response(status=404)
