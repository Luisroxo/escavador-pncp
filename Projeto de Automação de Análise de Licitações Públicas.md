# Projeto de Automação de Análise de Licitações Públicas

Este projeto implementa um fluxo de trabalho automatizado para extrair dados de CNPJ/CPF de relatórios de licitação em PDF/ZIP, armazená-los em um banco de dados PostgreSQL e enriquecê-los com informações comerciais.

## 1. Estrutura do Projeto

O fluxo de trabalho é orquestrado pelo script principal `full_process.py`, que executa as seguintes etapas:

| Arquivo | Função |
| :--- | :--- |
| `full_process.py` | Orquestrador principal. Lida com descompactação (se necessário), chama a extração, insere no DB e inicia o enriquecimento. |
| `extract_cnpj.py` | Extrai CNPJs/CPFs e classifica os participantes (`ganhador`, `licitantes`, `proponentes`) do PDF. |
| `db_setup.py` | Configura a conexão com o PostgreSQL e insere/atualiza os dados de CNPJ/CPF na tabela `participantes`. |
| `enrich_data.py` | Enriquecimento de dados: consulta a BrasilAPI para obter Razão Social, CNAE, Capital Social, Porte, Endereço e simula a busca por WhatsApp/Redes Sociais. |

## 2. Configuração do Ambiente

### 2.1. Banco de Dados PostgreSQL

O projeto utiliza um banco de dados PostgreSQL. A tabela `participantes` foi criada com a seguinte estrutura:

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `cnpj_cpf` | `VARCHAR(18)` | CNPJ/CPF limpo (apenas números). |
| `categoria` | `VARCHAR(20)` | Classificação do participante (ex: `ganhador`, `licitantes`, `proponentes`). |
| `razao_social` | `VARCHAR(255)` | Nome da empresa (obtido via API). |
| `porte_empresa` | `VARCHAR(50)` | Porte (ME, EPP, etc.). |
| `capital_social` | `NUMERIC(15, 2)` | Capital social. |
| `situacao_cadastral` | `VARCHAR(50)` | Situação na Receita Federal. |
| `cnaes` | `JSONB` | Lista de CNAEs principal e secundários. |
| `endereco` | `JSONB` | Dados de endereço completo. |
| `whatsapp` | `VARCHAR(20)` | Número de WhatsApp (requer busca/scraping). |
| `redes_sociais` | `JSONB` | Links para redes sociais (requer busca/scraping). |

**Credenciais de Conexão (padrão):**
*   **DB Name:** `licitacoes`
*   **User:** `manus`
*   **Password:** `manus123`
*   **Host:** `localhost` (ou o IP do seu servidor)

### 2.2. Enriquecimento de Dados

O enriquecimento de dados cadastrais utiliza a **BrasilAPI** (`https://brasilapi.com.br/api/cnpj/v1/{cnpj}`).

**Nota sobre Dados Comerciais:** A busca por WhatsApp e Redes Sociais é um processo complexo que requer *web scraping* e análise de resultados de busca. O script `enrich_data.py` contém um exemplo de como os dados devem ser atualizados no banco após a busca manual ou automatizada (que deve ser desenvolvida separadamente).

## 3. Guia de Integração com N8N (ou Plataforma de Automação Similar)

O fluxo de trabalho completo pode ser automatizado com o N8N, monitorando a pasta do Google Drive e executando o script Python no servidor.

### Fluxo N8N Sugerido:

| Nó | Tipo | Configuração | Ação |
| :--- | :--- | :--- | :--- |
| **1. Gatilho** | **Google Drive Trigger** | **Recurso:** Arquivo; **Operação:** Novo Arquivo Adicionado. | Monitora a pasta do Google Drive onde os relatórios (PDF/ZIP) são salvos. |
| **2. Download** | **Google Drive** | **Operação:** Download File; **ID do Arquivo:** ID do arquivo do Nó 1. | Baixa o arquivo para o ambiente de execução do N8N. |
| **3. Execução** | **Execute Command** | **Comando:** `python3 /caminho/para/full_process.py {{ $file.path }}` | Executa o script Python principal, passando o caminho do arquivo baixado como argumento. |
| **4. Notificação**| **E-mail / Telegram** | **Mensagem:** "Processamento do arquivo {{ $file.name }} concluído. {{$node["3. Execução"].json["output"]}}" | Envia notificação de sucesso ou erro. |

**Detalhe do Nó 3 (Execute Command):**

O script `full_process.py` foi projetado para aceitar o caminho do arquivo como argumento.

```python
# Exemplo de como você chamaria o script no N8N:
python3 /home/ubuntu/full_process.py /caminho/temporario/do/n8n/nome_do_arquivo.pdf
```

**Observação:** O script `full_process.py` já contém a lógica de descompactação de arquivos ZIP.

## 4. Próximos Passos (Desenvolvimento)

1.  **Ajuste da Busca de Contato:** Implementar um módulo de *web scraping* mais robusto para automatizar a busca por WhatsApp e Redes Sociais, em substituição à simulação atual no `enrich_data.py`.
2.  **Monitoramento de Erros:** Adicionar tratamento de erros mais detalhado nos scripts Python para facilitar a depuração no N8N.

Este projeto entrega o **esqueleto funcional completo** para a sua automação, cobrindo todas as etapas solicitadas: extração de CNPJs, armazenamento em PostgreSQL e enriquecimento de dados via API.
