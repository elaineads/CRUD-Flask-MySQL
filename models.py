from jogoteca import db

#conexão SQLAlquemy e banco de dados
class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    #boas práticas
    #__repr__ representa os objetos da classe como uma string, normalmente usado para depuração
    def __repr__(self):
        return 'Name %r' %self.name

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'Name %r' %self.name