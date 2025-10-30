# Roadmap do Serviço de Enriquecimento

## Objetivo
Este roadmap detalha as etapas de desenvolvimento e melhorias planejadas para o serviço de enriquecimento, que utiliza a BrasilAPI para obter informações detalhadas sobre CNPJs e atualizá-las no banco de dados.

---

## Etapas

### 1. **Validação e Tratamento de Dados**
- [ ] Implementar validação completa de CNPJs, incluindo verificação de dígitos verificadores.
- [ ] Garantir que todos os campos esperados na resposta da BrasilAPI sejam tratados adequadamente.
- [ ] Adicionar tratamento de erros mais robusto para falhas na API e no banco de dados.

### 2. **Testes Automatizados**
- [ ] Criar testes unitários para as funções `get_cnpj_data` e `validar_cnpj`.
- [ ] Simular respostas da BrasilAPI para testar diferentes cenários (sucesso, erro 404, erro 500).
- [ ] Desenvolver testes de integração para o endpoint `/enriquecer-cnpj/{cnpj_clean}`.

### 3. **Monitoramento e Observabilidade**
- [ ] Adicionar métricas Prometheus para monitorar:
  - Número de requisições à BrasilAPI.
  - Tempo de resposta da API.
  - Taxa de erros.
- [ ] Configurar alertas para falhas recorrentes na consulta à BrasilAPI ou no banco de dados.

### 4. **Otimizações**
- [ ] Usar um pool de conexões para o banco de dados para melhorar o desempenho.
- [ ] Configurar timeouts adequados para consultas à BrasilAPI e operações no banco.
- [ ] Implementar tentativas automáticas (retry) em caso de falha na consulta à BrasilAPI.

### 5. **Documentação**
- [ ] Documentar o endpoint `/enriquecer-cnpj/{cnpj_clean}` com exemplos de requisição e resposta.
- [ ] Atualizar o `README.md` com instruções detalhadas de configuração e execução do serviço.

### 6. **Funcionalidades Futuras**
- [ ] Integrar outras APIs públicas para enriquecer os dados com informações adicionais.
- [ ] Implementar fila de processamento (RabbitMQ ou Redis) para processar CNPJs em lote.
- [ ] Adicionar suporte para enriquecimento de dados de CPFs.

---

## Conclusão
Este roadmap será atualizado conforme novas necessidades e prioridades forem identificadas. O objetivo é garantir que o serviço de enriquecimento seja robusto, eficiente e fácil de manter.