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
        id_receita UUID,
        nome_receita TEXT,
        categoria TEXT,
        data_adicao TIMESTAMP,
        fonte_links TEXT,  
        ingredientes LIST<TEXT>,  
        instrucoes TEXT,
        porcoes INT,          
        tempo_preparo INT,  
        receita_publica BOOLEAN,
        id_usuario UUID,
        PRIMARY KEY (id_receita)
    ) WITH CLUSTERING;
""")

# Criação da tabela "usuarios"
session.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario UUID,
        nome TEXT,
        email TEXT,
        senha TEXT,
        data_criacao TIMESTAMP,
        PRIMARY KEY (id_usuario, nome)
    ) WITH CLUSTERING ORDER BY (nome ASC);
""")


session.shutdown()

