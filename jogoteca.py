from flask import Flask, render_template, request, redirect, session, flash, url_for
from models import Jogo, Usuario
from dao import JogoDao
import pymysql.cursors



app = Flask(__name__)
app.secret_key = 'zeleleia'

#jogo_dao = JogoDao(db='jogoteca')

#print('Conectando...')
#conn = pymysql.connect(host='127.0.0.1',
                             #user='root',
                             #password='201019',
                             #database='jogoteca',
                             #cursorclass=pymysql.cursors.DictCursor)

#with conn.cursor() as cursor:
    #sql = 'CREATE TABLE '

usuario1 = Usuario('Pedro', 'gonzaga', '201019')
usuario2 = Usuario('Beatryz', 'bona', 'pedro')
usuario3 = Usuario('teste', 'teste', 'teste')

usuarios = { usuario1.nickname:usuario1,
            usuario2.nickname:usuario2,
            usuario3.nickname:usuario3
            }

senhas = { usuario1.senha:usuario1,
           usuario2.senha:usuario2,
           usuario3.senha:usuario3
        }

jogo1 = Jogo('Anel Pristílo', 'RPG', 'Xbox One')
jogo2 = Jogo('Elden Ring', 'RPG', 'PS4')
lista = [jogo1, jogo2]


@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogoteca', cabeçalho='Jogos', jogos=lista)

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuário não logado.')
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=(url_for('novo'))))
    else:
        return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo_dao.salvar('jogo')
    return redirect(url_for('index'))

app.run(debug=True)