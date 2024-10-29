from flask import *
import uuid
from Banco.db_connection import get_session

session = get_session()
session.set_keyspace('laricabook')

app = Flask(__name__, template_folder="../Front")

@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar o formulário
@app.route('/add_receita', methods=['POST'])
def add_receita():
    # Coleta os dados do formulário
    nome_receita = request.form['nome_receita']
    categoria = request.form['categoria']
    ingredientes = request.form['ingredientes'].split(',')
    instrucoes = request.form['instrucoes']
    tempo_preparo = int(request.form['tempo_preparo'])
    porcoes = int(request.form['porcoes'])

    # Gera um ID único para a receita
    id_receita = uuid.uuid4()

    # Conecta ao Cassandra e insere a receita
    session = get_session()
    session.execute("""
        INSERT INTO laricabook.receitas (id_receita, nome_receita, categoria, ingredientes, instrucoes, tempo_preparo, porcoes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (id_receita, nome_receita, categoria, ingredientes, instrucoes, tempo_preparo, porcoes))

    session.shutdown()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
