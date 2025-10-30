import json
import re
import psycopg2
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager
import logging

DB_CONFIG = {
    "dbname": "licitacoes",
    "user": "luis",
    "password": "020646Juan",
    "host": "postgres"
}

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Iniciando o ciclo de vida do aplicativo.")
    setup_database()
    yield
    logging.info("Encerrando o ciclo de vida do aplicativo.")

app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app).expose(app)

logging.info("Serviço de persistência iniciado. Aguardando conexões...")

def setup_database():
    """Cria a tabela 'participantes' no PostgreSQL."""
    conn = None
    try:
        logging.info("Conectando ao banco de dados para configurar a tabela 'participantes'.")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS participantes (
                id SERIAL PRIMARY KEY,
                cnpj_cpf VARCHAR(18) UNIQUE NOT NULL,
                categoria VARCHAR(20) NOT NULL,
                razao_social VARCHAR(255),
                situacao_cadastral VARCHAR(50),
                porte_empresa VARCHAR(50),
                capital_social NUMERIC(15, 2),
                cnaes JSONB,
                endereco JSONB,
                contato JSONB,
                redes_sociais JSONB,
                whatsapp VARCHAR(20),
                data_extracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        logging.info("Tabela 'participantes' configurada com sucesso.")
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Erro ao conectar ou configurar o PostgreSQL: {error}")
    finally:
        if conn:
            conn.close()

@app.post("/participantes")
def insert_data_api(data: dict):
    """Recebe dados via API e insere no PostgreSQL."""
    logging.info("Recebendo dados para inserção/atualização na tabela 'participantes'.")
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        for categoria, cnpjs in data.items():
            logging.info(f"Processando categoria: {categoria}")
            for cnpj_cpf in cnpjs:
                cnpj_cpf_clean = re.sub(r'[^0-9]', '', cnpj_cpf)
                logging.info(f"Inserindo/atualizando CNPJ/CPF: {cnpj_cpf_clean}")
                insert_query = """
                    INSERT INTO participantes (cnpj_cpf, categoria)
                    VALUES (%s, %s)
                    ON CONFLICT (cnpj_cpf) 
                    DO UPDATE SET categoria = EXCLUDED.categoria || ' | ' || participantes.categoria
                    WHERE participantes.categoria NOT LIKE '%%' || EXCLUDED.categoria || '%%';
                """
                cur.execute(insert_query, (cnpj_cpf_clean, categoria))
        conn.commit()
        cur.close()
        logging.info("Dados inseridos/atualizados com sucesso.")
        return {"message": "Dados inseridos/atualizados com sucesso."}
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Erro ao inserir/atualizar dados: {error}")
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        if conn:
            conn.close()

@app.get("/participantes")
def get_participantes():
    logging.info("Recebendo solicitação para listar participantes.")
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT * FROM participantes LIMIT 100;")
        rows = cur.fetchall()
        cur.close()
        logging.info("Participantes recuperados com sucesso.")
        return {"participantes": rows}
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Erro ao recuperar participantes: {error}")
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        if conn:
            conn.close()
