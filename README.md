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

•Coleta das seguintes métricas:

    •createdAt

    •updatedAt

    •pullRequests(states: MERGED)

    •releases

    •issues

    •issues(states: CLOSED)

    •primaryLanguage



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

1️⃣ Erro 502 (Bad Gateway)

Ao solicitar 100 repositórios com múltiplas métricas aninhadas, a API retornou:

        502 Bad Gateway

Causa

Alta complexidade da query (limitação da API GraphQL do GitHub).

Solução:

→ Simplificação e validação progressiva da consulta.

2️⃣ Erro de Sintaxe GraphQL

Erro retornado:

        Expected NAME, actual: ("\n")

Causa

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
        ├── lab01s01.py
        ├── queries.py
        ├── .env
        ├── requirements.txt
        └── README.md



📈 Quadro de Evolução do Projeto

Esta seção apresenta a evolução incremental do experimento ao longo das sprints, evidenciando o que foi implementado e o que ainda será desenvolvido.

🟢 Sprint 1 — Lab01S01 (Concluída)
🎯 Objetivo

Implementar consulta GraphQL para coletar dados de 100 repositórios populares com todas as métricas necessárias para responder às RQs.

✅ Implementado

→ Consulta GraphQL para os 100 repositórios mais estrelados

→ Requisição automática via Python

→ Autenticação com token GitHub

→ Coleta das métricas:

    .createdAt

    .updatedAt

    .pullRequests (MERGED)

    .releases

    .issues

    .closedIssues

    .primaryLanguage

📌 Status das RQs na Sprint 1
RQ	Métricas Coletadas	RQ Respondida?
        RQ01	✔	❌
        RQ02	✔	❌
        RQ03	✔	❌
        RQ04	✔	❌
        RQ05	✔	❌
        RQ06	✔	❌

Observação:
Nesta sprint foi realizada apenas a coleta das métricas necessárias.
As RQs ainda não foram respondidas, pois não houve análise estatística ou interpretação dos dados.

🟡 Sprint 2 — Lab01S02 (Em desenvolvimento)
🎯 Objetivo

→ Implementar paginação

→ Coletar 1.000 repositórios

→ Exportar dados para CSV

→ Preparar base para análise estatística

📌 Status esperado
RQ	Métricas Coletadas	Análise Parcial	RQ Respondida?
    RQ01	✔	✔	❌
    RQ02	✔	✔	❌
    RQ03	✔	✔	❌
    RQ04	✔	✔	❌
    RQ05	✔	✔	❌
    RQ06	✔	✔	❌

🔵 Sprint 3 — Lab01S03 (Planejada)
🎯 Objetivo

→ Cálculo de medianas

→ Análise estatística

→ Geração de visualizações

→ Discussão das hipóteses

→ Relatório final

📌 Status esperado
RQ	Métricas Coletadas	Análise Estatística	RQ Respondida?
    RQ01	✔	✔	✔
    RQ02	✔	✔	✔
    RQ03	✔	✔	✔
    RQ04	✔	✔	✔
    RQ05	✔	✔	✔
    RQ06	✔	✔	✔

👨‍💻 Autor

Kaio Henrique Oliveira da Silveira Barbosa
Aluno de Engenharia de Software – PUC Minas
Email: kaiohsilveira@gmail.com

2026

