import pdfplumber
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
import os

from prometheus_fastapi_instrumentator import Instrumentator

import re

app = FastAPI()
Instrumentator().instrument(app).expose(app)

@app.post("/extrair-cnpjs")
def extrair_cnpjs(file: UploadFile = File(...)):
    """Recebe um PDF via upload, extrai e classifica CNPJs/CPFs."""
    try:
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(file.file.read())
        resultado = extract_cnpjs_from_pdf(temp_path)
        os.remove(temp_path)
        if resultado:
            return resultado
        else:
            raise HTTPException(status_code=400, detail="Falha na extração de dados do PDF.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_cnpjs_from_pdf(pdf_path):
    cnpjs = {
        "ganhador": set(),
        "licitantes": set(),
        "proponentes": set()
    }
    cnpj_cpf_pattern = re.compile(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{3}\.\d{3}\.\d{3}-\d{2})')
    cnpj_simples_pattern = re.compile(r'(\d{14})')
    ganhador_pattern = re.compile(r'Aceito e Habilitado por .*?CNPJ\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', re.IGNORECASE)
    all_proponentes = set()
    all_licitantes = set()
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue
                match_ganhador = ganhador_pattern.search(text)
                if match_ganhador:
                    cnpjs["ganhador"].add(match_ganhador.group(1))
                for match in cnpj_cpf_pattern.finditer(text):
                    cnpj_or_cpf = match.group(1)
                    if cnpj_or_cpf not in cnpjs["ganhador"]:
                        all_proponentes.add(cnpj_or_cpf)
                if "Lances do Item" in text:
                    for match in cnpj_cpf_pattern.finditer(text):
                        cnpj_or_cpf = match.group(1)
                        all_licitantes.add(cnpj_or_cpf)
        cnpjs["licitantes"] = all_licitantes - cnpjs["ganhador"]
        cnpjs["proponentes"] = all_proponentes - all_licitantes
        for key in cnpjs:
            cnpjs[key] = list(cnpjs[key])
    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")
        return None
    return cnpjs
