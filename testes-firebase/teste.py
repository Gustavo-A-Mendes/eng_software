from firebase_config import db

def menu():
    while True:
        print("\n=== Sistema de Aluguel de Carros ===")
        print("1. Cadastrar Cliente")
        print("2. Cadastrar Veículo")
        print("3. Registrar Aluguel")
        print("4. Registrar Devolução")
        print("5. Listar Clientes") # MENU SECUNDARIO PARA BUSCAR E EDITAR UM CLIENTE
        print("6. Listar Veículos") # MENU SECUNDARIO PARA BUSCAR E EDITAR UM VEÍCULO
        print("7. Importar Dados")
        print("8. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            cadastrar_veiculo()
        elif opcao == "3":
            registrar_aluguel()
        elif opcao == "4":
            registrar_devolucao()
        elif opcao == "5":
            listar_clientes()
        elif opcao == "6":
            listar_veiculos()
        elif opcao == "7":
            tabela = input("Nome da tabela para importar (clientes, veiculos, alugueis): ").strip()
            arquivo_csv = input("Nome do arquivo CSV (ex: clientes.csv): ").strip()
            importar_csv_para_bd(tabela, arquivo_csv)
        elif opcao == "8":
            exportar_tabelas_para_csv()
            break
        else:
            print("Opção inválida! Tente novamente.")

# ============================== DEFINIÇÃO DO CRUD ==============================   
def post_tabela(tabela, dados_envio): # (CREATE)
    """
    Envia os dados para uma tabela do banco de dados.

    :param tabela: Nome da tabela.
    :param dado_envio: Lista dos valores que devem ser adicionados.
    """
    valor_dados = list(dados_envio.values())
    try:
        cliente_ref = db.collection(tabela).add({
            "id_cliente": dados_envio["id"],
            "nome": dados_envio["nome"],
            "cpf": dados_envio["cpf"],
            "telefone": dados_envio["telefone"],
            "cidade": dados_envio["cidade"],
            "bairro": dados_envio["bairro"],
            "rua": dados_envio["rua"],
            "numero": dados_envio["numero"],
        })
        print("Cliente adicionado com sucesso!")
    
    except Exception as e:
        print(f"Erro ao atualizar: {e}")


def get_tabela(tabela): # (READ)
    """
    Solicita os dados de uma tabela do banco de dados.

    :param tabela: Nome da tabela.
    """
    
    # Cria conexão e executa o comando:
    conexao = conectar_bd()
    cursor = conexao.cursor()

    try:
        cursor.execute(f"SELECT * FROM {tabela}")
        clientes = cursor.fetchall()
        # Caso o resultado seja vazio, encerra a função:
        if not clientes:
            print("Nenhum cliente cadastrado.")
            clientes = None
        

    except Exception as e:
        print(f"Erro ao atualizar: {e}")
        clientes = None
    
    finally:
        # Encerra conexão:
        cursor.close()
        conexao.close()

        # retorna resultado:
        return clientes
 

def update_tabela(tabela, id, dados_envio): # (UPDATE)
    """
    Atualiza um registro em uma tabela específica.

    :param tabela: Nome da tabela.
    :param id: ID do registro a ser atualizado.
    :param dados_envio: Dicionário com as colunas e valores a serem atualizados.
    """
    
    # Cria conexão e executa o comando:
    conexao = conectar_bd()
    cursor = conexao.cursor()
    
    # Cria os pares "coluna = valor" dinamicamente:
    colunas_valores = [f"{coluna} = {valor}" for coluna, valor in dados_envio.items()]
    query = f"UPDATE {tabela} SET {', '.join(colunas_valores)} WHERE id = {id}"

    try:
        if not dados_envio:
            print("Nenhum dado para atualizar.")
        else:
            cursor.execute(query)
            conexao.commit()
            print(f"Registro {id} atualizado na tabela '{tabela}' com sucesso.")

    except Exception as e:
        print(f"Erro ao atualizar: {e}")
    
    finally:
        cursor.close()
        conexao.close()


def delete_tabela(tabela, id = None): # (DELETE)
    """
    Remove um registro de uma tabela específica.

    :param tabela: Nome da tabela.
    :param id: ID do registro a ser removido.
    """
    
    # Cria conexão e executa o comando:
    conexao = conectar_bd()
    cursor = conexao.cursor()

    try:
        if id is None:
            confirmacao = input(f"Tem certeza que deseja excluir TODOS os registros da tabela '{tabela}'? (sim/não): ").strip().lower()
            if confirmacao == "sim":
                query = f"DELETE FROM {tabela}"
                message = f"TODOS os registros da tabela '{tabela}' foram removidos!"
            else:
                print("Operação cancelada.")

        else:
            query = f"DELETE FROM {tabela} WHERE id = {id}"
            message = f"Registro {id} removido da tabela '{tabela}' com sucesso."

        cursor.execute(query)
        print(message)
        conexao.commit()

    except Exception as e:
        print(f"Erro ao remover registro: {e}")
    
    finally:
        cursor.close()
        conexao.close()

# ============================== DEFINIÇÃO DO CRUD ==============================   

# 
def cadastrar_cliente():
    nome = input("Nome do cliente: ")
    telefone = input("Telefone do cliente: ")
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO cliente (nome, cpf, cnh, telefone, cidade, bairro, rua, numero) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (nome, "123123", "123123", telefone, "Iguatu", "Bugi", "Francisco Adolfo", "171"))
    conexao.commit()
    cursor.close()
    conexao.close()
    print("Cliente cadastrado com sucesso!")

def cadastrar_veiculo():
    modelo = input("Modelo do veículo: ")
    ano = input("Ano do veículo: ")
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO veiculos (modelo, ano) VALUES (%s, %s)", (modelo, ano))
    conexao.commit()
    cursor.close()
    conexao.close()
    print("Veículo cadastrado com sucesso!")

def listar_clientes():
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM cliente")
    clientes = cursor.fetchall()

    if not clientes:
        print("Nenhum cliente cadastrado.")
    else:
        print("\n=== Lista de Clientes ===")
        for cliente in clientes:
            print(cliente)
            # print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Telefone: {cliente[2]}")

    cursor.close()
    conexao.close()
    # print("Veículo cadastrado com sucesso!")
# Outras funções como registrar aluguel, devolução e listar clientes/veículos podem ser implementadas seguindo a mesma lógica.

def importar_csv_para_bd(tabela, arquivo_csv):
    """Importa dados de um arquivo CSV para a tabela especificada."""
    conexao = conectar_bd()
    cursor = conexao.cursor()

    with open(arquivo_csv, mode="r", encoding="utf-8") as arquivo:
        leitor_csv = csv.reader(arquivo)
        colunas = next(leitor_csv)  # Lê a primeira linha (nomes das colunas)

        # Criando um placeholder para os valores (%s, %s, ...)
        placeholders = ", ".join(["%s"] * len(colunas))
        query = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({placeholders})"

        for linha in leitor_csv:
            cursor.execute(query, linha)

    conexao.commit()
    cursor.close()
    conexao.close()
    print(f"Dados do arquivo '{arquivo_csv}' importados para a tabela '{tabela}' com sucesso!")


def exportar_tabelas_para_csv():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    tabelas = ["clientes", "veiculos", "alugueis"]  # Adicione mais tabelas se necessário

    for tabela in tabelas:
        arquivo_csv = f"{tabela}.csv"
        
        # Executa a consulta para pegar todos os dados da tabela
        cursor.execute(f"SELECT * FROM {tabela}")
        dados = cursor.fetchall()  # Recupera todos os registros
        
        # Obtém os nomes das colunas
        colunas = [desc[0] for desc in cursor.description]

        # Escreve os dados no arquivo CSV
        with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(colunas)  # Escreve os cabeçalhos das colunas
            writer.writerows(dados)   # Escreve os dados

        print(f"Tabela '{tabela}' exportada para '{arquivo_csv}'")

    cursor.close()
    conexao.close()


if __name__ == "__main__":
    criar_tabelas()
    menu()
