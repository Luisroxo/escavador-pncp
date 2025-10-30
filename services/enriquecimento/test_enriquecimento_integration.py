import requests

def test_metrics():
    response = requests.get("http://localhost:8002/metrics")
    assert response.status_code == 200

def test_enriquecimento():
    # Teste de exemplo, ajuste conforme endpoint real
    pass
