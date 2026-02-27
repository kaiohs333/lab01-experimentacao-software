import os
import requests
import json
from dotenv import load_dotenv
from queries import QUERY_100_REPOS # variável do outro arquivo

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Pega o token de forma segura
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN') 
URL = 'https://api.github.com/graphql'

# Se o token não for encontrado, o script avisa e para
if not GITHUB_TOKEN:
    raise ValueError("Token do GitHub não encontrado. Verifique o arquivo .env")

# 2. Configura os cabeçalhos da requisição
headers = {
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'Content-Type': 'application/json'
}

# 3. Fazendo a requisição HTTP usando a query importada
print("Fazendo a requisição para a API do GitHub...")
response = requests.post(URL, json={'query': QUERY_100_REPOS}, headers=headers)

# 4. Verificando a resposta
if response.status_code == 200:
    print("Sucesso! Dados recebidos.\n")
    dados = response.json()
    repositorios = dados['data']['search']['nodes']
    
    print(f"Total de repositórios retornados: {len(repositorios)}")
    
    # Exibe o primeiro só para conferir
    primeiro_repo = repositorios[0]
    print("\n--- Exemplo do Top 1 Repositório ---")
    print(json.dumps(primeiro_repo, indent=2, ensure_ascii=False))
else:
    print(f"Falha na requisição. Código de status: {response.status_code}")
    print(response.text)