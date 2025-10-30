import psycopg2

try:
    conn = psycopg2.connect(
        dbname="licitacoes",
        user="luis",
        password="020646Juan",
        host="host.docker.internal",  # Padrão para acesso ao host via Docker
        port=5432
    )
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro na conexão: {e}")
