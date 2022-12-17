from flask import Flask, render_template, request, redirect, session, flash

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console

jogo1 = Jogo('Tetrs', 'Puzze', 'Atari')
jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombate', 'Luta', 'PS2')

lista = [jogo1, jogo2, jogo3]

app = Flask(__name__)
#camada de criptografia para as informações guardadas nos cookies
app.secret_key = 'Alohomora'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')

#rota intermediária entre '/' e '/novo'
@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome'] #request pega a informação 'name' do formulário
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    lista.append(jogo) #adiciona item a lista

    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

#rota intermediária entre '/login' e '/novo'
@app.route('/autenticar', methods=['POST',])
def autenticar():
    #verificando se a senha está correta
    if 'alohomora' == request.form['senha']:
        #guardando o nome do usuário nos cookies do navegador
        session['usuario_logado'] = request.form['usuario']

        flash(session['usuario_logado'] + ' logado com sucesso!') #mensagem
        return redirect('/')
    else:
        flash('Usuário não logado.')
        return redirect('/login')

app.run(debug=True)