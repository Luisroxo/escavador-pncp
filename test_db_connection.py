import psycopg2
import os
from dotenv import load_dotenv
import logging

# Configuração de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")  # Adicionar a porta
}

def test_db_connection():
    try:
        logging.info("Conectando ao banco de dados...")
        conn = psycopg2.connect(**DB_CONFIG)
        logging.info("Conexão estabelecida com sucesso!")

        # Testar uma consulta simples
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            logging.info(f"Resultado da consulta: {result}")

    except psycopg2.Error as e:
        logging.error(f"Erro ao conectar ou verificar o banco de dados: {e}")

    finally:
        if 'conn' in locals() and conn:
            conn.close()
            logging.info("Conexão com o banco de dados encerrada.")

if __name__ == "__main__":
    test_db_connection()
