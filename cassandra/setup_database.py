from db_connection import get_session

session = get_session()

# Criação do keyspace
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS LaricaBook
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")

# Conectando ao keyspace
session.set_keyspace('laricabook')

# Criação da tabela "receitas"
session.execute("""
    CREATE TABLE IF NOT EXISTS receitas (
    id_receita UUID PRIMARY KEY,
    nome_receita TEXT,
    categoria TEXT,
    ingredientes LIST<TEXT>,  
    instrucoes TEXT,
    tempo_preparo INT,  
    porcoes INT,
    foto BLOB,          
    fonte_links TEXT,  
    data_adicao TIMESTAMP
    );
""")

# Criação da tabela "comentarios"
session.execute("""
    CREATE TABLE IF NOT EXISTS receitasComentarios (
    comentario_id UUID,
    id_receita UUID,
    usuario_id UUID,
    comentario TEXT,
    avaliacao INT,
    data TIMESTAMP,
    PRIMARY KEY ((id_receita), data, comentario_id)
    );
""")

# Criação da tabela "categorias"
session.execute("""
    CREATE TABLE IF NOT EXISTS categoriasReceitas (
    categoria text,
    id_receita UUID,
    PRIMARY KEY (categoria, id_receita)
    );
""")

# Criação da tabela "de usuários"
session.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario UUID PRIMARY KEY,
        nome TEXT,
        email TEXT,
        senha TEXT, 
        data_criacao TIMESTAMP,
        foto_perfil BLOB
    );
""")

#Criar depois um insert padrão para execução

session.shutdown()

