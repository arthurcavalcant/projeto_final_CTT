from flask import Blueprint, request, flash, jsonify
import datetime
from models import Cliente, Pessoa, db
from flask_restplus import Api, Resource

compra_blueprint = Blueprint('compra_bp', __name__)
api = Api(compra_blueprint, doc='/api/docs/compra')

name_space = api.namespace("compra", descrption="Compras API documentation")


@name_space.route('/new/', methods=['POST'])
class New(Resource):
    def post(self):
        if request.method == 'POST':
            data = request.get_json()
            pessoa = Pessoa(**data)
            pessoa.data_nascimento = datetime.datetime.strptime(data["data_nascimento"], '%d/%m/%Y')
            db.session.add(pessoa)
            db.session.commit()
            flash('Record was successfully added')
            return pessoa
