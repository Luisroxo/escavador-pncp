import psycopg2
import logging

DB_CONFIG = {
    "dbname": "licitacoes",
    "user": "luis",
    "password": "020646Juan",
    "host": "localhost",
    "port": 5434
}

def verificar_encoding():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT * FROM participantes LIMIT 10;")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        conn.close()
    except psycopg2.Error as e:
        logging.error(f"Erro ao acessar o banco de dados: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    verificar_encoding()