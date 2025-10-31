# Roadmap do Serviço de Enriquecimento

## Objetivo
Este roadmap detalha as etapas de desenvolvimento e melhorias planejadas para o serviço de enriquecimento, que utiliza a BrasilAPI para obter informações detalhadas sobre CNPJs e atualizá-las no banco de dados.

---

## Etapas

### 1. **Validação e Tratamento de Dados**
- [x] Implementar validação completa de CNPJs, incluindo verificação de dígitos verificadores.
- [x] Garantir que todos os campos esperados na resposta da BrasilAPI sejam tratados adequadamente.
- [x] Adicionar tratamento de erros mais robusto para falhas na API e no banco de dados.

### 2. **Testes e Cobertura**
- [x] Criar testes unitários para as funções principais, como `get_cnpj_data` e `validar_cnpj`.
- [x] Simular respostas da BrasilAPI para cenários de sucesso e erro.

### 3. **Monitoramento e Métricas**
- [x] Adicionar métricas Prometheus para monitorar requisições, tempos de resposta e taxas de erro.
- [x] Configurar alertas para falhas recorrentes.

### 4. **Documentação**
- [x] Documentar o endpoint `/enriquecer-cnpj/{cnpj_clean}` com exemplos de requisição e resposta.

### 5. **Processamento em Lote**
- [x] Implementar fila de processamento para CNPJs utilizando RabbitMQ.

### 6. **Logs e Depuração**
- [x] Adicionar logs detalhados para rastrear o fluxo de execução e facilitar a depuração.

---

## Conclusão
Este roadmap foi concluído com sucesso. O serviço de enriquecimento está robusto, eficiente e fácil de manter.