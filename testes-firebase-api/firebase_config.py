import requests

# 🔹 Substitua pelos seus valores
PROJECT_ID = "teste-eng-software"
API_KEY = "AIzaSyD7cWnE5MCi1HAvXwvlJhXE2eNMk8miYTo"

# 🔹 URL base do Firestore
BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"


def get_clientes():
    """ Obtém todos os documentos da coleção 'clientes'. """
    url = f"{BASE_URL}/clientes?key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao buscar clientes:", response.text)
        return None


def add_cliente(cliente_id, nome, email, telefone):
    """ Adiciona um novo cliente ao Firestore. """
    url = f"{BASE_URL}/clientes/{cliente_id}?key={API_KEY}"
    data = {
        "fields": {
            "nome": {"stringValue": nome},
            "email": {"stringValue": email},
            "telefone": {"stringValue": telefone}
        }
    }
    
    response = requests.patch(url, json=data)
    
    if response.status_code == 200:
        print(f"Cliente {cliente_id} adicionado com sucesso!")
    else:
        print("Erro ao adicionar cliente:", response.text)


def update_cliente(cliente_id, nome=None, email=None, telefone=None):
    """ Atualiza os dados de um cliente existente no Firestore. """
    url = f"{BASE_URL}/clientes/{cliente_id}?key={API_KEY}"
    data = {"fields": {}}

    if nome:
        data["fields"]["nome"] = {"stringValue": nome}
    if email:
        data["fields"]["email"] = {"stringValue": email}
    if telefone:
        data["fields"]["telefone"] = {"stringValue": telefone}

    response = requests.patch(url, json=data)

    if response.status_code == 200:
        print(f"Cliente {cliente_id} atualizado com sucesso!")
    else:
        print("Erro ao atualizar cliente:", response.text)


def delete_cliente(cliente_id):
    """ Remove um cliente do Firestore. """
    url = f"{BASE_URL}/clientes/{cliente_id}?key={API_KEY}"
    response = requests.delete(url)

    if response.status_code == 200:
        print(f"Cliente {cliente_id} removido com sucesso!")
    else:
        print("Erro ao remover cliente:", response.text)