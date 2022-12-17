from flask import Flask
#SQLAlchemy conecta banco de dados com a aplicação
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#pega as configurações do arquivo config.py
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run(debug=True)