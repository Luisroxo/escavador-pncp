import requests

def test_metrics():
	response = requests.get("http://localhost:8001/metrics")
	assert response.status_code == 200

def test_extracao():
	# Teste de exemplo, ajuste conforme endpoint real
	pass
import requests

def test_metrics():
	response = requests.get("http://localhost:8001/metrics")
	assert response.status_code == 200

def test_extracao():
	# Teste de exemplo, ajuste conforme endpoint real
	pass
