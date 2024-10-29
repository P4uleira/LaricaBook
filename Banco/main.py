from db_connection import get_session
import uuid

session = get_session()
session.set_keyspace('laricabook')

# Função para inserir uma receita
def inserir_receita(nome, ingredientes):
    session.execute("""
        INSERT INTO receitas (id_receita, nome_receita, ingredientes)
        VALUES (%s, %s, %s)
    """, (uuid.uuid4(), nome, ingredientes))

# Função para consultar receitas
def consultar_receitas():
    rows = session.execute("SELECT * FROM receitas")
    for row in rows:
        print(row.id_receita, row.nome_receita, row.ingredientes)
        
def excluir_receita(id_receita):
    session.execute("DELETE FROM receitas WHERE id_receita = %s", (id_receita))

# Exemplo de uso
ingredientes1 = ["Farinha", "Açúcar", "Cacau", "Fermento"]
#inserir_receita("Bolo de Chocolate", ingredientes1)
excluir_receita()
consultar_receitas()


# Feche a conexão ao final
session.shutdown()
