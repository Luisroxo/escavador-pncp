import pytest
from fastapi.testclient import TestClient
from services.enriquecimento.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "db" in response.json()

def test_enriquecer_cnpj_update():
    cnpj = "53836509000135"
    response = client.post(f"/enriquecer-cnpj/{cnpj}")
    assert response.status_code in [200, 404]  # 200 se existe, 404 se não existe

def test_atualizar_contato():
    cnpj = "53836509000135"
    payload = {"whatsapp": "11999999999", "redes_sociais": {"instagram": "@empresa"}}
    response = client.post(f"/atualizar-contato/{cnpj}", json=payload)
    assert response.status_code in [200, 404]  # 200 se existe, 404 se não existe

def test_enriquecer_cnpj_invalido():
    cnpj = "00000000000000"
    response = client.post(f"/enriquecer-cnpj/{cnpj}")
    assert response.status_code == 400

def test_atualizar_contato_invalido():
    cnpj = "00000000000000"
    payload = {"whatsapp": "", "redes_sociais": {}}
    response = client.post(f"/atualizar-contato/{cnpj}", json=payload)
    assert response.status_code == 400
