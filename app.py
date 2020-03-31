from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import Usuario
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
'''
A configuração abaixo é para não ficar exibindo um aviso para marcar a config a baixo como True ou False,
mas que fica sobrecarregando o app, porém ao marcar como False apenas o flask deixa de rastrear as modificação, mas o
sql alchemy permanece rastreando
'''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
app.config['SECRET_KEY'] = 'meu teste rest'
app.config['JWT_BLACKLIST_ENABLED'] = True
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def verifica_blacklist(token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return jsonify({"Mensagem": "Você já desconectou!!"}), 401  # unauthorized


@app.before_first_request
def cria_banco():
    banco.create_all()


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hotel/<string:id>')
api.add_resource(Hotel.Add, '/hotel/add')
api.add_resource(Usuario, '/usuario/<int:id>')
api.add_resource(Usuario.Add_Usuario, '/usuario/add')
api.add_resource(Usuario.Login, '/login')
api.add_resource(Usuario.Logout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import banco

    banco.init_app(app)
    app.run(debug=True)
