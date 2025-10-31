import os
import json
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}

app = FastAPI()

@app.get("/health")
def health_check():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.close()
        return {"status": "ok", "db": "ok"}
    except Exception as e:
        return {"status": "ok", "db": f"erro: {str(e)}"}

@app.get("/rede-social/{cnpj_clean}")
def get_rede_social(cnpj_clean: str):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT redes_sociais FROM participantes WHERE cnpj_cpf = %s;", (cnpj_clean,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Participante não encontrado.")
        return {"redes_sociais": row[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rede-social/{cnpj_clean}")
def update_rede_social(cnpj_clean: str, redes_sociais: dict):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM participantes WHERE cnpj_cpf = %s;", (cnpj_clean,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Participante não encontrado.")
        update_query = """
            UPDATE participantes SET redes_sociais = %s WHERE cnpj_cpf = %s;
        """
        cur.execute(update_query, (json.dumps(redes_sociais), cnpj_clean))
        conn.commit()
        cur.close()
        conn.close()
        return {"message": f"Redes sociais atualizadas para o CNPJ {cnpj_clean}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
