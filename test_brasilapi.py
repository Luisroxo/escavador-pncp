import requests

def testar_brasilapi(cnpj):
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print("Resposta da API BrasilAPI:")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print("Erro ao acessar a BrasilAPI:", e)

if __name__ == "__main__":
    cnpj = input("Digite o CNPJ para testar na BrasilAPI: ")
    testar_brasilapi(cnpj)