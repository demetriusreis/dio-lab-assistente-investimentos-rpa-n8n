import requests
from bs4 import BeautifulSoup

# Endereço da página de clientes da DIO
URL_PAGINA = "https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/"

# Endereço do Webhook do n8n
N8N_WEBHOOK = "http://host.docker.internal:5678/webhook/clientes"

# 1. Acessar a página da DIO
resposta = requests.get(URL_PAGINA, timeout=30)
resposta.raise_for_status()

# 2. Ler o HTML da página
soup = BeautifulSoup(resposta.text, "html.parser")

# 3. Encontrar os clientes na tabela
linhas = soup.select("#clientes tbody tr")

clientes = []

for linha in linhas:
    colunas = linha.find_all("td")

    if len(colunas) < 4:
        continue

    cliente = {
        "nome": colunas[0].get_text(strip=True),
        "email": colunas[1].get_text(strip=True),
        "saldo": colunas[2].get_text(strip=True),
        "perfil": colunas[3].get_text(strip=True),
    }

    clientes.append(cliente)

# 4. Mostrar os clientes encontrados
print(f"Clientes encontrados: {len(clientes)}")

for cliente in clientes:
    print(cliente)

# 5. Enviar os clientes para o n8n
if clientes:
    resposta_n8n = requests.post(
        N8N_WEBHOOK,
        json={"clientes": clientes},
        timeout=30
    )

    resposta_n8n.raise_for_status()

    print("Dados enviados ao n8n com sucesso!")
    print(resposta_n8n.text)
else:
    print("Nenhum cliente encontrado.")
