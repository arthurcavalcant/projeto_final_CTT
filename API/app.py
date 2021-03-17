from flask import Flask
from flask_cors import CORS

from API.blueprints import banco
from models import db
from configparser import ConfigParser
from blueprints import cliente, compra, proprietario, vendedor, imovel

app = Flask(__name__)

CORS(app)

config = ConfigParser()
config.read('settings.ini')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config.get("DATABASE", "username")}:' \
                                        f'{config.get("DATABASE", "password")}@{config.get("DATABASE", "host")}' \
                                        f'/{config.get("DATABASE", "db_name")}'

app.config['SECRET_KEY'] = config.get("APP_KEY", "key")

app.register_blueprint(cliente.cliente_blueprint)
app.register_blueprint(proprietario.proprietario_blueprint)
app.register_blueprint(imovel.imovel_blueprint)
app.register_blueprint(vendedor.vendedor_blueprint)
app.register_blueprint(compra.compra_blueprint)
app.register_blueprint(banco.banco_blueprint)


with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
