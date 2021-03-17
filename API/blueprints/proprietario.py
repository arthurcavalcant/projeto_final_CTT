from flask import Blueprint, jsonify, Response
from flask_restplus import Api, Resource, fields

from API.models import Proprietario, Pessoa, db

proprietario_blueprint = Blueprint('proprietario_bp', __name__, url_prefix="/api/ns2")
api = Api(proprietario_blueprint, doc='/docs/proprietario', version="1.0",
          title="Proprietario Admin",
          description="Gerencia os dados referentes aos proprietários")

name_space = api.namespace("proprietario", description="Proprietário API")


proprietario_fields = api.model('Proprietario', {
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
                               help="Profissão não pode ficar em branco")
})
proprietario_dto = api.model('ProprietarioDTO', {
    'nome': fields.String(description="Nome de uma pessoa"),
    'estado_civil_pessoa': fields.String(enum=['solteira', 'casada', 'viúva', 'divorciada', 'união estável'],
                                         description="Estado civil de uma pessoa"),
    'profissao': fields.String(description="Profissão de uma pessoa")})


@name_space.route('/', methods=['POST', 'GET'])
class ProprietarioCollection(Resource):
    @name_space.expect(proprietario_fields, validate=True)
    @name_space.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    def post(self):
        data = name_space.payload
        try:
            if Pessoa.query.filter_by(cpf=data["cpf"]).first() is None \
                    and Pessoa.query.filter_by(rg=data["rg"]).first() is None:
                pessoa = Pessoa(**data)
                db.session.add(pessoa)
                db.session.commit()
                proprietario = Proprietario(id_pessoa=pessoa.id_pessoa)
                db.session.add(proprietario)
                db.session.commit()
                return jsonify(pessoa)
            elif Proprietario.query.filter_by(id_pessoa=Pessoa.query.filter_by(
                    cpf=data["cpf"]).first().id_pessoa) is not None or Proprietario.query.filter_by(
                id_pessoa=Pessoa.query.filter_by(rg=data["rg"]).first().id_pessoa) is not None:
                name_space.abort(400, status="CPF ou RG já cadastrado(s)", statusCode="400")

            elif Pessoa.query.filter_by(cpf=data["cpf"]).first() == Pessoa.query.filter_by(rg=data["rg"]).first():
                pessoa = Pessoa.query.filter_by(cpf=data["cpf"]).first()
                proprietario = Proprietario(id_pessoa=pessoa.id_pessoa)
                db.session.add(proprietario)
                db.session.commit()
                return jsonify(pessoa)
            else:
                return Response(status=400)

        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Could not save information", statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not save information", statusCode="400")

    @name_space.doc(responses={200: 'OK'})
    def get(self):
        proprietarios = Proprietario.query.order_by(Proprietario.id_pessoa).all()
        pessoas = []
        for proprietario in proprietarios:
            pessoa = Pessoa.query.filter_by(id_pessoa=proprietario.id_pessoa).first()
            pessoas.append(pessoa)

        return jsonify(pessoas)


@name_space.route('/<int:id>', methods=['PUT', 'GET', 'DELETE'])
class ProprietarioEntity(Resource):
    @name_space.expect(proprietario_dto, validate=True)
    @name_space.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: "Not Found"})
    def put(self, id):
        data = name_space.payload
        try:
            if Proprietario.query.filter_by(id_pessoa=id).first() is not None:
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
        proprietario = Proprietario.query.filter_by(id_pessoa=id).first()
        if proprietario:
            pessoa = Pessoa.query.filter_by(id_pessoa=id).first()
            return jsonify(pessoa)
        return Response(status=404)

    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def delete(self, id):
        proprietario = Proprietario.query.filter_by(id_pessoa=id).first()
        if proprietario:
            db.session.delete(proprietario)
            db.session.commit()
            return Response(status=200)
        return Response(status=404)
