from flask import Blueprint, jsonify, Response
from flask_restplus import Api, Resource, fields

from API.models import Cliente, Pessoa, db

cliente_blueprint = Blueprint('cliente_bp', __name__, url_prefix="/api/ns1")
api = Api(cliente_blueprint, doc='/docs/cliente', version="1.0",
          title="Cliente Admin",
          description="Gerencia os dados referentes aos clientes")

name_space = api.namespace("cliente", description="Cliente API")

cliente_fields = api.model('Cliente', {
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

cliente_dto = api.model('ClienteDTO', {
    'nome': fields.String(description="Nome de uma pessoa"),
    'estado_civil_pessoa': fields.String(enum=['solteira', 'casada', 'viúva', 'divorciada', 'união estável'],
                                         description="Estado civil de uma pessoa"),
    'profissao': fields.String(description="Profissão de uma pessoa")})


@name_space.route('/', methods=['POST', 'GET'])
class ClienteCollection(Resource):
    @name_space.expect(cliente_fields, validate=True)
    @name_space.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    def post(self):
        data = name_space.payload
        try:
            if Pessoa.query.filter_by(cpf=data["cpf"]).first() is None \
                    and Pessoa.query.filter_by(rg=data["rg"]).first() is None:
                pessoa = Pessoa(**data)
                db.session.add(pessoa)
                db.session.commit()
                cliente = Cliente(id_pessoa=pessoa.id_pessoa)
                db.session.add(cliente)
                db.session.commit()
                return jsonify(pessoa)
            elif Cliente.query.filter_by(id_pessoa=Pessoa.query.filter_by(
                    cpf=data["cpf"]).first().id_pessoa) is not None or Cliente.query.filter_by(
                id_pessoa=Pessoa.query.filter_by(rg=data["rg"]).first().id_pessoa) is not None:
                name_space.abort(400, status="CPF ou RG já cadastrado(s)", statusCode="400")

            elif Pessoa.query.filter_by(cpf=data["cpf"]).first() == Pessoa.query.filter_by(rg=data["rg"]).first():
                pessoa = Pessoa.query.filter_by(cpf=data["cpf"]).first()
                cliente = Cliente(id_pessoa=pessoa.id_pessoa)
                db.session.add(cliente)
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
        clientes = Cliente.query.order_by(Cliente.id_pessoa).all()
        pessoas = []
        for cliente in clientes:
            pessoa = Pessoa.query.filter_by(id_pessoa=cliente.id_pessoa).first()
            pessoas.append(pessoa)

        return jsonify(pessoas)


@name_space.route('/<int:id>', methods=['PUT', 'GET', 'DELETE'])
class ClienteEntity(Resource):
    @name_space.expect(cliente_dto, validate=True)
    @name_space.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: "Not Found"})
    def put(self, id):
        data = name_space.payload
        try:
            if Cliente.query.filter_by(id_pessoa=id).first() is not None:
                pessoa = Pessoa.query.get_or_404(id)
                print("a")
                if data.get("nome") is not None:
                    pessoa.nome = data["nome"]
                if data.get("estado_civil_pessoa") is not None:
                    pessoa.estado_civil_pessoa = data["estado_civil_pessoa"]
                if data.get("profissao") is not None:
                    pessoa.profissao = data["profissao"]
                db.session.add(pessoa)
                db.session.commit()
                return jsonify(pessoa)
            return Response(status=404)

        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Could not save information", statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not save information", statusCode="400")

    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def get(self, id):
        cliente = Cliente.query.filter_by(id_pessoa=id).first()
        if cliente:
            pessoa = Pessoa.query.filter_by(id_pessoa=id).first()
            return jsonify(pessoa)
        return Response(status=404)

    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def delete(self, id):
        cliente = Cliente.query.filter_by(id_pessoa=id).first()
        if cliente:
            pessoa = Pessoa.query.filter_by(id_pessoa=id).first()
            db.session.delete(pessoa)
            db.session.commit()
            return Response(status=200)
        return Response(status=404)
