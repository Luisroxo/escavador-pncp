# Serviço Enriquecimento

Este microserviço é responsável por enriquecer os dados de participantes já existentes no banco de dados, além de atualizar o contato (whatsapp).

## Endpoints

- `POST /enriquecer/{cnpj_clean}`: Atualiza os dados de um participante existente. Não realiza INSERT ou DELETE.
- `POST /atualizar-contato/{cnpj_clean}`: Atualiza apenas o campo whatsapp do participante.
- `GET /health`: Verifica a saúde do serviço e do banco de dados.

## Observações
- O serviço **não** manipula redes sociais. Para isso, utilize o microserviço `rede_social`.
- Retorna 404 se o participante não existir.
- Retorna 400 para payload inválido ou CNPJ mal formatado.
- Retorna 500 em caso de erro interno.

## Exemplo de payload para enriquecimento
```json
{
  "razao_social": "Empresa Exemplo",
  "situacao_cadastral": "Ativa",
  "porte_empresa": "ME",
  "capital_social": 100000,
  "cnaes": ["6201-5/01", "6202-3/00"],
  "endereco": {
    "logradouro": "Rua Exemplo",
    "numero": "123",
    "bairro": "Centro",
    "cep": "12345678",
    "municipio": "Cidade",
    "uf": "SP"
  },
  "contato": {
    "email": "contato@empresa.com",
    "telefone": "11999999999"
  }
}
```

## Exemplo de payload para contato
```json
{
  "whatsapp": "11999999999"
}
```

## Monitoramento
- Métricas Prometheus disponíveis via instrumentação automática.

## Testes
- Testes automatizados disponíveis em `test_endpoints.py`.