from firebase_config import get_clientes, add_cliente, update_cliente, delete_cliente

# # 🔹 Teste: Adicionar cliente
# add_cliente("cliente1", "Anderson Augusto", "anderson@email.com", "987654321")

# 🔹 Teste: Buscar clientes
clientes = get_clientes()
if clientes:
    print("Clientes encontrados:", clientes)

# # 🔹 Teste: Atualizar cliente
# update_cliente("cliente1", nome="Anderson A.", email="novoemail@email.com")

# # 🔹 Teste: Deletar cliente
# delete_cliente("cliente1")