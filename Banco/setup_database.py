from db_connection import get_session

session = get_session()

# Criação do keyspace
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS meu_keyspace
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")

# Conectando ao keyspace
session.set_keyspace('meu_keyspace')

# Criação da tabela "receitas"
session.execute("""
    CREATE TABLE IF NOT EXISTS receitas (
        id UUID PRIMARY KEY,
        nome text,
        ingredientes text
    )
""")

# Feche a conexão ao final (opcional)
session.shutdown()

