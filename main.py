from flask import Flask, render_template, redirect, url_for, flash, request, session
import fdb
import re

app = Flask(__name__)
app.secret_key = 'matheus-lindo'

host = 'localhost'
database = r'C:\Users\Aluno\PycharmProjects\Esse\WePay.FDB'
user = 'SYSDBA'
password = 'sysdba'

con = fdb.connect(host=host, database=database, user=user, password=password)

class Usuario:
    def __init__(self, id_usuario, nome, senha, email):
        self.id_usuario = id_usuario
        self.nome = nome
        self.senha = senha
        self.email = email

class Despesa:
    def __init__(self, id_despesa, id_usuario, preco, descricao):
        self.id_despesa = id_despesa
        self.id_usuario = id_usuario
        self.preco = preco
        self.descricao = descricao

class Receita:
    def __init__(self, id_receita, id_usuario, preco, descricao):
        self.id_receita = id_receita
        self.id_usuario = id_usuario
        self.preco = preco
        self.descricao = descricao



def validar_senha(senha):
    # Expressão regular para validar os critérios
    regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$'
    # Retorna True se a senha for válida, False caso contrário
    return bool(re.fullmatch(regex, senha))

@app.route('/')
def index():
    cursor = con.cursor()
    cursor.execute("SELECT id_usuario, nome, senha, email FROM USUARIO")
    usuario = cursor.fetchall()
    cursor.close()
    return render_template('index.html', usuario=usuario, modal=False)

@app.route('/financas2')
def financas2():
    return render_template('financas2.html')

@app.route('/financas')
def financas(modal=False):
    nome = session.get('nome')


    if nome is None:
        flash("Sessão não iniciada", "error")
        return redirect(url_for('index'))

    cursor = con.cursor()

    cursor.execute("SELECT PRECO FROM DESPESA WHERE ID_USUARIO = ?", (session.get('id_usuario'),))
    despesa = 0
    for item in cursor.fetchall():
        despesa += item[0]

    cursor.execute("SELECT PRECO FROM RECEITA WHERE ID_USUARIO = ?", (session.get('id_usuario'),))
    receita = 0
    for item2 in cursor.fetchall():
        receita += item2[0]

    cursor.execute("SELECT descricao, preco, data, id_despesa FROM DESPESA WHERE ID_USUARIO = ?", (session.get('id_usuario'),))
    historico_despesa = cursor.fetchall()

    cursor.execute("SELECT descricao, preco, data, id_receita FROM RECEITA WHERE ID_USUARIO = ?", (session.get('id_usuario'),))
    historico_receita = cursor.fetchall()

    cursor.close()
    return render_template('financas.html', despesa=despesa, receita=receita, historico_despesa=historico_despesa, historico_receita=historico_receita,nome = nome, modal=modal)

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    senha = request.form['senha']
    email = request.form['email']

    if not nome or not senha or not email:
        flash("Todos os campos são obrigatórios", "error")
        return render_template('index.html', modal="cadastro")

        # Valida a força da senha
    if not validar_senha(senha):
        flash("Senha fraca! Inclua letras maiúsculas, minúsculas, números e caracteres especiais.", "error")
        return render_template('index.html', modal="cadastro")

    cursor = con.cursor()
    try:
        cursor.execute("SELECT * FROM usuario WHERE EMAIL = ?", (email,))
        if cursor.fetchone():
            flash("Email já cadastrado.", "error")
            return render_template('index.html', modal="cadastro")
        cursor.execute(
            "INSERT INTO usuario (NOME, senha, EMAIL) VALUES (?, ?, ?)",
            (nome, senha, email)
        )
        con.commit()
    finally:
        cursor.close()

    flash("Usuário cadastrado com sucesso!", "success")
    return render_template('index.html', modal="login")

@app.route('/login', methods=['POST', 'GET'])
def login():
    senha = request.form['senha']
    email = request.form['email']

    if not email or not senha:
        flash("Todos os campos são obrigatórios", "error")
        return render_template('index.html', modal="login")

    cursor = con.cursor()

    cursor.execute('SELECT senha, id_usuario, nome FROM Usuario WHERE email = ?', (email,))
    usuario = cursor.fetchone()
    cursor.close()
    if usuario and usuario[0] == senha:
        session['id_usuario'] = usuario[1]
        session['nome'] = usuario[2]
        return redirect(url_for('financas'))
    else:
        flash("Email ou senha inválidos!", "error")
        return render_template('index.html', modal="login")


@app.route('/nova_transacao/<tipo>', methods=['POST'])
def nova_transacao(tipo):
    fonte = request.form['descricao']
    valor = request.form['valor']
    data = request.form['data']
    id_usuario = session.get('id_usuario')

    if not fonte or not valor or not data or not id_usuario:
        flash("Todos os campos são obrigatórios", 'error')
        return financas("financas")

    if not id_usuario:
        flash("Sessão não iniciada", "error")
        return redirect(url_for('index'))

    cursor = con.cursor()
    if tipo == 'saida':
        cursor.execute('''
            INSERT INTO despesa (ID_USUARIO, PRECO, DESCRICAO, DATA)
            VALUES (?,?,?,?)
        ''', (id_usuario, valor, fonte, data))
        con.commit()
    if tipo == 'entrada':
        cursor.execute('''
            INSERT INTO receita (ID_USUARIO, PRECO, DESCRICAO, DATA)
            VALUES (?,?,?,?)
        ''', (id_usuario, valor, fonte, data))
        con.commit()

    cursor.close()
    return redirect(url_for('financas'))

@app.route('/editar_transacao', methods=['POST'])
def editar():
    fonte = request.form['fonte']
    valor = request.form['valor']
    data = request.form['data']
    tipo = request.form['tipo']
    id_transacao = request.form['id']

    if not fonte or not valor or not data or not tipo or not id_transacao:
        flash("Todos os campos são obrigatórios", 'error')
        return redirect(url_for('financas', ))

    cursor = con.cursor()

    if tipo == 'receita':
        cursor.execute('''
            UPDATE RECEITA SET descricao = ?, preco = ?, data = ?
            WHERE ID_RECEITA = ? 
        ''', (fonte, valor, data, id_transacao))

    if tipo == 'despesa':
        cursor.execute('''
            UPDATE DESPESA SET descricao = ?, preco = ?, data = ?
            WHERE ID_DESPESA = ? 
        ''', (fonte, valor, data, id_transacao))

    con.commit()
    cursor.close()

    return redirect(url_for('financas'))

@app.route('/excluir_transacao', methods=['POST'])
def excluir():
    tipo = request.form['tipo']
    id_transacao = request.form['id']

    cursor = con.cursor()

    if tipo == 'receita':
        cursor.execute('DELETE FROM RECEITA WHERE ID_RECEITA = ?', (id_transacao,))

    if tipo == 'despesa':
        cursor.execute('DELETE FROM DESPESA WHERE ID_DESPESA = ?', (id_transacao,))

    con.commit()
    cursor.close()

    return redirect(url_for('financas'))

@app.route('/sair')
def sair():
    session.pop('id_usuario', None)
    session.pop('nome', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)