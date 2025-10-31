# Serviço Rede Social

Este microserviço permite consultar e atualizar as redes sociais de um participante cadastrado no banco de dados.

## Endpoints

- `GET /rede-social/{cnpj_clean}`: Consulta as redes sociais do participante pelo CNPJ.
- `POST /rede-social/{cnpj_clean}`: Atualiza as redes sociais do participante pelo CNPJ.
- `GET /health`: Verifica a saúde do serviço e do banco de dados.

## Exemplo de payload para atualização
```json
{
  "instagram": "@empresa",
  "facebook": "facebook.com/empresa",
  "linkedin": "linkedin.com/in/empresa"
}
```

## Observações
- Retorna 404 se o participante não existir.
- Retorna 500 em caso de erro interno.
