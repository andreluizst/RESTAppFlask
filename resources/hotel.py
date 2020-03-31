from flask_restful import Resource, reqparse
from models.hotel_model import HotelModel
from flask_jwt_extended import jwt_required

hoteis = [
    {"id": 1, "nome": "Hotel A", "estrelas": 4.3, "diaria": 420.34, "cidade": "Rio de Janeiro"},
    {"id": 2, "nome": "Hotel B", "estrelas": 4.4, "diaria": 380.90, "cidade": "Santa Catarina"},
    {"id": 3, "nome": "Hotel C", "estrelas": 3.9, "diaria": 320.20, "cidade": "Santa Catarina"}
]


def last_hotel_id():
    lastid = 0
    for hotel in hoteis:
        if int(hotel['id']) > lastid:
            lastid = int(hotel['id'])
    return lastid + 1


def get_hotel_by_id(id):
    for hotel in hoteis:
        if int(hotel['id']) == int(id):
            return hotel
    return None


def novo_hotel(nome, estrelas, diaria, cidade):
    lastid = last_hotel_id()
    hotel = {
        'id': lastid,
        'nome': nome,
        'estrelas': estrelas,
        'diaria': diaria,
        'cidade': cidade
    }
    return hotel


class Hoteis(Resource):
    def get(self):
        json = None
        try:
            json = {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}  # select * from hoteis
        except:
            return {"message": "A internal error ocurred trying to save hotels."}, 500  # Internal Server Error
        return json, 200


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    class Add(Resource):
        @jwt_required
        def post(self):
            dados = Hotel.argumentos.parse_args()
            # hotel = HotelModel(last_hotel_id(), **dados)
            hotel = HotelModel(None, **dados)
            # hotel = novo_hotel(dados['nome'], dados['estrelas'], dados['diaria'], dados['cidade'])
            # hotel_json = hotel.json()
            # hoteis.append(hotel_json)
            # print('Objeto HotelModel:')
            # print(hotel)
            try:
                hotel.save_hotel()
            except:
                return {"message": "A internal error ocurred trying to save hotel."}, 500  # Internal Server Error
            return hotel.json(), 201  # Criated

    def get(self, id):
        # hotel = get_hotel_by_id(id)
        try:
            hotel = HotelModel.find_hotel(id)
        except:
            return {"message": "A internal error ocurred trying to get hotel."}, 500  # Internal Server Error
        return (hotel.json(), 200) if hotel else ({'Mensagem': 'Hotel não encontrado.'}, 404)

    '''
    def post(self, id):
        dados = Hotel.argumentos.parse_args()
        novo_hotel = {
            'id': int(id),
            'nome': dados['nome'],
            'estrelas': dados['estrelas'],
            'diaria': dados['diaria'],
            'cidade': dados['cidade']
        }
        hoteis.append(novo_hotel)
        return novo_hotel, 200
        '''

    @jwt_required
    def put(self, id):
        dados = Hotel.argumentos.parse_args()
        # obj_hotel_received = HotelModel(id, **dados)
        # hotel_received = obj_hotel_received.json()
        # hotel = get_hotel_by_id(id)
        hotel = HotelModel.find_hotel(id)
        if hotel:
            # hotel.update(hotel_received)
            try:
                hotel.update_hotel(**dados)
                hotel.save_hotel()
            except:
                return {"message": "A internal error ocurred trying to update hotel."}, 500  # Internal Server Error
            return hotel.json(), 200
        return {'Mensagem': f'Não foi possível atualizar o hotel {id}'}, 404  # Verificar se esse é o código correto

    @jwt_required
    def delete(self, id):
        # global hoteis
        # hoteis = [hotel for hotel in hoteis if hotel['id'] != int(id)]
        hotel = HotelModel.find_hotel(id)
        if hotel is not None:
            try:
                hotel.delete_hotel()
            except:
                return {"message": "A internal error ocurred trying to delete hotel."}, 500  # Internal Server Error
            return {'Mensagem:': f'Hotel {id} excluido com sucesso!'}, 200
        return {'Mensagem:': f'Hotel {id} não encontrado!'}, 404
