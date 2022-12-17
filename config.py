#camada de criptografia para as informações guardadas nos cookies
#se estivesse no app.py = app.secret_key 
SECRET_KEY = 'Alohomora'

#configuração banco de dados
#se estivesse no app.py = app.config['SQLALCHEMY_DATABASE_URI']
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'root',
        servidor = 'localhost',
        database = 'jogoteca'
    )