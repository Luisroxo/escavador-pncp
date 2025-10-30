import psycopg2
import logging

DB_CONFIG = {
    "dbname": "licitacoes",
    "user": "luis",
    "password": "020646Juan",
    "host": "localhost",
    "port": 5434
}

def limpar_tabela():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM participantes;")
        conn.commit()
        logging.info("Tabela 'participantes' limpa com sucesso.")
        conn.close()
    except psycopg2.Error as e:
        logging.error(f"Erro ao limpar a tabela: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    limpar_tabela()