from flask import Flask, render_template, request, redirect, url_for
import uuid
import os
from Cassandra.db_connection import get_session

session = get_session()
session.set_keyspace('laricabook')

app = Flask(__name__, template_folder=os.path.join("..", "templates"))

@app.route('/')
def index():
    query = "SELECT * FROM receitas;"  # Não usar DISTINCT
    rows = session.execute(query)
    data = [dict(row._asdict()) for row in rows]

    # Remover duplicatas em Python
    unique_data = []
    seen = set()
    for item in data:
        # Aqui, você pode escolher quais chaves usar como identificador único
        item_tuple = tuple((key, item[key]) for key in item if key == "sua_chave_unica")  # Substitua "sua_chave_unica" pela chave que identifica unicamente o item
        if item_tuple not in seen:
            unique_data.append(item)
            seen.add(item_tuple)

    return render_template('index.html', data=unique_data)

@app.route('/InserirReceita')
def inserirReceita():
    return render_template('InserirReceita.html')


@app.route('/add_receita', methods=['POST',])
def add_receita():

    id_receita = uuid.uuid4()
    nome_receita = request.form['nome_receita']
    categoria = request.form['categoria']
    ingredientes = request.form['ingredientes'].split(',')
    instrucoes = request.form['instrucoes']
    tempo_preparo = int(request.form['tempo_preparo'])
    porcoes = int(request.form['porcoes'])
    fontes_link = request.form['fontes']
    foto_receita = request.files['foto']
    foto_blob = foto_receita.read()

    try:
        session.execute("""
            INSERT INTO laricabook.receitas (id_receita, nome_receita, categoria, ingredientes, instrucoes, tempo_preparo, porcoes, fonte_links, foto, data_adicao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, toTimestamp(now()))
        """, (id_receita, nome_receita, categoria, ingredientes, instrucoes, tempo_preparo, porcoes, fontes_link, foto_blob)
        )
    except Exception as e:
        print(f"Erro ao inserir a receita: {e}")

    return redirect(url_for('inserirReceita'))






















if __name__ == '__main__':
    app.run(debug=True)
