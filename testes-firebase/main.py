from firebase_config import db

def adicionar_cliente(nome, email, telefone):
    cliente_ref = db.collection("clientes").add({
        "nome": nome,
        "email": email,
        "telefone": telefone
    })
    print("Cliente adicionado com sucesso!")

# Exemplo de uso
adicionar_cliente("And", "Andisu@gmail.com", "123456789")

#---------------------------------------------------------------#
def listar_clientes():
    clientes_ref = db.collection("clientes").stream()
    
    for cliente in clientes_ref:
        print(f'ID: {cliente.id} - {cliente.to_dict()}')

# Chamando a função
# listar_clientes()

#---------------------------------------------------------------#
def atualizar_cliente(id_documento, novo_email):
    doc_ref = db.collection("clientes").document(id_documento)
    doc_ref.update({"email": novo_email})
    print("Cliente atualizado com sucesso!")

# Exemplo de uso (substitua pelo ID correto)
# atualizar_cliente("abc123", "novoemail@email.com")


#---------------------------------------------------------------#
def deletar_cliente(id_documento):
    db.collection("clientes").document(id_documento).delete()
    print("Cliente removido com sucesso!")

# Exemplo de uso
# deletar_cliente("abc123")