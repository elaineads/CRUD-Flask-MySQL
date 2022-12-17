from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Tetrs', 'Puzze', 'Atari')
jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombate', 'Luta', 'PS2')

lista = [jogo1, jogo2, jogo3]

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Elaine', 'elaineads', '123')
usuario2 = Usuario('Lua', 'luazinha', '1234')
usuario3 = Usuario('Bellatrix', 'bella', '12345')

usuarios = {usuario1.nickname: usuario1,
            usuario2.nickname: usuario2,
            usuario3.nickname: usuario3,}

app = Flask(__name__)
#camada de criptografia para as informações guardadas nos cookies
app.secret_key = 'Alohomora'

@app.route('/')
def index():
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

    jogo = Jogo(nome, categoria, console)
    lista.append(jogo) #adiciona item a lista

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
    #se o nome de usuário estiver na lista de usuários
    if request.form['usuario'] in usuarios:
        #chave do dicionário para o usuário
        usuario = usuarios[request.form['usuario']]
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