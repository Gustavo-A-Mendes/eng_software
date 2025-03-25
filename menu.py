from crud import *
from sistema import *

# 
def menu():
    while True:
        os.system('cls')
        print("=== Sistema de Aluguel de Carros ===")
        print("1. Cadastro")
        print("2. Consulta")
        print("3. Importar Dados")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        # SUBMENU CADASTRO
        if opcao == "1":
            menu_cadastro()

        # SUBMENU CONSULTA
        elif opcao == "2":
            menu_consulta()
            
        # IMPORTAR DADOS
        elif opcao == "3":
            importar_csv_para_bd()

        # SAIR
        elif opcao == "4":
            exportar_tabelas_para_csv()
            break
        
        else:
            print("\nOpção inválida! Tente novamente.")
            sleep(0.25)

#
def menu_cadastro():
    while True:
        os.system('cls') 
        print("\n=== Sistema de Aluguel de Carros ===")
        print("1. Cadastrar Aluguel")
        print("2. Cadastrar Cliente")
        print("3. Cadastrar Carro")
        print("4. Cadastrar Funcionário")
        print("5. Voltar")
        opcao_submenu = input ("Escolha uma opção: ")

        if opcao_submenu == "1":
            cadastrar_aluguel()
            break
        
        elif opcao_submenu == "2":
            cadastrar_cliente()
            break
        
        elif opcao_submenu == "3":
            cadastrar_carro()
            break
        
        elif opcao_submenu == "4":
            cadastrar_funcionario()
            break
        
        elif opcao_submenu == "5":
            break
        
        else:
            print("\nOpção inválida! Tente novamente.")
            sleep(0.25)

#
def menu_consulta():
    while True:
        os.system('cls')
        print("\n=== Sistema de Aluguel de Carros ===")
        print("1. Consultar Aluguéis")
        print("2. Consultar Clientes") # MENU SECUNDARIO PARA BUSCAR E EDITAR UM CLIENTE
        print("3. Consultar Carros") # MENU SECUNDARIO PARA BUSCAR E EDITAR UM CARRO
        print("4. Consultar Funcionários") # MENU SECUNDARIO PARA BUSCAR E EDITAR UM FUNCIONÁRIO
        print("5. Voltar")
        opcao_submenu = input ("Escolha uma opção: ")
        
        # SUBMENU ALUGUEL
        if opcao_submenu == "1":
            while True:
                os.system('cls')
                print("\n=== Sistema de Aluguel de Carros ===")
                
                print("\n=== Lista de Aluguéis ===")

                if not exibe_tabela("aluguel"):
                    input("\nAperte ENTER para voltar...")
                    break

                ret = exibir_opcoes()
                if ret == "1":
                    id = input("Especifique um ID: ")
                    if verifica_id_existente("aluguel", id):
                        edita_aluguel(id)
                    else:
                        print("ID não encontrado.")
                        sleep(0.25)
                elif ret == "2":
                    id = input("Especifique um ID: ")
                    if verifica_id_existente("aluguel", id):
                        dados_aluguel = dados_tabela('aluguel', id)
                        if delete_tabela("aluguel", id):
                            encerra_aluguel(dados_aluguel)

                    else:
                        print("ID não encontrado.")
                        sleep(0.25)
                elif ret == "3":
                    break
                else: 
                    print("Opção inválida.")
                    sleep(0.25)
        
        # SUBMENU CLIENTE
        elif opcao_submenu == "2":
            while True:
                os.system('cls')
                print("\n=== Sistema de Aluguel de Carros ===")
                
                print("\n=== Lista de Clientes ===")

                if not exibe_tabela("cliente"):
                    input("\nAperte ENTER para voltar...")
                    break

                ret = exibir_opcoes()
                if ret == "1":
                    id = input("Especifique um ID: ")
                    if verifica_id_existente("cliente", id):
                        edita_cliente(id)
                    else:
                        print("ID não encontrado.")
                        sleep(0.25)
                elif ret == "2":
                    id = input("Especifique um ID: ")
                    if verifica_id_existente("cliente", id):
                        delete_tabela("cliente", id)
                    else:
                        print("ID não encontrado.")
                        sleep(0.25)
                elif ret == "3":
                    break
                else: 
                    print("Opção inválida.")
                    sleep(0.25)

        # SUBMENU CARROS
        elif opcao_submenu == "3":
            while True:
                os.system('cls')
                print("\n=== Sistema de Aluguel de Carros ===")
                
                print("\n=== Lista de Carros ===")

                if not exibe_tabela("carro"):
                    input("\nAperte ENTER para voltar...")
                    break

                ret = exibir_opcoes()
                if ret == "1":
                    id = input("Especifique um ID: ")
                    if verifica_id_existente("carro", id):
                        edita_carro(id)
                    else:
                        print("ID não encontrado.")
                        sleep(0.25)
                elif ret == "2":
                    id = input("Especifique um ID: ")
                    if verifica_id_existente("carro", id):
                        delete_tabela("carro", id)
                    else:
                        print("ID não encontrado.")
                        sleep(0.25)

                elif ret == "3":
                    break
                else: 
                    print("Opção inválida.")
                    sleep(0.25)

        # SUBMENU FUNCIONÁRIOS
        elif opcao_submenu == "4":
            while True:
                os.system('cls')
                print("\n=== Sistema de Aluguel de Carros ===")
                
                print("\n=== Lista de Funcionarios ===")
                
                if not exibe_tabela("funcionario"):
                    input("\nAperte ENTER para voltar...")
                    break
                
                ret = exibir_opcoes()
                if ret == "1":
                    id = input("Especifique um ID: ")
                    if verifica_id_existente("funcionario", id):
                        edita_funcionario(id)
                    else:
                        print("ID não encontrado.")
                        sleep(0.25)
                elif ret == "2":
                    id = input("Especifique um ID: ")
                    if verifica_id_existente("funcionario", id):
                        delete_tabela("funcionario", id)
                    else:
                        print("ID não encontrado.")
                        sleep(0.25)
                elif ret == "3":
                    break
                else: 
                    print("Opção inválida.")
                    sleep(0.25)

        elif opcao_submenu == "5":
            break

        else:
            print("\nOpção inválida! Tente novamente.")
            sleep(0.25)

# Opções exibidas na consulta:
def exibir_opcoes():
    print("1. Editar")
    print("2. Remover")
    print("3. Voltar")
    return input("Escolha uma opção: ")

def autenticacao():
    os.system('cls')
    
    try:
        # Inicia uma conexão ao banco de dados:
        conexao = conectar_bd()

        usuario = input("Digite seu usuário: ").upper()
        senha = input("Digite sua senha: ").upper()

        dados_autenticacao = get_tabela(conexao, 'login')

        if [usuario, senha] == ['ADMIN', 'ADMIN']:
            return True
        
        for linha in dados_autenticacao:
            if [usuario, senha] == [linha['usuario'], linha['senha']]:
                return linha['id_funcionario']

        print("Usuário ou senha inválidos.")
        sleep(0.25)
        return None
    
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        sleep(0.25)
        return None

    finally:
        # Fecha a conexão ao banco de dados:
        conexao.close()
    
# 
def verifica_id_existente(tabela, id):
    try:
        conexao = conectar_bd()
        cursor = conexao.cursor()

        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tabela}' LIMIT 1")
        id_name = "".join(cursor.fetchall()[0])
        
        cursor.execute(f"SELECT * FROM {tabela} WHERE {id_name} = {id}")
        id_tabela = cursor.fetchone()
        return id_tabela
    
    except Exception as e:
        print(f"Erro : {e}")
        return False
    
    finally:
        cursor.close()
        conexao.close()


# ===============================================================================   
# Execução do sistema:
if __name__ == "__main__":
    criar_tabelas()
    
    while not autenticacao():
        continue
    
    menu()
