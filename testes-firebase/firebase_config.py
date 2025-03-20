import firebase_admin
from firebase_admin import credentials, firestore
import os

# Obtém o caminho absoluto do diretório onde o script está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "meu-firebase.json")

# Carregar a chave JSON com o caminho absoluto
cred = credentials.Certificate(json_path)

# Inicializar Firebase
firebase_admin.initialize_app(cred)

# Conectar ao Firestore
db = firestore.client()