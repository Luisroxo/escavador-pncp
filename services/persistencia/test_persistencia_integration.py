import pytest
import requests

def test_metrics():
    response = requests.get("http://localhost:8000/metrics")
    assert response.status_code == 200

def test_db():
    response = requests.get("http://localhost:8000/algum-endpoint")
    assert response.status_code in [200, 404]
    # Teste de exemplo, ajuste conforme endpoint real
