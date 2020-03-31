from sql_alchemy import banco


class UsuarioModel(banco.Model):
    __tablename__ = 'usuarios'
    id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    def json(self):
        return {
            "id": str(self.id),
            "login": self.login
        }

    def __str__(self):
        return str(self.json())

    @classmethod
    def find(cls, id):
        usuario = cls.query.filter_by(id=id).first()  # equivalente a: select * from usuarios where id = :id and rownum = 1
        if usuario:
            return usuario
        return None

    @classmethod
    def find_by_login(cls, login):
        usuario = cls.query.filter_by(login=login).first()
        if usuario:
            return usuario
        return None

    def save(self):
        banco.session.add(self)
        banco.session.commit()

    def delete(self):
        banco.session.delete(self)
        banco.session.commit()
