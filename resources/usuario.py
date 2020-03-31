from flask_restful import Resource, reqparse
from models.usuario_model import UsuarioModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp


class Usuario(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
    argumentos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")

    class Add_Usuario(Resource):
        def post(self):
            dados = Usuario.argumentos.parse_args()
            try:
                if UsuarioModel.find_by_login(dados['login']):
                    return {"Mensagem": f"O login {dados['login']} já exite!"}
                usuario = UsuarioModel(**dados)
                usuario.save()
            except:
                return {"message": "A internal error ocurred trying to save user."}, 500  # Internal Server Error
            return usuario.json(), 201  # Criated

    def get(self, id):
        try:
            usuario = UsuarioModel.find(id)
        except:
            return {"message": "A internal error ocurred trying to get user."}, 500  # Internal Server Error
        return (usuario.json(), 200) if usuario else ({'Mensagem': 'Usuário não encontrado.'}, 404)
    '''
    def put(self, id):
        dados = Usuario.argumentos.parse_args()
        usuario = UsuarioModel.find(id)
        if Usuario:
            try:
                usuario.update_hotel(**dados)
                usuario.save_hotel()
            except:
                return {"message": "A internal error ocurred trying to update user."}, 500  # Internal Server Error
            return usuario.json(), 200
        return {'Mensagem': f'Não foi possível atualizar o usuário {id}'}, 404  # Verificar se esse é o código correto
    '''
    @jwt_required
    def delete(self, id):
        usuairo = UsuarioModel.find(id)
        if usuairo is not None:
            try:
                usuairo.delete()
            except:
                return {"message": "A internal error ocurred trying to delete user."}, 500  # Internal Server Error
            return {'Mensagem:': f'Usuário {id} excluido com sucesso!'}, 200
        return {'Mensagem:': f'Usuário {id} não encontrado!'}, 404

    class Login(Resource):
        @classmethod
        def post(self):
            dados = Usuario.argumentos.parse_args()
            try:
                usuario = UsuarioModel.find_by_login(dados['login'])
            except:
                return {"message": "A internal error ocurred trying to get user."}, 500  # Internal Server Error
            if usuario is not None and safe_str_cmp(usuario.senha, dados['senha']):
                token_de_acesso = create_access_token(identity=usuario.id)
                return {"access_token":token_de_acesso}
            return {"Mensagem":"The user name or password is incorrect."}, 401 # Unauthorized

    class Logout(Resource):
        @jwt_required
        def post(self):
            jwt_id = get_raw_jwt()['jti']
            BLACKLIST.add(jwt_id)
            return {"Mensagem":"Logged out successfully!"}