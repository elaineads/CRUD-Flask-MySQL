from flask import Flask, render_template, request, redirect, session, flash, url_for
#SQLAlchemy conecta banco de dados com a aplicação
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#camada de criptografia para as informações guardadas nos cookies
app.secret_key = 'Alohomora'

#configuração banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'root',
        servidor = 'localhost',
        database = 'jogoteca'
    )

db = SQLAlchemy(app)

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

@app.route('/')
def index():
    #query faz uma consulta no banco de dados
    lista = Jogos.query.order_by(Jogos.id)
    #render_template renderiza a página
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    #adicionando etapa de verificação, o usuário só pode acessar esta rota se estiver logado
    #caso o usuário não esteja logado ou esteja deslogado redireciona para tela de login
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        #a proxima página a ser redirecionada será a 'novo'
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

#rota intermediária entre '/' e '/novo'
@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome'] #request pega a informação 'name' do formulário
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já existe!')
        return redirect(url_for('index'))

    #adicionando novo jogo
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    #redirect redireciona para outra página, a rota criar não aparece no navegador
    return redirect(url_for('index'))

@app.route('/login')
def login():
    #capturando as informações da variável próxima
    proxima = request.args.get('proxima')
    #mandando as informações da próxima página para o html
    return render_template('login.html', proxima=proxima)

#rota intermediária entre '/login' e '/novo'
@app.route('/autenticar', methods=['POST',])
def autenticar():
    #se o nickname estiver na tabela de usuários
    #first retorna a primeira ocorrência
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        #verificando se a senha está correta
        if request.form['senha'] == usuario.senha:
            #guardando o nickname do usuário nos cookies do navegador
            session['usuario_logado'] = usuario.nickname

            flash(usuario.nickname + ' logado com sucesso!') #mensagem

            #pegando informações do formulário de login
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)      
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    #retirando dados do navegador
    session['usuario_logado'] = None

    flash('Logout efetuado com sucessso!')
    return redirect(url_for('index'))

app.run(debug=True)