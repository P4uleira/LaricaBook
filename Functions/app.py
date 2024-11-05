from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import uuid
import os
from Cassandra.db_connection import get_session

session_bd = get_session()
session_bd.set_keyspace('laricabook')

app = Flask(__name__, 
            template_folder=os.path.join("..", "templates"), 
            static_folder=os.path.join("..", "static"))

UPLOAD_FOLDER = os.path.join(app.static_folder, 'Imagens')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.secret_key = 'laricabook'

# Sistema de login do larica
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/SignUP')
def signIN():
    return render_template('SignUP.html')

@app.route('/cadastraUser', methods=['POST',])
def cadastrarUser():

    id_usuario = uuid.uuid4()
    nome_usuario = request.form['name']
    email_usuario = request.form['email']
    senha_usuario = request.form['password']

    try:
        session_bd.execute("""
            INSERT INTO laricabook.usuarios (id_usuario, nome, data_criacao, email, senha)
            VALUES (%s, %s, toTimestamp(now()), %s, %s)
        """, (id_usuario, nome_usuario, email_usuario, senha_usuario)
        )
    except Exception as e:
        print(f"Erro ao inserir o usuário: {e}")

    return render_template('index.html')

@app.route('/validaUsuario', methods=['POST',])
def validaUsario():

    nome_usuario = request.form['username']
    senha_usuario = request.form['password']

    try:
        query ="""
            SELECT * FROM usuarios WHERE nome = %s AND senha = %s ALLOW FILTERING
        """
        
        resultadoBusca = session_bd.execute(query, (nome_usuario, senha_usuario))

        if resultadoBusca :
            session['nome_usuario'] = nome_usuario
            session['id_usuario'] = resultadoBusca[0].id_usuario
            return render_template('home.html')
        else:
            flash('Usuário ou senha incorretas!')
            return render_template('index.html')

    except Exception as e:
        print(f"Erro ao tentar logar no sistema {e}")

import os

@app.route('/Home')
def home():
    if session.get('nome_usuario') is None:
        return render_template('index.html')
    else:
        try:
            query = "SELECT * FROM laricabook.receitas"
            receitas = session_bd.execute(query)
            extensoes_permitidas = ['jpg', 'png', 'jpeg']
            
            receitas_list_home = []
            for receita in receitas:
                
                caminho_imagem = None
                for ext in extensoes_permitidas:
                    nome_imagem = f"{receita.id_usuario}_{receita.id_receita}.{ext}"
                    caminho_possivel = os.path.join(UPLOAD_FOLDER, nome_imagem)
                    print(f"Verificando caminho da imagem: {caminho_possivel}")
                    if os.path.exists(caminho_possivel): 
                        caminho_imagem = f"Imagens/{nome_imagem}"
                        print(f"Imagem encontrada: {caminho_imagem}")
                        break  
                
                receitas_list_home.append({
                    'nome_receita': receita.nome_receita,
                    'categoria': receita.categoria,
                    'fonte_link': receita.fonte_links,  
                    'ingredientes': ', '.join(receita.ingredientes),  
                    'instrucoes': receita.instrucoes,
                    'porcoes': receita.porcoes,
                    'tempo_preparo': receita.tempo_preparo,
                    'imagem': caminho_imagem
                })

        except Exception as e:
            print(f"Erro ao mostrar receitas: {e}")

        return render_template('home.html', receitas=receitas_list_home)


# Fim do sistema de Login

# Logoff do sistema
@app.route('/LogOFF')
def logOff():
    session.pop('nome_usuario', None)

    return render_template('index.html')
# fim do Logoff do sistema


# Sistema de receitas
@app.route('/HomeReceita')
def homeReceita():
    if session.get('nome_usuario') is None :
        return render_template('index.html')
        print(f"tem sessão: " + session['nome_usuario'])
    else:
        
        try:
            query = "SELECT * FROM laricabook.receitas WHERE receita_publica = true ALLOW FILTERING"
            receitas = session_bd.execute(query)
            extensoes_permitidas = ['jpg', 'png', 'jpeg']
            
            receitas_list = []
            for receita in receitas:
                
                caminho_imagem = None
                for ext in extensoes_permitidas:
                    nome_imagem = f"{receita.id_usuario}_{receita.id_receita}.{ext}"
                    caminho_possivel = os.path.join(UPLOAD_FOLDER, nome_imagem)
                    print(f"Verificando caminho da imagem: {caminho_possivel}")
                    if os.path.exists(caminho_possivel): 
                        caminho_imagem = f"Imagens/{nome_imagem}"
                        print(f"Imagem encontrada: {caminho_imagem}")
                        break  
                
                receitas_list.append({
                    'nome_receita': receita.nome_receita,
                    'categoria': receita.categoria,
                    'fonte_link': receita.fonte_links,  
                    'ingredientes': ', '.join(receita.ingredientes),  
                    'instrucoes': receita.instrucoes,
                    'porcoes': receita.porcoes,
                    'tempo_preparo': receita.tempo_preparo,
                    'imagem': caminho_imagem
                })
        except Exception as e:
            print(f"Erro ao mostrar receitas: {e}")

        return render_template('HomeReceita.html', receitas=receitas_list)

@app.route('/InserirReceita')
def inserirReceita():
    if session.get('nome_usuario') is None :
        return render_template('index.html')
        print(f"tem sessão: " + session['nome_usuario'])
    else:
        return render_template('InsereReceita.html')

@app.route('/enviaReceita', methods=['POST',])
def add_receita():

    id_receita = uuid.uuid4()
    nome_receita = request.form['nome_receita']
    categoria_receita = request.form['categoria']
    fontes_link_receita = request.form['fontes_links']
    ingredientes_receita = request.form['ingredientes']
    ingredientes_lista = [ingrediente.strip() for ingrediente in ingredientes_receita.split(',')]
    instrucoes_receita = request.form['instrucoes']
    porcoes_receita = request.form['porcoes']
    porcoes_receita = int(porcoes_receita)
    tempo_preparo_receita = request.form['tempo_preparo'] 
    tempo_preparo_receita = int(tempo_preparo_receita)
    receita_publica = request.form['publico'] == 'true'
    id_usuario = session['id_usuario']
    imagem_receita = request.files['imagem']
    
    extensao = imagem_receita.filename.rsplit('.', 1)[1].lower()
    nome_imagem = f"{id_usuario}_{id_receita}.{extensao}" 
    caminho_imagem = os.path.join(UPLOAD_FOLDER, nome_imagem)
    imagem_receita.save(caminho_imagem)  

    try:
        session_bd.execute(""" 
        INSERT INTO laricabook.receitas (id_receita, nome_receita, categoria, data_adicao, fonte_links, ingredientes, instrucoes, porcoes, tempo_preparo, receita_publica, id_usuario
        ) VALUES (%s, %s, %s, toTimestamp(now()), %s, %s, %s, %s, %s, %s, %s)
        """, (id_receita, nome_receita, categoria_receita, fontes_link_receita, ingredientes_lista, instrucoes_receita, porcoes_receita, tempo_preparo_receita, receita_publica, id_usuario)
        )
    except Exception as e:
        print(f"Erro ao inserir a receita: {e}")

    return render_template('InsereReceita.html')



if __name__ == '__main__':
    app.run(debug=True)