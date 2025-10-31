# Serviço de Enriquecimento

Integra com APIs públicas e realiza scraping para enriquecer os dados dos participantes.

## Funcionalidades
- Validação de CNPJs.
- Consulta à BrasilAPI para obter dados cadastrais.
- Atualização de informações no banco de dados PostgreSQL.

## Configuração
1. Certifique-se de que as dependências estão instaladas:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure as variáveis de ambiente no arquivo `.env`:
   ```env
   POSTGRES_DB=licitacoes
   POSTGRES_USER=luis
   POSTGRES_PASSWORD=senha
   POSTGRES_HOST=localhost
   ```

## Execução
Para iniciar o serviço, execute:
```bash
uvicorn main:app --host 0.0.0.0 --port 8002
```

## Documentação do Endpoint `/enriquecer-cnpj/{cnpj_clean}`

### Descrição
Este endpoint permite enriquecer os dados de um CNPJ consultando a BrasilAPI e atualizando as informações no banco de dados.

### Método HTTP
`POST`

### URL
`/enriquecer-cnpj/{cnpj_clean}`

### Parâmetros
- **cnpj_clean** (string): CNPJ sem formatação (apenas números).

### Exemplo de Requisição
```http
POST /enriquecer-cnpj/12345678000195 HTTP/1.1
Host: localhost:8000
Content-Type: application/json
```

### Exemplo de Resposta Sucesso (200)
```json
{
  "message": "CNPJ 12345678000195 enriquecido com sucesso."
}
```

### Exemplo de Resposta Erro (400)
```json
{
  "detail": "CNPJ inválido ou mal formatado."
}
```

### Exemplo de Resposta Erro (404)
```json
{
  "detail": "Dados não encontrados ou erro na API."
}
```

### Exemplo de Resposta Erro (500)
```json
{
  "detail": "Erro ao atualizar o banco de dados."
}
```

### Notas
- Certifique-se de que o CNPJ fornecido é válido.
- O serviço depende da disponibilidade da BrasilAPI e do banco de dados configurado.