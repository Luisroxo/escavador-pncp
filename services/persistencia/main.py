import json
import re
from fastapi import FastAPI, HTTPException

import psycopg2
import json
import re
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

DB_CONFIG = {
    "dbname": "licitacoes",
    "user": "luis",
    "password": "020646Juan",
    "host": "postgres"
}


app = FastAPI()
Instrumentator().instrument(app).expose(app)

def setup_database():
    """Cria a tabela 'participantes' no PostgreSQL."""
    conn = None
    try:
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
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao conectar ou configurar o PostgreSQL: {error}")
    finally:
        if conn:
            conn.close()

@app.on_event("startup")
def startup_event():
    setup_database()

@app.post("/participantes")
def insert_data_api(data: dict):
    """Recebe dados via API e insere no PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        for categoria, cnpjs in data.items():
            for cnpj_cpf in cnpjs:
                cnpj_cpf_clean = re.sub(r'[^0-9]', '', cnpj_cpf)
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
        return {"message": "Dados inseridos/atualizados com sucesso."}
    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        if conn:
            conn.close()

@app.get("/participantes")
def get_participantes():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT * FROM participantes LIMIT 100;")
        rows = cur.fetchall()
        cur.close()
        return {"participantes": rows}
    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        if conn:
            conn.close()
