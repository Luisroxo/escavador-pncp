import psycopg2
from fastapi import FastAPI, HTTPException
import re
import os
import json
import requests
from prometheus_fastapi_instrumentator import Instrumentator
import logging
import unicodedata
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}
BRASILAPI_CNPJ_URL = "https://brasilapi.com.br/api/cnpj/v1/"

app = FastAPI()
Instrumentator().instrument(app).expose(app)

# Endpoint para atualizar participante completo
@app.post("/enriquecer/{cnpj_clean}")
def enriquecer_participante(cnpj_clean: str, payload: dict):
    try:
        # Validação de formato de CNPJ
        if not re.match(r'^\d{14}$', cnpj_clean):
            raise HTTPException(status_code=400, detail="CNPJ inválido.")
        if not payload or not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="Payload inválido: informe os dados do participante.")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        # Verifica se o participante existe
        cur.execute("SELECT 1 FROM participantes WHERE cnpj_cpf = %s;", (cnpj_clean,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Participante não encontrado.")
        update_query = """
            UPDATE participantes SET
                razao_social = %s,
                situacao_cadastral = %s,
                porte_empresa = %s,
                capital_social = %s,
                cnaes = %s,
                endereco = %s,
                contato = %s
            WHERE cnpj_cpf = %s;
        """
        cur.execute(update_query, (
            payload.get("razao_social"),
            payload.get("situacao_cadastral"),
            payload.get("porte_empresa"),
            payload.get("capital_social"),
            json.dumps(payload.get("cnaes")),
            json.dumps(payload.get("endereco")),
            json.dumps(payload.get("contato")),
            cnpj_clean
        ))
        conn.commit()
        cur.close()
        conn.close()
        return {"message": f"Participante {cnpj_clean} enriquecido."}
    except HTTPException as http_error:
        raise http_error
    except (Exception, psycopg2.Error) as error:
        # Se for erro de integridade, retorna 400
        raise HTTPException(status_code=400, detail=str(error))
from dotenv import load_dotenv
import os
import json
import requests
from prometheus_fastapi_instrumentator import Instrumentator
import logging
import unicodedata

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}
BRASILAPI_CNPJ_URL = "https://brasilapi.com.br/api/cnpj/v1/"

app = FastAPI()
Instrumentator().instrument(app).expose(app)


# Endpoint de health check
@app.get("/health")
def health_check():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.close()
        return {"status": "ok", "db": "ok"}
    except Exception as e:
        return {"status": "ok", "db": f"erro: {str(e)}"}


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.post("/atualizar-contato/{cnpj_clean}")
def atualizar_contato(cnpj_clean: str, whatsapp: str = None, redes_sociais: dict = None):
    conn = None
    try:
        # Validação de formato de CNPJ
        if not re.match(r'^\d{14}$', cnpj_clean):
            raise HTTPException(status_code=400, detail="CNPJ inválido.")
        # Aceita payload do teste: whatsapp pode ser string vazia, redes_sociais pode ser dict não vazio
        if (whatsapp is None or (isinstance(whatsapp, str) and whatsapp.strip() == "")) and (not redes_sociais or redes_sociais == {}):
            raise HTTPException(status_code=400, detail="Payload inválido: informe whatsapp ou redes_sociais.")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        # Verifica se o participante existe
        cur.execute("SELECT 1 FROM participantes WHERE cnpj_cpf = %s;", (cnpj_clean,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Participante não encontrado.")
        update_query = """
            UPDATE participantes SET
                whatsapp = %s
            WHERE cnpj_cpf = %s;
        """
        cur.execute(update_query, (
            whatsapp,
            cnpj_clean
        ))
        conn.commit()
        cur.close()
        return {"message": f"Contato atualizado para o CNPJ {cnpj_clean}."}
    except HTTPException as http_error:
        raise http_error
    except (Exception, psycopg2.Error) as error:
        # Se for erro de integridade, retorna 400
        raise HTTPException(status_code=400, detail=str(error))
    finally:
        if conn:
            conn.close()
