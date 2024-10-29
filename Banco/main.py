from db_connection import get_session
import uuid

session = get_session()
session.set_keyspace('meu_keyspace')

# Função para inserir uma receita
def inserir_receita(nome, ingredientes):
    session.execute("""
        INSERT INTO receitas (id, nome, ingredientes)
        VALUES (%s, %s, %s)
    """, (uuid.uuid4(), nome, ingredientes))

# Função para consultar receitas
def consultar_receitas():
    rows = session.execute("SELECT * FROM receitas")
    for row in rows:
        print(row.id, row.nome, row.ingredientes)

# Exemplo de uso
inserir_receita("Bolo de Chocolate", "Farinha, Açúcar, Cacau, Fermento")
consultar_receitas()

# Feche a conexão ao final
session.shutdown()
