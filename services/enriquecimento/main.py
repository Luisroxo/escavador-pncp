import requests
import json
import psycopg2
from fastapi import FastAPI, HTTPException

DB_CONFIG = {
    "dbname": "licitacoes",
    "user": "manus",
    "password": "manus123",
    "host": "postgres"
}
BRASILAPI_CNPJ_URL = "https://brasilapi.com.br/api/cnpj/v1/"

app = FastAPI()

def get_cnpj_data(cnpj_clean):
    try:
        response = requests.get(f"{BRASILAPI_CNPJ_URL}{cnpj_clean}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None

@app.post("/enriquecer-cnpj/{cnpj_clean}")
def enriquecer_cnpj(cnpj_clean: str):
    data = get_cnpj_data(cnpj_clean)
    if not data or "cnpj" not in data:
        raise HTTPException(status_code=404, detail="Dados não encontrados ou erro na API.")
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        razao_social = data.get("razao_social")
        situacao_cadastral = data.get("situacao")
        porte_empresa = data.get("porte")
        capital_social = data.get("capital_social")
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
        endereco = {
            "logradouro": data.get("logradouro"),
            "numero": data.get("numero"),
            "complemento": data.get("complemento"),
            "bairro": data.get("bairro"),
            "cep": data.get("cep"),
            "municipio": data.get("municipio"),
            "uf": data.get("uf")
        }
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
        return {"message": f"CNPJ {cnpj_clean} enriquecido com sucesso."}
    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        if conn:
            conn.close()

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
