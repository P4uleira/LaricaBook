from cassandra.cluster import Cluster

def get_session():
    # Cria a conexão com o Cassandra e retorna a sessão
    cluster = Cluster(['localhost'])
    session = cluster.connect()
    return session