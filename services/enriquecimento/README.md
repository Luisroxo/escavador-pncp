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