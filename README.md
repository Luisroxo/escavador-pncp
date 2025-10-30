## Monitoramento de Métricas (Prometheus & Grafana)

### 1. Serviços adicionados ao docker-compose
- Prometheus: coleta métricas dos microserviços
- Grafana: visualização dos dashboards

### 2. Configuração do Prometheus
- Arquivo: `monitor/prometheus.yml`
- Scrape dos serviços: persistencia (porta 8000), extracao (8001), enriquecimento (8002)

### 3. Subindo o ambiente
```powershell
docker compose up -d prometheus grafana
```

### 4. Acessando os dashboards
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (login padrão: admin/admin)

### 5. Próximos passos
- Expor endpoint `/metrics` nos microserviços (FastAPI: starlette_exporter ou prometheus_fastapi_instrumentator)
- Criar dashboards customizados no Grafana
## Checklist de Troubleshooting

### Containers não sobem
- Verifique se as portas estão livres (`netstat -ano | findstr LISTENING`).
- Confira se há erros de sintaxe no docker-compose.yml.
- Execute `docker compose logs <servico>` para detalhes.

### Banco de dados não conecta
- Verifique variáveis de ambiente (DB_URL, usuário, senha, host, porta).
- Teste conexão manual com `psql` ou via script Python.
- Confira se o volume está montado corretamente.

### Rede interna não funciona
- Teste com `ping <servico>` dentro dos containers.
- Verifique nomes dos serviços no docker-compose.yml.
- Reinicie containers após rebuild das imagens.

### Permissões e persistência
- Verifique permissões do volume e usuário do banco.
- Realize backup antes de alterações críticas.

### Logs e monitoramento
- Use `docker compose logs <servico>` para investigar problemas.
- Integre com Prometheus, Grafana ou ELK Stack para monitoramento avançado.

### CI/CD falha
- Confira variáveis de ambiente e secrets no pipeline.
- Valide dependências e versões de Python/Docker.

### Outros problemas
- Consulte a documentação oficial do Docker, FastAPI, PostgreSQL e ferramentas utilizadas.
## Volumes, Backup e Segurança do PostgreSQL

### Configuração de Volumes
O volume `pgdata` garante persistência dos dados do banco mesmo após reinicialização dos containers.
Exemplo no docker-compose:
```yaml
volumes:

	# Roadmap

	Todas as tarefas principais do projeto foram concluídas:

	- [x] Finalizar scripts de build dos microserviços
	- [x] Documentar padrão DB_URL
	- [x] Remover atributo version do docker-compose.yml
	- [x] Criar templates de deploy para produção
	- [x] Configurar CI/CD
	- [x] Implementar pipeline automatizado
	- [x] Documentar variáveis sensíveis
	- [x] Criar scripts de inicialização/shutdown
	- [x] Testar reinicialização e persistência
	- [x] Documentar processo de subida dos containers
	- [x] Validar logs dos containers
	- [x] Testar rede interna do Docker Compose
	- [x] Testar integração entre microserviços e banco
	- [x] Revisar permissões dos volumes
	- [x] Criar checklist de troubleshooting

	## Próximos passos sugeridos

	- Monitoramento avançado (Prometheus, Grafana, ELK)
	- Testes automatizados de integração e carga
	- Auditoria de segurança contínua
	- Evolução dos microserviços (novas features, refatoração)
	- Deploy automatizado em ambiente cloud

	Consulte o checklist de troubleshooting para resolução rápida de problemas.
2. Execute o teste de integração no serviço persistencia:
	```powershell
	docker compose exec persistencia python main.py --test-db
	```
Se o serviço conectar ao banco e não retornar erro, a integração está funcionando!
## Teste da Rede Interna do Docker Compose

Para garantir que os serviços se comunicam pela rede interna do Docker Compose:

1. Certifique-se que os containers estão rodando:
	```powershell
	./start.ps1
	```
2. Execute o teste de comunicação entre serviços (exemplo: persistencia para enriquecimento):
	```powershell
	docker compose exec persistencia ping -c 2 enriquecimento
	```
Se o ping retornar resposta, a rede interna está funcionando corretamente!
## Logs dos Containers

Para visualizar os logs de cada serviço:
```powershell
docker compose logs <nome-do-servico>
```
Exemplo:
```powershell
docker compose logs persistencia
```

Para monitoramento avançado, integre com ferramentas como Prometheus, Grafana ou ELK Stack.

Você pode redirecionar logs para arquivos usando:
```powershell
docker compose logs <nome-do-servico> > logs/<nome-do-servico>.log
```

Consulte a documentação das ferramentas de monitoramento para integração completa.
## Processo de Subida e Atualização dos Containers

### Subir todos os serviços
```powershell
./start.ps1
```

### Derrubar todos os serviços
```powershell
./stop.ps1
```

### Atualizar imagens e containers
Se modificar o código ou Dockerfile de algum serviço, execute:
```powershell
docker compose build
./stop.ps1
./start.ps1
```

### Verificar status dos containers
```powershell
docker compose ps
```

### Logs dos containers
```powershell
docker compose logs <nome-do-servico>
```

Consulte o checklist de troubleshooting para dicas de resolução de problemas.
## Teste de Reinicialização e Persistência do Banco

Para garantir que os dados do PostgreSQL persistem após reinicialização dos containers:

1. Suba os containers:
	```powershell
	.\start.ps1
	```
2. Insira um dado de teste no banco:
	```powershell
	docker exec -it escavador-pncp-postgres-1 psql -U luis -d licitacoes -c "CREATE TABLE IF NOT EXISTS teste_persistencia (id SERIAL PRIMARY KEY, valor TEXT); INSERT INTO teste_persistencia (valor) VALUES ('persistencia_ok');"
	```
3. Derrube os containers:
	```powershell
	.\stop.ps1
	```
4. Suba novamente os containers:
	```powershell
	.\start.ps1
	```
5. Verifique se o dado persiste:
	```powershell
	docker exec -it escavador-pncp-postgres-1 psql -U luis -d licitacoes -c "SELECT * FROM teste_persistencia;"
	```
Se o dado aparecer, a persistência está funcionando corretamente!
## Variáveis Sensíveis e Segredos

Utilize o arquivo `.env` para definir variáveis sensíveis como credenciais de banco, tokens de APIs e chaves secretas.

Nunca faça commit do arquivo `.env` com dados reais. Use o `.env.example` como referência para novos desenvolvedores.

Exemplo de variáveis:
```
DB_URL=postgresql://usuario:senha@host:porta/banco
GOOGLE_DRIVE_API_KEY=your_google_drive_api_key
BRASILAPI_TOKEN=your_brasilapi_token
RECEITAWS_TOKEN=your_receitaws_token
SECRET_KEY=your_secret_key
```

Para produção, utilize mecanismos de secrets do Docker, Kubernetes ou GitHub Secrets.
# escavador-pncp

# Projeto de Microserviços para Análise de Licitações Públicas

Estrutura inicial do projeto, com diretórios para cada serviço e arquivos de configuração. Consulte o roadmap e escopo para detalhes das funcionalidades.

## Padrão de Conexão com Banco de Dados (DB_URL)

Todos os microserviços utilizam a variável de ambiente `DB_URL` para conectar ao PostgreSQL.

**Exemplo de configuração:**

```
DB_URL=postgresql://luis:020646Juan@postgres:5432/licitacoes
```

**Parâmetros:**
- `luis`: usuário do banco
- `020646Juan`: senha do banco
- `postgres`: nome do serviço do banco no docker-compose
- `5432`: porta interna do container PostgreSQL
- `licitacoes`: nome do banco de dados

**Como usar:**
- No docker-compose, já está configurado para cada serviço.
- Se rodar localmente, ajuste o host para `localhost` ou `host.docker.internal` e a porta conforme o mapeamento.

**Exemplo para acesso local:**
```
DB_URL=postgresql://luis:020646Juan@host.docker.internal:5434/licitacoes
```

Documente e utilize sempre o padrão DB_URL para facilitar integração e manutenção dos serviços.
