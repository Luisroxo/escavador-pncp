import psycopg2
from fastapi import FastAPI, HTTPException
import re
from dotenv import load_dotenv
import os
import json
import requests
from prometheus_fastapi_instrumentator import Instrumentator
import logging

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST")
}
BRASILAPI_CNPJ_URL = "https://brasilapi.com.br/api/cnpj/v1/"


app = FastAPI()
Instrumentator().instrument(app).expose(app)

# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_cnpj_data(cnpj_clean):
    try:
        logging.info(f"Consultando BrasilAPI para o CNPJ: {cnpj_clean}")
        response = requests.get(f"{BRASILAPI_CNPJ_URL}{cnpj_clean}", timeout=10)
        response.raise_for_status()
        logging.info("Dados recebidos da BrasilAPI com sucesso.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao consultar BrasilAPI: {e}")
        return None

def validar_cnpj(cnpj):
    padrao = re.compile(r'^[0-9]{14}$')
    return padrao.match(cnpj) is not None

@app.post("/enriquecer-cnpj/{cnpj_clean}")
def enriquecer_cnpj(cnpj_clean: str):
    logging.info(f"Recebida requisição para enriquecer o CNPJ: {cnpj_clean}")
    if not validar_cnpj(cnpj_clean):
        logging.warning("CNPJ inválido ou mal formatado.")
        raise HTTPException(status_code=400, detail="CNPJ inválido ou mal formatado.")

    data = get_cnpj_data(cnpj_clean)
    logging.info(f"Dados retornados pela BrasilAPI: {data}")

    if not data or "cnpj" not in data:
        logging.warning("Dados não encontrados ou erro na API.")
        raise HTTPException(status_code=404, detail="Dados não encontrados ou erro na API.")

    conn = None
    try:
        logging.info("Conectando ao banco de dados para atualizar informações.")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        razao_social = data.get("razao_social")
        situacao_cadastral = data.get("situacao")
        porte_empresa = data.get("porte")
        capital_social = data.get("capital_social")
        logging.info(f"Dados extraídos: Razão Social: {razao_social}, Situação: {situacao_cadastral}, Porte: {porte_empresa}, Capital Social: {capital_social}")

        cnaes = []
        cnae_principal_code = data.get("cnae_fiscal")
        cnae_principal_desc = data.get("cnae_fiscal_descricao")
        if cnae_principal_code:
            cnaes.append({
                "codigo": cnae_principal_code,
                "descricao": cnae_principal_desc,
                "principal": True
            })
        cnaes_secundarios = data.get("cnaes_secundarios", [])
        for cnae_sec in cnaes_secundarios:
            cnaes.append({
                "codigo": cnae_sec.get("codigo"),
                "descricao": cnae_sec.get("descricao"),
                "principal": False
            })
        logging.info(f"CNAEs processados: {cnaes}")

        endereco = {
            "logradouro": data.get("logradouro"),
            "numero": data.get("numero"),
            "complemento": data.get("complemento"),
            "bairro": data.get("bairro"),
            "cep": data.get("cep"),
            "municipio": data.get("municipio"),
            "uf": data.get("uf")
        }
        logging.info(f"Endereço processado: {endereco}")

        contato = {}
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
            razao_social,
            situacao_cadastral,
            porte_empresa,
            capital_social,
            json.dumps(cnaes),
            json.dumps(endereco),
            json.dumps(contato),
            cnpj_clean
        ))
        conn.commit()
        cur.close()
        logging.info(f"CNPJ {cnpj_clean} enriquecido com sucesso.")
        return {"message": f"CNPJ {cnpj_clean} enriquecido com sucesso."}
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Erro ao atualizar o banco de dados: {error}")
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        if conn:
            conn.close()
            logging.info("Conexão com o banco de dados encerrada.")

@app.post("/atualizar-contato/{cnpj_clean}")
def atualizar_contato(cnpj_clean: str, whatsapp: str = None, redes_sociais: dict = None):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        update_query = """
            UPDATE participantes SET
                whatsapp = %s,
                redes_sociais = %s
            WHERE cnpj_cpf = %s;
        """
        cur.execute(update_query, (
            whatsapp,
            json.dumps(redes_sociais) if redes_sociais else None,
            cnpj_clean
        ))
        conn.commit()
        cur.close()
        return {"message": f"Contato atualizado para o CNPJ {cnpj_clean}."}
    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        if conn:
            conn.close()
