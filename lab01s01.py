import os
import requests
import json
from dotenv import load_dotenv
from queries import QUERY_100_REPOS

# 1. Carrega variáveis de ambiente
load_dotenv()

# 2. Obtém token do GitHub
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
URL = 'https://api.github.com/graphql'

# 3. Verifica se o token existe
if not GITHUB_TOKEN:
    raise ValueError("Token do GitHub não encontrado. Verifique o arquivo .env")

# 4. Define cabeçalhos da requisição
headers = {
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'Content-Type': 'application/json'
}

print("Iniciando requisição automática para 100 repositórios...")

# 5. Faz a requisição HTTP para a API GraphQL
response = requests.post(
    URL,
    json={'query': QUERY_100_REPOS},
    headers=headers
)

# 6. Verifica status da resposta
if response.status_code == 200:
    print("Requisição realizada com sucesso!\n")

    dados = response.json()

    # 👇 RESPOSTA DA API
    print("Resposta bruta da API:")
    print(json.dumps(dados, indent=2))

    # Verificação segura
    if "errors" in dados:
        print("\nErro retornado pela API GraphQL:")
        print(json.dumps(dados["errors"], indent=2))
        exit()

    if "data" not in dados:
        print("\nResposta inesperada (não contém 'data')")
        exit()

    repositorios = dados['data']['search']['nodes']

    print(f"\nTotal de repositórios retornados: {len(repositorios)}")

else:
    print(f"Erro HTTP: {response.status_code}")
    print(response.text)