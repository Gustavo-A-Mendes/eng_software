import os
import json
import firebase_admin
from firebase_admin import credentials, firestore


# Tenta pegar credenciais do GitHub Secrets
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

if firebase_credentials:
    # Se rodando no GitHub, converte a string JSON em um dicionário
    cred_data = json.loads(firebase_credentials)
    cred = credentials.Certificate(cred_data)
else:
    # Se rodando localmente, usa o arquivo JSON
    # Obtém o caminho absoluto do diretório onde o script está localizado
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(BASE_DIR, "meu-firebase.json")
    cred = credentials.Certificate(json_path)

# Inicializa o Firebase
firebase_admin.initialize_app(cred)
db = firestore.client()

print("🔥 Firebase conectado com sucesso!")