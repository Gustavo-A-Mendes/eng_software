from crud import *
from datetime import datetime, timedelta

# ============================================================
# Cadastra um funcionário:
def cadastrar_funcionario():
    try:
        # Cria conexão e executa o comando:
        conexao = conectar_bd()

        os.system('cls')
        print("DADOS PESSOAIS DO FUNCIONÁRIO")
        nome = input("Nome Completo: ").upper()
        cpf = input("CPF (somente números): ").upper()
        email = input("E-mail: ").upper()
        telefone = input("Telefone (somente números): ").upper()
        cargo = input("Cargo: ").upper()

        """ 
        Nesse sistema, vamos ter apenas um gerente e ele deve ser
        cadastrado primeiro. 
        """

        # Verifica se já existe um gerente:
        existe_gerente = conta_cargo("GERENTE")

        if existe_gerente and cargo == "GERENTE":
            print("Já existe um gerente. Não é possível adicionar outro.")
            sleep(0.25)
            return False
        
        elif not existe_gerente and cargo != "GERENTE":
            print("Cadastre o Gerente primeiro!")
            sleep(0.25)
            return False
        
        # retorna o id do funcionário que é gerente:
        id_gerente = get_gerenteID() 
        print()
        
        # Cadastra novo funcionário:
        dados = [nome, cpf, email, telefone, cargo, id_gerente]
        id_gerado = post_tabela(conexao, "funcionario", dados, autocommit=False)

        # Criar uma autenticação de email e senha:
        usuario = input("Nome de usuário: ").upper()

        while True:
            os.system('cls')
            senha = input("Crie uma senha: ").upper()
            senha_conf = input("Repita a senha: ").upper()

            if (senha_conf == senha):
                            # usuário, senha, tipo_usuario, id_cliente, id_funcionario)
                dados_login = [usuario, senha, id_gerado]
                if post_tabela(conexao, "login", dados_login, autocommit=True):
                    return True
            
            print("Senhas não conferem. Tente novamente.")

    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return False
    
    finally:
        # Fecha a conexão:
        conexao.close()
    
# Cadastra um novo cliente:
def cadastrar_cliente():
    try:
        # Abre a conexão com o banco de dados:
        conexao = conectar_bd()

        os.system('cls')
        print("DADOS PESSOAIS DO CLIENTE")
        nome = input("Nome Completo: ").upper()
        cpf = input("CPF: ").upper()
        email = input("E-mail: ").lower()
        cnh = input("CNH: ").upper()
        telefone = input("Telefone (somente números): ").upper()
        print()
        print("ENDEREÇO DO CLIENTE")
        cidade = input("Cidade: ").upper()
        bairro = input("Bairro: ").upper()
        rua = input("Rua: ").upper()
        numero = input("Número: ").upper()
        # status_aluguel = False
        print()
        
        # Cadastra novo cliente:
        dados = [nome, cpf, email, cnh, telefone, cidade, bairro, rua, numero]
        if post_tabela(conexao, "cliente", dados):
            return True
        return False

    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return False
    
    finally:
        # Fecha a conexão:
        conexao.close()
    
# Cadastra um novo carro:
def cadastrar_carro():
    try:
        # Abre a conexão com o banco de dados:
        conexao = conectar_bd()

        os.system('cls')
        print("DADOS DO CARRO")
        modelo = input("Modelo: ").upper()
        marca = input("Marca: ").upper()
        diaria = float(input("Diaria: "))
        # disponibilidade = True
        print()
        
        # Cadastra novo carro:
        dados = [modelo, marca, diaria]
        post_tabela(conexao, "carro", dados)
        return True
    
    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return False
    
    finally:
        # Fecha a conexão:
        conexao.close()

# Registra uma nova locação
def cadastrar_aluguel():
    try:
        # Abre a conexão com o banco de dados:
        conexao = conectar_bd()

        #  Solicita ID do Funcionário responsável pelo aluguel:
        os.system('cls')
        print("\n=== Sistema de Aluguel de Carros ===")
        
        print("\n=== Lista de Funcionarios ===")
        
        exibe_tabela('funcionario')

        id_func = int(input("\n Digite o ID do Funcionario responsável pelo aluguel: "))
        
        #  Solicita ID do Cliente que está alugando:
        os.system('cls')
        print("\n=== Sistema de Aluguel de Carros ===")
        
        print("\n=== Lista de Clientes ===")

        exibe_tabela('cliente')

        id_cli = int(input("\n Digite o ID do Cliente do aluguel: "))

        #  Solicita ID do Carro alugado:
        os.system('cls')
        print("\n=== Sistema de Aluguel de Carros ===")
        
        exibe_tabela('carro')

        print("\n=== Lista de Carros ===")
        
        id_car = int(input("\n Digite o ID do Carro do aluguel: "))

        # ==================================================
        os.system('cls')
        print("\n=== Sistema de Aluguel de Carros ===")

        data_ini_str = input("Data de Início (DD/MM/AAAA): ")
        tempo_aluguel = int(input("Quantos dias de aluguel? "))
    
        # Converte a string da data em um formato datetime:
        data_ini = datetime.strptime(data_ini_str, "%d/%m/%Y").date()
        # Calcula data final do aluguel:
        data_fim = data_ini + timedelta(days=tempo_aluguel)
        
        preco_total = preco_carro(id_car, tempo_aluguel)

        # status = True
        print()

        dados = [id_func, id_cli, id_car, data_ini, data_fim, preco_total]

        # Registra Aluguel e atualiza os dados dos envolvidos:
        if post_tabela(conexao, "aluguel", dados):
            inicia_aluguel(id_cli, id_car)
        return True

    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return False
    
    finally:
        # Fecha a conexão:
        conexao.close()

# ==================================================
# Modifica os dados de um funcionário:
def edita_funcionario(id):
    try:
        # Abre a conexão:
        conexao = conectar_bd()

        dados_atuais = dados_tabela("funcionario", id)

        exibe_dados(dados_atuais)
        print()
        
        dados = {
            "nome": input("Nome: ").upper() or dados_atuais['nome'],
            "cpf": input("CPF (somente números): ").upper() or dados_atuais['cpf'],
            "telefone": input("Telefone (somente números): ").upper() or dados_atuais['telefone'],
            "cargo": input("Cargo: ").upper() or dados_atuais['cargo'],
        }
        
        update_tabela(conexao, "funcionario", id, dados)
        return True

    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return False
    
    finally:
        # Fecha a conexão:
        conexao.close()
    
# Modifica os dados de um cliente:
def edita_cliente(id):
    try:
        # Inicia uma conexão ao banco de dados:
        conexao = conectar_bd()

        dados_atuais = dados_tabela("cliente", id)

        exibe_dados(dados_atuais)
        print()

        dados = {
            "nome": input("Nome: ").upper() or dados_atuais['nome'],
            "cpf": input("CPF (somente números): ").upper() or dados_atuais['cpf'],
            "cnh": input("CNH (somente letra e números): ").upper() or dados_atuais['cnh'],
            "telefone": input("Telefone (somente números): ").upper() or dados_atuais['telefone'],
            "cidade": input("Cidade: ").upper() or dados_atuais['cidade'],
            "bairro": input("Bairro: ").upper() or dados_atuais['bairro'],
            "rua": input("Rua: ").upper() or dados_atuais['rua'],
            "numero": input("Número: ").upper() or dados_atuais['numero'],
            "status_aluguel": dados_atuais['status_aluguel']
        }
        
        update_tabela(conexao, "cliente", id, dados)
        return True

    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return False
    
    finally:
        # Fecha a conexão:
        conexao.close()
    
# Modifica os dados de um carro:
def edita_carro(id):
    try:
        # Inicia uma conexão ao banco de dados:
        conexao = conectar_bd()

        dados_atuais = dados_tabela("carro", id)

        exibe_dados(dados_atuais)
        print()

        dados = {
            "modelo": input("Modelo: ").upper() or dados_atuais['modelo'],
            "marca": input("Marca: ").upper() or dados_atuais['marca'],
            "diaria": float(input("Valor da Diária: ")) or dados_atuais['diaria']
        }
        
        update_tabela(conexao, "carro", id, dados)
        return True

    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return False
    
    finally:
        # Fecha a conexão:
        conexao.close()
    
# Modifica os dados de um aluguel:
def edita_aluguel(id):
    try:
        # Inicia uma conexão ao banco de dados:
        conexao = conectar_bd()

        dados_atuais = dados_tabela("aluguel", id)

        exibe_dados(dados_atuais)
        print()
        
        nova_data_ini_str = input("Data de Início (DD/MM/AAAA): ")
        nova_data_ini = datetime.strptime(nova_data_ini_str, "%d/%m/%Y").date()
        novo_tempo_aluguel = int(input("Quantos dias de aluguel? "))

        nova_data_fim = nova_data_ini + timedelta(days=novo_tempo_aluguel)

        diaria = dados_atuais['preco_total'] / (dados_atuais['data_fim'] - dados_atuais['data_inicio']).days

        novo_status = input("Status do Aluguel (True/False): ")


        dados = {
            "data_inicio": nova_data_ini or dados_atuais['data_inicio'],
            "data_fim": nova_data_fim or dados_atuais['data_fim'],
            "preco_total": diaria * novo_tempo_aluguel or dados_atuais['preco_total'],
            "status": novo_status or dados_atuais['status']
        }

        if update_tabela(conexao, "aluguel", id, dados) and novo_status == False:
            encerra_aluguel(dados_atuais)
            return True
    
    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.5)
        return False

    finally:
        # Fecha a conexão:
        conexao.close()

