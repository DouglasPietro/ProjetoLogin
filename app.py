from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


def init_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefone TEXT,
            senha TEXT NOT NULL,
            tipo TEXT DEFAULT 'usuario' CHECK(tipo IN ('usuario', 'prestador')),
            servico TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    usuario = session.get('usuario')
    tipo_usuario = session.get('tipo')
    return render_template('index.html',
                           usuario=usuario,
                           tipo_usuario=tipo_usuario)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        return redirect(url_for('index'))

    erro = None
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            erro = "Preencha todos os campos"
        else:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM usuarios WHERE email = ?',
                                (email, )).fetchone()
            conn.close()

            if user and check_password_hash(user['senha'], senha):
                session['usuario'] = user['nome']
                session['tipo'] = user['tipo']
                session['email'] = user['email']
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('index'))
            else:
                erro = "E-mail ou senha inválidos."

    return render_template('login.html', erro=erro)


@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('index'))


@app.route('/cadastrousuario', methods=['GET', 'POST'])
def cadastrousuario():
    if 'usuario' in session:
        return redirect(url_for('index'))

    erro = None
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        senha = request.form.get('senha')

        if not all([nome, email, senha]):
            erro = "Preencha todos os campos obrigatórios"
        else:
            try:
                conn = get_db_connection()
                conn.execute(
                    'INSERT INTO usuarios (nome, email, telefone, senha, tipo) VALUES (?, ?, ?, ?, ?)',
                    (nome, email, telefone, generate_password_hash(senha),
                     'usuario'))
                conn.commit()
                conn.close()
                flash(
                    'Cadastro realizado com sucesso! Faça login para continuar.',
                    'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                erro = 'Este e-mail já está cadastrado.'

    return render_template('cadastrousuario.html', erro=erro)


@app.route('/cadastroprestador', methods=['GET', 'POST'])
def cadastroprestador():
    if request.method == 'POST':
        nome = request.form['nome']
        session['usuario'] = nome
        return redirect(url_for('sucesso'))

    return render_template('cadastroprestador.html')


@app.route('/contato')
def contato():
    usuario = session.get('usuario')
    tipo_usuario = session.get('tipo')
    return render_template('CONTATO.HTML',
                           usuario=usuario,
                           tipo_usuario=tipo_usuario)


@app.route('/quemsomosx')
def quemsomosx():
    usuario = session.get('usuario')
    tipo_usuario = session.get('tipo')
    return render_template('quemsomosx.html',
                           usuario=usuario,
                           tipo_usuario=tipo_usuario)


@app.route('/sucesso')
def sucesso():
    usuario = session.get('usuario')
    return render_template('sucesso.html', usuario=usuario)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)

