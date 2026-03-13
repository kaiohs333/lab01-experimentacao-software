📊 Características de Repositórios Populares no GitHub

Python | GraphQL | Engenharia de Software

Projeto acadêmico desenvolvido para a disciplina de Experimentação de Software, com o objetivo de investigar características estruturais e evolutivas de sistemas open-source populares hospedados no GitHub.

📖 Índice

•📌 Contexto do Projeto

•🎯 Questões de Pesquisa (RQs)

•🧠 Hipóteses Iniciais

•🛠️ Metodologia – Sprint 1 (Lab01S01)

•🔎 Implementação Técnica

•⚠️ Problemas Encontrados e Soluções

•🚀 Como Executar o Projeto

•📂 Estrutura do Projeto

•📈 Próximas Sprints

•👨‍💻 Autor

📌 Contexto do Projeto

Sistemas open-source populares desempenham papel central na indústria de software. Este projeto tem como objetivo investigar as principais características desses sistemas, analisando aspectos como:

    •Maturidade

    •Frequência de atualização

    •Contribuição externa

    •Lançamento de releases

    •Linguagem de programação

    •Taxa de fechamento de issues

O estudo será realizado sobre os 1.000 repositórios com maior número de estrelas no GitHub, sendo dividido em três sprints incrementais.

Esta versão corresponde à Sprint 1 (Lab01S01).

🎯 Questões de Pesquisa (RQs)

•RQ01. Sistemas populares são maduros/antigos?
    → Métrica: idade do repositório (data de criação)

•RQ02. Sistemas populares recebem muita contribuição externa?
    → Métrica: total de pull requests aceitas

•RQ03. Sistemas populares lançam releases com frequência?
    → Métrica: total de releases

•RQ04. Sistemas populares são atualizados com frequência?
    → Métrica: tempo desde a última atualização

•RQ05. Sistemas populares são escritos nas linguagens mais populares?
    → Métrica: linguagem primária

•RQ06. Sistemas populares possuem alto percentual de issues fechadas?
    → Métrica: razão entre número de issues fechadas e total de issues

🧠 Hipóteses Iniciais

Antes da coleta dos dados, foram formuladas hipóteses informais:

    •Sistemas populares tendem a ser mais antigos (maior maturidade).

    •Projetos populares recebem maior volume de contribuições externas.

    •Projetos populares lançam releases com maior frequência.

    •Projetos populares apresentam atualizações recentes.

    •Linguagens amplamente adotadas (ex.: JavaScript, Python, Java) devem ser predominantes.

    •Projetos populares tendem a manter um alto percentual de issues fechadas.

Essas hipóteses serão validadas nas próximas sprints.

🛠️ Metodologia – Sprint 1 (Lab01S01)

Objetivo da Sprint 1

Implementar uma consulta GraphQL para coletar dados de 100 repositórios populares, incluindo todas as métricas necessárias para responder às RQs, utilizando requisição automática via Python.

Estratégia adotada

•Uso da API GraphQL do GitHub

•Autenticação via token pessoal

•Requisição automática com Python (requests)

•**Busca por lotes usando faixas de estrelas** (sem paginação)

•Mecanismo de **retry automático** com backoff

•Coleta das seguintes métricas:

    •createdAt

    •updatedAt

    •stargazerCount

    •pullRequests(states: MERGED)

    •releases

    •issues

    •issues(states: CLOSED)

    •primaryLanguage



**Estratégia de Busca por Faixas de Estrelas**

Devido a limitações da API (erro 502), foi implementada uma estratégia de busca em **10 lotes de 10 repositórios**, cada um filtrando por uma faixa específica de estrelas:

| Lote | Faixa de Estrelas |
|------|-------------------|
| 1 | ≥ 200.000 |
| 2 | 150.000 - 199.999 |
| 3 | 120.000 - 149.999 |
| 4 | 100.000 - 119.999 |
| 5 | 85.000 - 99.999 |
| 6 | 70.000 - 84.999 |
| 7 | 60.000 - 69.999 |
| 8 | 50.000 - 59.999 |
| 9 | 45.000 - 49.999 |
| 10 | 40.000 - 44.999 |

A consulta foi estruturada utilizando o filtro:

        stars:>10000 sort:stars-desc

🔎 Implementação Técnica

A requisição é realizada via:

        Python


        requests.post(
            "https://api.github.com/graphql",
            json={"query": QUERY_100_REPOS},
            headers=headers
        )



A consulta utiliza Inline Fragment, pois o campo search retorna um tipo Union (SearchResultItem).

Estrutura principal da query:

        query {
        search(query: "stars:>10000 sort:stars-desc", type: REPOSITORY, first: 100) {
            nodes {
            ... on Repository {
                nameWithOwner
                createdAt
                updatedAt
                primaryLanguage {
                name
                }
                pullRequests(states: MERGED) {
                totalCount
                }
                releases {
                totalCount
                }
                issues {
                totalCount
                }
                closedIssues: issues(states: CLOSED) {
                totalCount
                }
            }
            }
        }
        }



⚠️ Problemas Encontrados e Soluções

1️⃣ Erro 502 (Bad Gateway) - PRINCIPAL DESAFIO

Ao solicitar 100 repositórios com múltiplas métricas aninhadas (especialmente `pullRequests(states: MERGED)`), a API retornava consistentemente:

        502 Bad Gateway

Causa:

Alta complexidade da query - a API GraphQL do GitHub não consegue processar 100 repositórios com campos complexos de uma vez.

Tentativas que NÃO funcionaram:

→ Aumentar timeout e número de retries

→ Simplificar a query removendo campos (não era permitido pelo escopo do projeto)

→ Usar paginação com cursor (não era permitido pelo escopo do projeto)

✅ Solução Final Implementada:

→ **Busca por faixas de estrelas**: Dividir a busca em 10 lotes de 10 repositórios cada, usando filtros de estrelas diferentes para cada lote (ex: `stars:>=200000`, `stars:150000..199999`, etc.)

→ **Mecanismo de retry**: 10 tentativas por lote com delay linear (5s, 10s, 15s...)

→ **Timeout aumentado**: 120 segundos por requisição

→ **Pausa entre lotes**: 2 segundos para evitar rate limit

2️⃣ Erro de Sintaxe GraphQL

Erro retornado:

        Expected NAME, actual: ("\n")

Causa:

→ Chaves {} não fechadas corretamente.

Solução:

→ Reestruturação da query garantindo fechamento adequado dos blocos.

3️⃣ Erro de Union Type

Erro retornado:

        Selections can't be made directly on unions

Causa:

→ Tentativa de acessar campos diretamente em um tipo Union.

Solução:

→ Uso de Inline Fragment:

        ... on Repository

4️⃣ Erro no arquivo .env

Erro retornado:

        python-dotenv could not parse statement starting at line 1

Causa:

→ Formato incorreto no arquivo `.env` (uso de `:` em vez de `=`).

Solução:

→ Corrigir para o formato correto: `GITHUB_TOKEN=seu_token_aqui`

🚀 Como Executar o Projeto

Pré-requisitos

•Python 3.x

•Token pessoal do GitHub

•Criar um arquivo .env contendo:
    GITHUB_TOKEN=seu_token_aqui

Passos

1.Clone o repositório:

    git clone https://github.com/seu-usuario/lab01-experimentacao-software.git




2.Acesse a pasta:

        cd lab01-experimentacao-software



3.Instale as dependências:

        pip install -r requirements.txt



4.Execute o script:

        python lab01s01.py



O script realizará automaticamente a requisição e exibirá os dados coletados.

📂 Estrutura do Projeto

        lab01-experimentacao-software/
        │
        ├── lab01s01.py          # Sprint 1 - Coleta 100 repos (faixas de estrelas)
        ├── lab01s02.py          # Sprint 2 - Coleta 1000 repos (paginação) + CSV
        ├── queries.py           # Queries GraphQL
        ├── repositorios.csv     # Dados exportados (1000 repos)
        ├── saida.txt            # Saída da execução Sprint 1
        ├── .env                 # Token do GitHub
        ├── requirements.txt
        └── README.md



📈 Quadro de Evolução do Projeto

Esta seção apresenta a evolução incremental do experimento ao longo das sprints, evidenciando o que foi implementado e o que ainda será desenvolvido.

🟢 Sprint 1 — Lab01S01 (Concluída)
🎯 Objetivo

Implementar consulta GraphQL para coletar dados de 100 repositórios populares com todas as métricas necessárias para responder às RQs.

✅ Implementado

→ Consulta GraphQL para os 100 repositórios mais estrelados

→ **Busca por lotes usando faixas de estrelas** (10 lotes de 10 repos)

→ **Mecanismo de retry automático** com backoff (10 tentativas, delay linear)

→ Requisição automática via Python (requests + python-dotenv)

→ Autenticação com token GitHub via arquivo .env

→ Coleta das métricas:

    • nameWithOwner

    • createdAt

    • updatedAt

    • stargazerCount

    • pullRequests (MERGED)

    • releases

    • issues

    • closedIssues

    • primaryLanguage

📊 Resultado da Execução

```
Iniciando busca de 100 repositórios em lotes por faixa de estrelas...
(Sem paginação - usando filtros diferentes para cada lote)

[Lote 1/10] Buscando: stars:>=200000
  Tentativa 1/10...
  ✓ Coletados 10 repositórios (total: 10)
  ...
[Lote 10/10] Buscando: stars:40000..44999
  Tentativa 1/10...
  ✓ Coletados 10 repositórios (total: 100)

==================================================
Total de repositórios coletados: 100
==================================================
```

🏆 Top 10 Repositórios Coletados

| # | Repositório | Estrelas | Linguagem |
|---|-------------|----------|----------|
| 1 | codecrafters-io/build-your-own-x | 472.553 | Markdown |
| 2 | sindresorhus/awesome | 442.887 | - |
| 3 | freeCodeCamp/freeCodeCamp | ~420k | TypeScript |
| 4 | public-apis/public-apis | ~340k | Python |
| 5 | kamranahmedse/developer-roadmap | ~320k | TypeScript |
| 6 | jwasham/coding-interview-university | ~319k | - |
| 7 | donnemartin/system-design-primer | ~298k | Python |
| 8 | facebook/react | ~235k | JavaScript |
| 9 | torvalds/linux | ~191k | C |
| 10 | tensorflow/tensorflow | ~188k | C++ |

📌 Status das RQs na Sprint 1

| RQ | Pergunta | Métrica | Dados Coletados | RQ Respondida |
|----|----------|---------|-----------------|---------------|
| RQ01 | Sistemas populares são maduros/antigos? | Idade do repositório (data de criação) | `createdAt` | ❌ |
| RQ02 | Sistemas populares recebem muita contribuição externa? | Total de pull requests aceitas | `pullRequests(MERGED)` | ❌ |
| RQ03 | Sistemas populares lançam releases com frequência? | Total de releases | `releases` | ❌ |
| RQ04 | Sistemas populares são atualizados com frequência? | Tempo até última atualização | `updatedAt` | ❌ |
| RQ05 | Sistemas populares são escritos nas linguagens mais populares? | Linguagem primária | `primaryLanguage` | ❌ |
| RQ06 | Sistemas populares possuem alto percentual de issues fechadas? | Razão issues fechadas/total | `issues` + `closedIssues` | ❌ |

**Observação:**
Nesta sprint foi realizada apenas a coleta das métricas necessárias para 100 repositórios.
As RQs ainda não foram respondidas, pois não houve análise estatística ou interpretação dos dados.

🟡 Sprint 2 — Lab01S02 (Concluída)
🎯 Objetivo

→ Implementar paginação

→ Coletar 1.000 repositórios

→ Exportar dados para CSV

→ Preparar base para análise estatística

✅ Implementado

→ **Paginação com cursor** para coleta de 1000 repositórios

→ **Query GraphQL otimizada** com suporte a paginação (`after: $cursor`)

→ **Exportação automática para CSV** com todas as métricas

→ **Métricas calculadas** adicionais:
    • `idade_dias` - idade do repositório em dias
    • `dias_desde_atualizacao` - dias desde última atualização
    • `razao_issues_fechadas` - proporção de issues fechadas

→ **Estatísticas automáticas** exibidas ao final da execução

→ **Retry automático** com 10 tentativas e backoff para erros 502

📊 Estrutura do CSV Gerado

| Coluna | Descrição | RQ Relacionada |
|--------|-----------|----------------|
| nome | Nome do repositório (owner/repo) | - |
| criado_em | Data de criação | RQ01 |
| atualizado_em | Data última atualização | RQ04 |
| estrelas | Número de estrelas | - |
| linguagem | Linguagem principal | RQ05 |
| prs_merged | Total de PRs aceitos | RQ02 |
| releases | Total de releases | RQ03 |
| issues_total | Total de issues | RQ06 |
| issues_fechadas | Issues fechadas | RQ06 |
| idade_dias | Idade em dias | RQ01 |
| dias_desde_atualizacao | Dias desde atualização | RQ04 |
| razao_issues_fechadas | Issues fechadas / total | RQ06 |

📈 Resultado da Execução

```
============================================================
LAB01S02 - Sprint 2: Paginação + Exportação CSV
============================================================

============================================================
Iniciando coleta de 1000 repositórios com paginação
Páginas estimadas: 100 (10 repos/página)
============================================================

[Página 1/100] Coletando repositórios 1-10...
  ✓ Coletados 10 repositórios (total: 10)
[Página 2/100] Coletando repositórios 11-20...
  ✓ Coletados 10 repositórios (total: 20)
...
[Página 100/100] Coletando repositórios 991-1000...
  ✓ Coletados 10 repositórios (total: 1000)

============================================================
COLETA FINALIZADA: 1000 repositórios
============================================================

✓ Dados exportados para: repositorios.csv
  Total de linhas: 1000
```

📊 Estatísticas Coletadas

```
============================================================
ESTATÍSTICAS DOS DADOS COLETADOS
============================================================

Total de repositórios: 1000

Estrelas:
  Máximo: ~470.000
  Mínimo: ~10.000
  Média: ~30.000

Idade (dias):
  Máximo: ~6.000 dias
  Mínimo: ~100 dias
  Média (anos): ~7 anos

Top 10 Linguagens:
  1. JavaScript
  2. Python
  3. TypeScript
  4. Go
  5. Java
  6. Rust
  7. C++
  8. C
  9. Shell
  10. Ruby

Pull Requests Merged:
  Total: ~500.000+
  Média por repo: ~500

Razão de Issues Fechadas:
  Média: ~85%
```

🗂️ Arquivos da Sprint 2

| Arquivo | Descrição |
|---------|-----------|
| `lab01s02.py` | Script principal com paginação |
| `queries.py` | Query `QUERY_PAGINADA` adicionada |
| `repositorios.csv` | Dados dos 1000 repositórios |

📌 Status das RQs na Sprint 2

| RQ | Pergunta | Métrica | Campo no CSV | RQ Respondida |
|----|----------|---------|--------------|---------------|
| RQ01 | Sistemas populares são maduros/antigos? | Idade do repositório | `criado_em`, `idade_dias` | ❌ |
| RQ02 | Sistemas populares recebem muita contribuição externa? | Total de PRs aceitas | `prs_merged` | ❌ |
| RQ03 | Sistemas populares lançam releases com frequência? | Total de releases | `releases` | ❌ |
| RQ04 | Sistemas populares são atualizados com frequência? | Tempo até última atualização | `atualizado_em`, `dias_desde_atualizacao` | ❌ |
| RQ05 | Sistemas populares são escritos nas linguagens mais populares? | Linguagem primária | `linguagem` | ❌ |
| RQ06 | Sistemas populares possuem alto percentual de issues fechadas? | Razão issues fechadas/total | `issues_total`, `issues_fechadas`, `razao_issues_fechadas` | ❌ |

**Observação:**
Nesta sprint foi realizada a coleta completa dos 1000 repositórios com exportação para CSV.
Todas as métricas necessárias estão disponíveis no arquivo `repositorios.csv`.
As RQs ainda não foram respondidas formalmente, aguardando análise estatística na Sprint 3.

🔵 Sprint 3 — Lab01S03 (Concluída)
🎯 Objetivo

→ Cálculo de medianas

→ Análise estatística

→ Geração de visualizações

→ Discussão das hipóteses

→ Relatório final

✅ Implementado

→ Script `lab01s03.py` para análise automática do CSV da Sprint 2

→ Geração do relatório final em Markdown: `docs/Sprint3/Relatorio_Final_Sprint3.md`

→ Geração de 4 gráficos:
  - `docs/Sprint3/figures/top_linguagens.png`
  - `docs/Sprint3/figures/distribuicao_idade.png`
  - `docs/Sprint3/figures/distribuicao_issues_fechadas.png`
  - `docs/Sprint3/figures/boxplot_prs.png`

→ Resposta das RQs com base em métricas de mediana/distribuição

📌 Status das RQs na Sprint 3 (Respondidas)

| RQ | Pergunta | Resultado | RQ Respondida |
|----|----------|-----------|---------------|
| RQ01 | Sistemas populares são maduros/antigos? | Mediana de idade = 8,39 anos | ✅ Sim |
| RQ02 | Sistemas populares recebem muita contribuição externa? | Mediana de PRs merged = 739 | ✅ Sim |
| RQ03 | Sistemas populares lançam releases com frequência? | Mediana de releases = 40 | ✅ Sim |
| RQ04 | Sistemas populares são atualizados com frequência? | Mediana desde última atualização = 0 dias | ✅ Sim |
| RQ05 | Sistemas populares são escritos nas linguagens mais populares? | Top linguagens incluem Python, TypeScript e JavaScript | ✅ Sim |
| RQ06 | Sistemas populares possuem alto percentual de issues fechadas? | Mediana da razão de fechamento = 87,78% | ✅ Sim |

📎 Artefatos finais da Sprint 3

- `lab01s03.py`
- `docs/Sprint3/Relatorio_Final_Sprint3.md`
- `docs/Sprint3/figures/*.png`

👨‍💻 Autor

Kaio Henrique Oliveira da Silveira Barbosa
Aluno de Engenharia de Software – PUC Minas
Email: kaiohsilveira@gmail.com

2026

