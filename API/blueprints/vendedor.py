from flask import Blueprint, jsonify, Response
from flask_restplus import Api, Resource, fields

from API.models import Vendedor, Pessoa, db

vendedor_blueprint = Blueprint('vendedor_bp', __name__, url_prefix="/api/ns3")
api = Api(vendedor_blueprint, doc='/docs/vendedor', version="1.0",
          title="Vendedor Admin",
          description="Gerencia os dados referentes aos vendedores")

name_space = api.namespace("vendedor", descrption="Vendedores API")


vendedor_fields = api.model('Vendedor', {
    'nome': fields.String(required=True, description="Nome de uma pessoa", help="Nome não pode ficar em branco."),
    'cpf': fields.String(max_length=11, min_length=11, required=True,
                         description="CPF de uma pessoa", help="CPF deve conter 11 dígitos."),
    'rg': fields.String(max_length=7, min_length=7, required=True,
                        description="RG de uma pessoa", help="RG deve conter 7 dígitos."),
    'data_nascimento': fields.Date(required=True,
                                   description="Data de nascimento de uma pessoa",
                                   help="Data de nascimento no padrão dd/mm/yyyy."),
    'estado_civil_pessoa': fields.String(enum=['solteira', 'casada', 'viúva', 'divorciada', 'união estável'],
                                         required=True, description="Estado civil de uma pessoa",
                                         help="Estado civil não pode ficar em branco"),
    'profissao': fields.String(required=True, description="Profissão de uma pessoa",
                               help="Profissão não pode ficar em branco", example="vendedor")
})

vendedor_dto = api.model('VendedorDTO', {
    'nome': fields.String(description="Nome de uma pessoa"),
    'estado_civil_pessoa': fields.String(enum=['solteira', 'casada', 'viúva', 'divorciada', 'união estável'],
                                         description="Estado civil de uma pessoa"),
    'profissao': fields.String(description="Profissão de uma pessoa")})


@name_space.route('/', methods=['POST', 'GET'])
class VendedorCollection(Resource):
    @name_space.expect(vendedor_fields, validate=True)
    @name_space.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    def post(self):
        data = name_space.payload
        try:
            if Pessoa.query.filter_by(cpf=data["cpf"]).first() is None \
                    and Pessoa.query.filter_by(rg=data["rg"]).first() is None:
                pessoa = Pessoa(**data)
                db.session.add(pessoa)
                db.session.commit()
                vendedor = Vendedor(id_pessoa=pessoa.id_pessoa)
                db.session.add(vendedor)
                db.session.commit()
                return jsonify(pessoa)
            elif Vendedor.query.filter_by(id_pessoa=Pessoa.query.filter_by(
                    cpf=data["cpf"]).first().id_pessoa) is not None or Vendedor.query.filter_by(
                id_pessoa=Pessoa.query.filter_by(rg=data["rg"]).first().id_pessoa) is not None:
                name_space.abort(400, status="CPF ou RG já cadastrado(s)", statusCode="400")

            elif Pessoa.query.filter_by(cpf=data["cpf"]).first() == Pessoa.query.filter_by(rg=data["rg"]).first():
                pessoa = Pessoa.query.filter_by(cpf=data["cpf"]).first()
                vendedor = Vendedor(id_pessoa=pessoa.id_pessoa)
                db.session.add(vendedor)
                db.session.commit()
                return jsonify(pessoa)
            else:
                return Response(status=400)

        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Could not retrieve information", statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not retrieve information", statusCode="400")

    @name_space.doc(responses={200: 'OK'})
    def get(self):
        vendedores = Vendedor.query.order_by(Vendedor.id_pessoa).all()
        pessoas = []
        for vendedor in vendedores:
            pessoa = Pessoa.query.filter_by(id_pessoa=vendedor.id_pessoa).first()
            pessoas.append(pessoa)

        return jsonify(pessoas)


@name_space.route('/<int:id>', methods=['PUT', 'GET', 'DELETE'])
class VendedorEntity(Resource):
    @name_space.expect(vendedor_dto, validate=True)
    @name_space.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: "Not Found"})
    def put(self, id):
        data = name_space.payload
        try:
            if Vendedor.query.filter_by(id_pessoa=id).first() is not None:
                pessoa = Pessoa.query.filter_by(id_pessoa=id).first()
                if data.get("nome") is not None:
                    pessoa.nome = data["nome"]
                if data.get("estado_civil_pessoa") is not None:
                    pessoa.estado_civil_pessoa = data["estado_civil_pessoa"]
                if data.get("profissao") is not None:
                    pessoa.profissao = data["profissao"]
                db.session.commit()
                return jsonify(pessoa)
            return Response(status=404)

        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Could not save information", statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not save information", statusCode="400")

    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def get(self, id):
        vendedor = Vendedor.query.filter_by(id_pessoa=id).first()
        if vendedor:
            pessoa = Pessoa.query.filter_by(id_pessoa=id).first()
            return jsonify(pessoa)
        return Response(status=404)

    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def delete(self, id):
        vendedor = Vendedor.query.filter_by(id_pessoa=id).first()
        if vendedor:
            db.session.delete(vendedor)
            db.session.commit()
            return Response(status=200)
        return Response(status=404)
