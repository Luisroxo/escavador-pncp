# Escopo e Requisitos do Projeto

## Objetivo
Automatizar a análise de licitações públicas, extraindo, enriquecendo e organizando dados de participantes a partir de arquivos PDF/ZIP, integrando com banco de dados e APIs públicas, e disponibilizando visualizações e relatórios.

## Funcionalidades Principais
- Ingestão de arquivos (upload manual ou integração com Google Drive)
- Extração de CNPJs/CPFs e classificação dos participantes
- Persistência dos dados em banco relacional (PostgreSQL)
- Enriquecimento dos dados via APIs públicas e scraping
- Orquestração do fluxo entre microserviços
- Automação e monitoramento de uploads
- Visualização e geração de relatórios
- Segurança, autenticação e autorização
- Observabilidade e monitoramento
- Testes automatizados e documentação
- Deploy escalável e auditoria de segurança

## Stacks e Ferramentas
- **Backend:** Python (FastAPI, Celery, SQLAlchemy)
- **Banco de Dados:** PostgreSQL
- **Mensageria:** RabbitMQ, Redis Streams
- **Automação:** N8N, Zapier, Make
- **Monitoramento:** Prometheus, Grafana, ELK Stack
- **Segurança:** Auth0, Keycloak, OAuth2/JWT, Snyk, Trivy
- **API Gateway:** Kong, NGINX, Traefik
- **Documentação:** Swagger/OpenAPI
- **Visualização:** Dash, Streamlit, Power BI, Tableau
- **Infraestrutura:** Docker, Kubernetes
- **CI/CD:** GitHub Actions, GitLab CI, Jenkins

## Regras de Negócio
- Apenas arquivos PDF ou ZIP são processados.
- Participantes são classificados em ganhador, licitantes e proponentes.
- Dados enriquecidos devem incluir razão social, situação cadastral, porte, capital social, CNAEs, endereço, contato e redes sociais.
- Processamento deve ser assíncrono e escalável.
- Segurança e autenticação obrigatórias para APIs sensíveis.
- Logs e métricas devem ser centralizados para monitoramento.

## Restrições Técnicas
- O sistema deve ser containerizado (Docker) e orquestrado por Kubernetes.
- Comunicação entre microserviços via APIs REST ou filas de mensagens.
- Integração com Google Drive deve ser automatizada.
- Deploy e escalabilidade devem ser testados antes do Go Live.

---

Se quiser adicionar requisitos específicos, regras de negócio ou restrições, posso complementar este documento!