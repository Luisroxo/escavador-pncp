import requests
import pytest
from main import validar_cnpj, get_cnpj_data

def test_validar_cnpj():
    assert validar_cnpj("12345678000195") is True
    assert validar_cnpj("123") is False

def test_get_cnpj_data(mocker):
    mock_response = {
        "cnpj": "12345678000195",
        "razao_social": "Empresa Teste"
    }
    mocker.patch("requests.get", return_value=mocker.Mock(json=lambda: mock_response, status_code=200))
    data = get_cnpj_data("12345678000195")
    assert data["razao_social"] == "Empresa Teste"

def test_metrics():
    response = requests.get("http://localhost:8002/metrics")
    assert response.status_code == 200

def test_enriquecer_cnpj():
    response = requests.post("http://localhost:8002/enriquecer-cnpj/12345678000195")
    assert response.status_code in [200, 404]
