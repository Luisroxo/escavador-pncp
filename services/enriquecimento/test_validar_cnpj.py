import pytest
from main import validar_cnpj, get_cnpj_data

def test_validar_cnpj():
    # Teste de CNPJs válidos
    assert validar_cnpj("11222333000181") is True
    assert validar_cnpj("12345678000195") is True

    # Teste de CNPJs inválidos
    assert validar_cnpj("11222333000182") is False  # Dígito verificador incorreto
    assert validar_cnpj("123") is False  # Muito curto
    assert validar_cnpj("abc12345678000195") is False  # Contém letras

def test_get_cnpj_data(mocker):
    # Simular resposta da BrasilAPI
    mock_response = {
        "cnpj": "12345678000195",
        "razao_social": "Empresa Teste",
        "situacao": "ATIVA",
        "porte": "ME",
        "capital_social": "50000.00",
        "cnae_fiscal": "6201501",
        "cnae_fiscal_descricao": "Desenvolvimento de programas de computador sob encomenda",
        "logradouro": "Rua Teste",
        "numero": "123",
        "bairro": "Centro",
        "cep": "12345678",
        "municipio": "Cidade Teste",
        "uf": "SP"
    }

    mocker.patch("requests.get", return_value=mocker.Mock(json=lambda: mock_response, status_code=200))

    # Testar função get_cnpj_data
    data = get_cnpj_data("12345678000195")
    assert data["razao_social"] == "Empresa Teste"
    assert data["situacao"] == "ATIVA"
    assert data["porte"] == "ME"