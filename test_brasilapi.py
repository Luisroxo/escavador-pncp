import pytest
import requests

@pytest.fixture
def cnpj():
    return "47986478000104"

def testar_brasilapi(cnpj):
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print("Resposta da API BrasilAPI:")
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Erro ao acessar a BrasilAPI:", e)
        return None

def test_brasilapi(cnpj):
    resultado = testar_brasilapi(cnpj)
    assert resultado is not None, "A resposta da API BrasilAPI está vazia."

if __name__ == "__main__":
    cnpj = "47986478000104"
    resultado = testar_brasilapi(cnpj)
    if resultado:
        print("Dados recebidos:", resultado)
    else:
        print("Falha ao obter dados da API BrasilAPI.")