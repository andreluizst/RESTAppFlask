from sql_alchemy import banco


class HotelModel(banco.Model):
    __tablename__ = 'hoteis'
    id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))

    def __init__(self, id, nome, estrelas, diaria, cidade):
        self.id = id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        return {
            "id": str(self.id),
            "nome": self.nome,
            "estrelas": self.estrelas,
            "diaria": self.diaria,
            "cidade": self.cidade
        }

    def __str__(self):
        return str(self.json())

    @classmethod
    def find_hotel(cls, id):
        hotel = cls.query.filter_by(id=id).first()  # equivalente a: select * from hoteis where id = :id and rownum = 1
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
