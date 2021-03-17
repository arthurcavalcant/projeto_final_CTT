from flask import Blueprint, jsonify, Response
from flask_restplus import Api, Resource, fields

from API.models import db, Banco

banco_blueprint = Blueprint('banco_bp', __name__, url_prefix="api/ns6")
api = Api(banco_blueprint, doc='/docs/banco',
          version="1.0",
          title="Banco Admin",
          description="Gerencia os dados referentes aos bancos")

name_space = api.namespace("banco", descrption="Bancos API")


banco_fields = api.model('Banco', {
    'nome': fields.String(required=True, description="Nome do banco", help="Nome não pode ficar em branco."),
    'codigo_banco': fields.Integer(required=True, description="Código do banco", help="Código não pode ficar nulo.")
})

banco_dto = api.model('BancoDTO', {
        'nome': fields.String(required=True, description="Nome do banco", help="Nome não pode ficar em branco."),
})


@name_space.route('/', methods=['POST', 'GET'])
class BancoCollection(Resource):
    @name_space.expect(banco_fields, validate=True)
    @name_space.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    def post(self):
        data = name_space.payload
        try:
            if Banco.query.filter_by(codigo_banco=data["codigo_banco"]).first() is None:
                banco = Banco(**data)
                db.session.add(banco)
                db.session.commit()
                return jsonify(banco)
            else:
                return Response(status=400)

        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Could not retrieve information", statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not retrieve information", statusCode="400")

    @name_space.doc(responses={200: 'OK'})
    def get(self):
        bancos = Banco.query.order_by(Banco.id_banco).all()

        return jsonify(bancos)


@name_space.route('/<int:id>', methods=['PUT', 'GET', 'DElETE'])
class BancoEntity(Resource):
    @name_space.expect(banco_dto, validate=True)
    @name_space.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: "Not Found"})
    def put(self, id):
        data = name_space.payload
        try:
            if Banco.query.filter_by(id_pessoa=id).first() is not None:
                banco = Banco.query.filter_by(id_banco=id).first()
                banco.nome = data["nome"]
                db.session.commit()
                return jsonify(banco)
            return Response(status=404)

        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Could not save information", statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not save information", statusCode="400")

    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def get(self, id):
        banco = Banco.query.filter_by(id_banco=id).first()
        if banco:
            return jsonify(banco)
        return Response(status=404)

    @name_space.doc(responses={200: 'OK', 404: 'Not Found'})
    def delete(self, id):
        banco = Banco.query.filter_by(id_banco=id).first()
        if banco:
            db.session.delete(banco)
            db.session.commit()
            return Response(status=200)
        return Response(status=404)
