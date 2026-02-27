1-  Implementação Inicial

Foi desenvolvida uma requisição automática em Python utilizando:

requests para consumo da API

dotenv para leitura segura do token

API GraphQL do GitHub (https://api.github.com/graphql)

Query buscando os 100 repositórios mais estrelados (stars:>10000 sort:stars-desc)

Coleta das métricas necessárias para responder às RQs

A requisição foi realizada via método POST, enviando a query no corpo da requisição em formato JSON.

2- Erro 502 – Limitação de Complexidade da API

Ao tentar solicitar:

first: 100

junto com múltiplas métricas aninhadas (pull requests, issues, releases, linguagem principal etc.), a API retornou:

502 Bad Gateway (nginx)

Esse erro ocorre quando a query excede o limite de complexidade permitido pela API do GitHub. Queries com muitos nós e campos aninhados aumentam significativamente o custo computacional da operação.

Conclusão:
A consulta estava sintaticamente correta, mas complexa demais para ser processada pelo servidor.

3- Erro de Sintaxe GraphQL

Após simplificar a query, foi retornado o erro:

Expected NAME, actual: ("\n")

Esse erro indicava problema estrutural na query, causado por:

Chaves {} abertas e não fechadas corretamente

Estrutura incompleta da query

A correção foi feita ajustando corretamente o fechamento dos blocos:

query {
  search {
    nodes {
      campo
    }
  }
}

4️- Erro de Union Type (SearchResultItem)

Após corrigir a sintaxe, surgiu o erro:

Selections can't be made directly on unions

Isso ocorre porque o campo search retorna um tipo UNION chamado SearchResultItem.

Em GraphQL, não é permitido acessar campos diretamente em um union.
É necessário especificar o tipo concreto utilizando Inline Fragment:

Forma incorreta:

nodes {
  nameWithOwner
}

Forma correta:

nodes {
  ... on Repository {
    nameWithOwner
  }
}

A partir dessa correção, a query passou a ser semanticamente válida.

5- Versão Final da Query

A consulta final passou a utilizar:

first: 100

Inline fragment ... on Repository

Coleta de todas as métricas necessárias para as RQs

Exemplo da estrutura final:

nodes {
  ... on Repository {
    nameWithOwner
    createdAt
    updatedAt
    primaryLanguage { name }
    pullRequests(states: MERGED) { totalCount }
    releases { totalCount }
    issues { totalCount }
    closedIssues: issues(states: CLOSED) { totalCount }
  }
}

6-  Aprendizados Técnicos

Durante a implementação foram consolidados os seguintes conceitos:

-Autenticação via token na API GraphQL

-Estrutura de requisições POST com JSON

-Tratamento de erros HTTP (502)

-Interpretação de erros semânticos do GraphQL

-Uso de Inline Fragments para tratar Union Types

-Limitações de complexidade da API do GitHub