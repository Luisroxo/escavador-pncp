import psycopg2
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST")
}

def test_db_connection():
    try:
        print("Conectando ao banco de dados...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("Conexão estabelecida com sucesso!")

        cur = conn.cursor()
        print("Verificando a existência da tabela 'participantes'...")
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'participantes';
        """)

        columns = cur.fetchall()
        if columns:
            print("Tabela 'participantes' encontrada com as seguintes colunas:")
            for column in columns:
                print(f"- {column[0]}")
        else:
            print("Tabela 'participantes' não encontrada.")

        cur.close()
    except Exception as e:
        print(f"Erro ao conectar ou verificar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados encerrada.")

if __name__ == "__main__":
    test_db_connection()
