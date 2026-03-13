# Relatório Final — Experimentação de Software (Lab01)

## Título

Características de Repositórios Populares no GitHub: Coleta, Análise e Resposta às RQs

## Autores

- Kaio Henrique Oliveira da Silveira Barbosa

## Introdução

Este projeto investigou características de repositórios populares no GitHub para responder 6 questões de pesquisa (RQs) relacionadas a maturidade, contribuição externa, releases, atualização, linguagem e fechamento de issues.

O trabalho foi dividido em 3 sprints incrementais:

- Sprint 1: coleta inicial (100 repositórios)
- Sprint 2: coleta ampliada com paginação (1000 repositórios) e exportação CSV
- Sprint 3: análise estatística, visualização e conclusões finais

---

## Questões de Pesquisa (RQs) e Hipóteses

- **RQ01**: Sistemas populares são maduros/antigos?
  - Métrica: idade do repositório
  - Hipótese: sistemas populares tendem a ser mais antigos.

- **RQ02**: Sistemas populares recebem muita contribuição externa?
  - Métrica: total de pull requests aceitas
  - Hipótese: sistemas populares têm alto volume de PRs aceitas.

- **RQ03**: Sistemas populares lançam releases com frequência?
  - Métrica: total de releases
  - Hipótese: sistemas populares publicam releases com frequência.

- **RQ04**: Sistemas populares são atualizados com frequência?
  - Métrica: tempo até a última atualização
  - Hipótese: sistemas populares apresentam atualização recente.

- **RQ05**: Sistemas populares são escritos nas linguagens mais populares?
  - Métrica: linguagem primária
  - Hipótese: predominância de linguagens amplamente adotadas.

- **RQ06**: Sistemas populares possuem alto percentual de issues fechadas?
  - Métrica: razão entre issues fechadas e issues totais
  - Hipótese: percentual de fechamento é alto.

---

## Objetivo

Construir um pipeline completo de coleta e análise para responder quantitativamente às RQs com base em dados reais da API GraphQL do GitHub.

---

## Metodologia Geral

1. Coleta inicial e validação da query (Sprint 1)
2. Escalonamento para 1000 repositórios com paginação (Sprint 2)
3. Cálculo de métricas, geração de gráficos e conclusões (Sprint 3)

---

## Sprint 1 — Lab01S01

### O que foi feito

- Implementação da primeira coleta de dados via GraphQL
- Coleta de 100 repositórios populares
- Inclusão das métricas das RQs:
  - `createdAt`, `updatedAt`
  - `pullRequests(states: MERGED)`
  - `releases`
  - `issues`, `closedIssues`
  - `primaryLanguage`
- Implementação de retry para aumentar robustez

### Dificuldades encontradas

- Erro **502 Bad Gateway** em consultas pesadas
- Erros de sintaxe GraphQL e uso de union type
- Problema de configuração no `.env`

### Soluções aplicadas

- Estratégia sem paginação por **lotes de faixas de estrelas** (10 lotes de 10)
- Correção da query com `... on Repository`
- Retry com espera entre tentativas
- Correção de formato do `.env` para `GITHUB_TOKEN=...`

### Conclusão da Sprint 1

A sprint validou a arquitetura da coleta, estabilizou a consulta e garantiu a extração das métricas necessárias em pequena escala.

---

## Sprint 2 — Lab01S02

### O que foi feito

- Implementação de **paginação com cursor**
- Coleta de **1000 repositórios**
- Exportação dos dados para CSV (`docs/Sprint2/repositorios.csv`)
- Criação de métricas derivadas:
  - `idade_dias`
  - `dias_desde_atualizacao`
  - `razao_issues_fechadas`

### Dificuldades encontradas

- Manter estabilidade em alto volume de requisições
- Limites e intermitência da API
- Padronização de dados para análise posterior

### Soluções aplicadas

- Paginação (`first: 10`, `after: cursor`)
- Retry com múltiplas tentativas e backoff
- Timeout configurado para requisições longas
- Normalização de campos para saída tabular consistente

### Conclusão da Sprint 2

A sprint entregou a base definitiva de dados (1000 repositórios) em formato estruturado, pronta para análise estatística e visualização.

---

## Sprint 3 — Lab01S03

### O que foi feito

- Implementação de script de análise (`lab01s03.py`)
- Cálculo de medidas estatísticas (mediana e média)
- Geração de gráficos em `docs/Sprint3/figures`
- Geração do relatório final em Markdown
- Resposta final das RQs

### Dificuldades encontradas

- Dependência de biblioteca para visualização (`matplotlib`)
- Definição de regras objetivas para confirmar/rejeitar hipóteses
- Garantia de consistência entre resultados numéricos e texto do relatório

### Soluções aplicadas

- Instalação e uso de `matplotlib`
- Regras explícitas de decisão por RQ (medianas/limiares)
- Automação da escrita do relatório a partir das métricas calculadas

### Resultados (RQs respondidas)

| RQ | Resultado | Resposta |
|---|---|---|
| RQ01 | Mediana de idade = 8,39 anos | Sim |
| RQ02 | Mediana de PRs merged = 739 | Sim |
| RQ03 | Mediana de releases = 40 | Sim |
| RQ04 | Mediana desde última atualização = 0 dias | Sim |
| RQ05 | Top linguagens inclui Python, TypeScript e JavaScript | Sim |
| RQ06 | Mediana da razão de issues fechadas = 87,78% | Sim |

### Conclusão da Sprint 3

A sprint finalizou o ciclo analítico do experimento, com visualizações e respostas quantitativas para todas as RQs.

---

## Discussões (Insights)

- Repositórios populares tendem a ser maduros e ativos.
- Há forte evidência de contribuição externa em escala.
- Popularidade não implica distribuição homogênea de releases; existe assimetria entre projetos.
- Linguagens dominantes confirmam tendências do ecossistema atual.
- O alto percentual de issues fechadas indica manutenção ativa na maioria dos projetos.

---

## Conclusão Final

O projeto evoluiu de coleta inicial para análise completa, com robustez técnica e rastreabilidade dos resultados. As hipóteses propostas foram sustentadas pelos dados coletados e analisados. O processo em sprints permitiu validar incrementalmente consulta, escala e interpretação, resultando em um relatório final consistente e reproduzível.

## Artefatos finais

- `lab01s01.py`
- `lab01s02.py`
- `lab01s03.py`
- `docs/Sprint2/repositorios.csv`
- `docs/Sprint3/Relatorio_Final_Sprint3.md`
- `docs/Sprint3/figures/*.png`


