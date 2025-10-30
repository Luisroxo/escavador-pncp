import sys
import os

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import psycopg2
from fastapi import FastAPI, HTTPException
import re
from dotenv import load_dotenv
import os
import json
import requests
from services.persistencia.db_operations import update_participante_data, update_participante_contato
from prometheus_fastapi_instrumentator import Instrumentator
import logging
from typing import Optional

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST")
}
BRASILAPI_CNPJ_URL = "https://brasilapi.com.br/api/cnpj/v1/"
BRASILAPI_TIMEOUT = int(os.getenv("BRASILAPI_TIMEOUT", 10)) # Default 10 seconds


app = FastAPI()
Instrumentator().instrument(app).expose(app)

# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_cnpj_data(cnpj_clean: str) -> Optional[dict]:
    """
    Consulta a BrasilAPI para obter dados de enriquecimento de um CNPJ.

    Args:
        cnpj_clean: O CNPJ (somente números) a ser consultado.

    Returns:
        Um dicionário com os dados do CNPJ ou None em caso de erro de requisição.
    """
    try:
        logging.info(f"Consultando BrasilAPI para o CNPJ: {cnpj_clean}")
        response = requests.get(f"{BRASILAPI_CNPJ_URL}{cnpj_clean}", timeout=BRASILAPI_TIMEOUT)
        response.raise_for_status()
        logging.info("Dados recebidos da BrasilAPI com sucesso.")
        data = response.json()
        logging.debug(f"Dados retornados pela BrasilAPI: {json.dumps(data, ensure_ascii=False)}")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao consultar BrasilAPI: {e}")
        return None

def validar_cnpj(cnpj: str) -> bool:
    """
    Verifica se a string fornecida é um CNPJ ou CPF válido (11 ou 14 dígitos).

    Args:
        cnpj: A string contendo o CNPJ/CPF a ser validado.

    Returns:
        True se for válido, False caso contrário.
    """
    padrao = re.compile(r'^[0-9]{11,14}$')
    return padrao.match(cnpj) is not None

def safe_decode(data):
    """
    Decodifica strings para UTF-8 de forma segura.

    Args:
        data: A string ou bytes a ser decodificada.

    Returns:
        A string decodificada ou None em caso de erro.
    """
    try:
        if isinstance(data, bytes):
            return data.decode('utf-8')
        return data
    except UnicodeDecodeError as e:
        logging.error(f"Erro ao decodificar dados: {e}")
        return None

@app.post("/enriquecer-cnpj/{cnpj_clean}")
def enriquecer_cnpj(cnpj_clean: str):
    """
    Endpoint para enriquecer os dados de um participante (CNPJ/CPF) com informações da BrasilAPI.

    Args:
        cnpj_clean: O CNPJ (somente números) do participante.

    Returns:
        Um dicionário com a mensagem de sucesso.

    Raises:
        HTTPException: 400 se o CNPJ for inválido.
        HTTPException: 404 se o CNPJ não for encontrado na BrasilAPI ou no banco de dados.
        HTTPException: 500 se ocorrer um erro interno no banco de dados.
    """
    logging.info(f"Recebida requisição para enriquecer o CNPJ: {cnpj_clean}")
    if not validar_cnpj(cnpj_clean):
        logging.warning("CNPJ inválido ou mal formatado.")
        raise HTTPException(status_code=400, detail="CNPJ inválido ou mal formatado.")

    data = get_cnpj_data(cnpj_clean)
    logging.info(f"Dados retornados pela BrasilAPI: {data}")

    # Verifica se os dados são válidos (deve conter 'cnpj' e 'razao_social' como campos essenciais)
    if not data or "cnpj" not in data or "razao_social" not in data:
        logging.warning(f"Dados da BrasilAPI não contêm 'cnpj' ou são None. JSON: {data}")
        raise HTTPException(status_code=404, detail="Dados não encontrados ou erro na API.")

    conn = None  # Inicializar a variável conn
    try:
        logging.info(f"Tentando atualizar dados de enriquecimento para o CNPJ: {cnpj_clean}")
        conn = psycopg2.connect(**DB_CONFIG, options="-c client_encoding=UTF8")
        rows_affected = update_participante_data(conn, cnpj_clean, data)

        if rows_affected == 0:
            logging.warning(f"CNPJ {cnpj_clean} não encontrado na tabela participantes para enriquecimento.")
            raise HTTPException(status_code=404, detail=f"Participante com CNPJ {cnpj_clean} não encontrado no banco de dados.")

        logging.info(f"CNPJ {cnpj_clean} enriquecido com sucesso.")
        return {"message": f"CNPJ {cnpj_clean} enriquecido com sucesso."}
    except psycopg2.Error as error:
        logging.error(f"Erro ao atualizar o banco de dados: {error}")
        raise HTTPException(status_code=500, detail=str(error))
    except Exception as error:
        logging.error(f"Erro inesperado no enriquecimento: {error}")
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        if conn:
            conn.close()
            logging.info("Conexão com o banco de dados encerrada.")

@app.post("/atualizar-contato/{cnpj_clean}")
def atualizar_contato(cnpj_clean: str, whatsapp: str = None, redes_sociais: dict = None):
    """
    Endpoint para atualizar as informações de contato de um participante.

    Args:
        cnpj_clean: O CNPJ (somente números) do participante.
        whatsapp: Número de WhatsApp para atualização.
        redes_sociais: Dicionário com links de redes sociais.

    Returns:
        Um dicionário com a mensagem de sucesso.

    Raises:
        HTTPException: 400 se o CNPJ for inválido.
        HTTPException: 404 se o CNPJ não for encontrado no banco de dados.
        HTTPException: 500 se ocorrer um erro interno no banco de dados.
    """
    logging.info(f"Recebida requisição para atualizar contato do CNPJ: {cnpj_clean}")
    if not validar_cnpj(cnpj_clean):
        logging.warning("CNPJ inválido ou mal formatado.")
        raise HTTPException(status_code=400, detail="CNPJ inválido ou mal formatado.")

    conn = None  # Inicializar a variável conn
    try:
        conn = psycopg2.connect(**DB_CONFIG, options="-c client_encoding=UTF8")
        rows_affected = update_participante_contato(conn, cnpj_clean, whatsapp, redes_sociais)

        if rows_affected == 0:
            logging.warning(f"CNPJ {cnpj_clean} não encontrado na tabela participantes para atualização de contato.")
            raise HTTPException(status_code=404, detail=f"Participante com CNPJ {cnpj_clean} não encontrado no banco de dados.")

        return {"message": f"Contato atualizado para o CNPJ {cnpj_clean}."}
    except psycopg2.Error as error:
        logging.error(f"Erro ao atualizar o contato no banco de dados: {error}")
        raise HTTPException(status_code=500, detail=str(error))
    except Exception as error:
        logging.error(f"Erro inesperado na atualização de contato: {error}")
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        if conn:
            conn.close()
            logging.info("Conexão com o banco de dados encerrada.")

if __name__ == "__main__":
    logging.info("Iniciando testes locais para o serviço de persistência.")

    # Testar conexão com o banco de dados
    try:
        logging.info("Verificando conexão com o banco de dados...")
        conn = psycopg2.connect(**DB_CONFIG, options="-c client_encoding=UTF8")
        logging.info("Conexão com o banco de dados estabelecida com sucesso.")
        conn.close()
    except Exception as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")

    # Testar endpoint enriquecer_cnpj
    cnpj_teste = "47986478000104"  # Alterado para testar com outro CNPJ
    logging.info(f"Testando enriquecimento para o CNPJ: {cnpj_teste}")
    try:
        resultado = enriquecer_cnpj(cnpj_teste)
        logging.info(f"Resultado do enriquecimento: {resultado}")
    except HTTPException as http_err:
        logging.error(f"Erro HTTP: {http_err.detail}")
    except Exception as err:
        logging.error(f"Erro inesperado: {err}")

    logging.info("Testes locais concluídos.")
