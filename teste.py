import psycopg2
import csv
import os

# Configurações do banco de dados
DB_NAME = "locadora_carro"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

def conectar_bd():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def criar_tabelas():
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionario(
            id_funcionario SERIAL,
            nome VARCHAR(80) not null,
            cpf VARCHAR(11) not null,
            telefone VARCHAR(11) not null,
            PRIMARY key (id_funcionario)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cliente(
            id_cliente SERIAL,
            nome VARCHAR(80) not null,
            cpf VARCHAR(11) not null,
            cnh VARCHAR(11) not null,
            telefone VARCHAR(11) not null,
            cidade VARCHAR(50) not null,
            bairro VARCHAR(50) not null,
            rua VARCHAR(50) not null,
            numero VARCHAR(5) not null,
            PRIMARY key (id_cliente)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carro(
            id_carro SERIAL,
            modelo VARCHAR(30) not null,
            marca VARCHAR(30) not null,
            diaria NUMERIC(6, 2) default 0000.00,
            disponibilidade BOOLEAN default TRUE,
            PRIMARY	key (id_carro)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aluguel(
            id_aluguel SERIAL,
            id_funcionario INTEGER not null,
            id_carro INTEGER not null,
            id_cliente INTEGER not null,
            preco_total NUMERIC(7, 2) not null,
            data_inicio TIMESTAMP not null,
            data_fim TIMESTAMP,
            status BOOLEAN default TRUE,
            PRIMARY key (id_aluguel),
            
            FOREIGN key (id_funcionario) REFERENCES funcionario 
            ON UPDATE CASCADE ON DELETE CASCADE,
            
            FOREIGN key (id_carro) REFERENCES carro
            ON UPDATE CASCADE ON DELETE CASCADE,
            
            FOREIGN key (id_cliente) REFERENCES cliente
            ON UPDATE CASCADE ON DELETE CASCADE
        );
    ''')
    conexao.commit()
    cursor.close()
    conexao.close()

def menu():
    while True:
        print("\n=== Sistema de Aluguel de Carros ===")
        print("1. Cadastro")
        print("2. Consulta")
        print("3. Importar Dados")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        # SUBMENU CADASTRO
        if opcao == "1":
            while True:
                os.system('cls') 
                print("\n=== Sistema de Aluguel de Carros ===")
                print("1. Registrar Aluguel")
                print("2. Cadastrar Cliente")
                print("3. Cadastrar Veículo")
                print("4. Cadastrar Funcionário")
                print("5. Voltar")
                opcao_submenu = input ("Escolha uma opção: ")

                if opcao_submenu == "1":
                    registrar_aluguel()
                    # edita_cliente()
                    # delete_tabela("cliente")
                elif opcao_submenu == "2":
                    cadastrar_cliente()
                elif opcao_submenu == "3":
                    cadastrar_carro()
                elif opcao_submenu == "4":
                    cadastrar_funcionario()
                elif opcao_submenu == "5":
                    break

        # SUBMENU CONSULTA
        elif opcao == "2":
            while True:
                os.system('cls')
                print("\n=== Sistema de Aluguel de Carros ===")
                print("1. Consultar Aluguéis")
                print("2. Listar Clientes") # MENU SECUNDARIO PARA BUSCAR E EDITAR UM CLIENTE
                print("3. Listar Veículos") # MENU SECUNDARIO PARA BUSCAR E EDITAR UM VEÍCULO
                print("4. Listar Funcionários") # MENU SECUNDARIO PARA BUSCAR E EDITAR UM FUNCIONÁRIO
                print("5. Voltar")
                opcao_submenu = input ("Escolha uma opção: ")
                
                # SUBMENU ALUGUEL
                if opcao_submenu == "1":
                    while True:
                        os.system('cls')
                        print("\n=== Sistema de Aluguel de Carros ===")
                        consultar_alugueis()
                        ret = exibir_opcoes()
                        if ret == "1":
                            id = input("Especifique um ID: ")
                            if verificar_id_existente("aluguel", id):
                                editar_aluguel(id)
                            else:
                                print("ID não encontrado.")
                        elif ret == "2":
                            id = input("Especifique um ID: ")
                            if verificar_id_existente("aluguel", id):
                                delete_tabela("aluguel", id)
                            else:
                                print("ID não encontrado.")
                        elif ret == "3":
                            break
                        else: 
                            print("Opção inválida.")

                # SUBMENU CLIENTE
                elif opcao_submenu == "2":
                    while True:
                        os.system('cls')
                        print("\n=== Sistema de Aluguel de Carros ===")
                        exibe_clientes()
                        ret = exibir_opcoes()
                        if ret == "1":
                            id = input("Especifique um ID: ")
                            if verificar_id_existente("cliente", id):
                                editar_cliente(id)
                            else:
                                print("ID não encontrado.")
                        elif ret == "2":
                            id = input("Especifique um ID: ")
                            if verificar_id_existente("cliente", id):
                                delete_tabela("cliente", id)
                            else:
                                print("ID não encontrado.")
                        elif ret == "3":
                            break
                        else: 
                            print("Opção inválida.")

                # SUBMENU CARROS
                elif opcao_submenu == "3":
                    while True:
                        os.system('cls')
                        print("\n=== Sistema de Aluguel de Carros ===")
                        exibe_carros()
                        ret = exibir_opcoes()
                        if ret == "1":
                            id = input("Especifique um ID: ")
                            if verificar_id_existente("carro", id):
                                editar_carro(id)
                            else:
                                print("ID não encontrado.")
                        elif ret == "2":
                            id = input("Especifique um ID: ")
                            if verificar_id_existente("carro", id):
                                delete_tabela("carro", id)
                            else:
                                print("ID não encontrado.")
                        elif ret == "3":
                            break
                        else: 
                            print("Opção inválida.")

                # SUBMENU FUNCIONÁRIOS
                elif opcao_submenu == "4":
                    while True:
                        os.system('cls')
                        print("\n=== Sistema de Aluguel de Carros ===")
                        exibe_funcionarios()
                        ret = exibir_opcoes()
                        if ret == "1":
                            id = input("Especifique um ID: ")
                            if verificar_id_existente("funcionario", id):
                                editar_funcionario(id)
                            else:
                                print("ID não encontrado.")
                        elif ret == "2":
                            id = input("Especifique um ID: ")
                            if verificar_id_existente("funcionario", id):
                                delete_tabela("funcionario", id)
                            else:
                                print("ID não encontrado.")
                        elif ret == "3":
                            break
                        else: 
                            print("Opção inválida.")

                elif opcao_submenu == "5":
                    break

                else:
                    print("Opção inválida.")
            
        # IMPORTAR DADOS
        elif opcao == "3":
            tabela = input("Nome da tabela para importar (clientes, veiculos, alugueis): ").strip()
            arquivo_csv = input("Nome do arquivo CSV (ex: clientes.csv): ").strip()
            importar_csv_para_bd(tabela, arquivo_csv)

        # SAIR
        elif opcao == "4":
            exportar_tabelas_para_csv()
            break
        
        else:
            print("Opção inválida! Tente novamente.")

# ============================== DEFINIÇÃO DO CRUD ==============================   
# (CREATE)
def post_tabela(tabela, dados_envio):
    """
    Envia os dados para uma tabela do banco de dados.

    :param tabela: Nome da tabela.
    :param dado_envio: Lista dos valores que devem ser adicionados.
    """
    
    # Cria conexão e executa o comando:
    conexao = conectar_bd()
    cursor = conexao.cursor()

    valores = ', '.join(["%s"] * len(dados_envio))
    
    try:
        # Obtém as colunas da tabela (excluindo a coluna SERIAL, se houver):
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tabela}' AND column_default IS NULL")
        colunas = [coluna[0] for coluna in cursor.fetchall()]
        if not colunas:
            print("Erro: Não foi possível obter as colunas da tabela.")
        else:
            # Adiciona os valores na tabela:
            cursor.execute(f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({valores})", tuple(dados_envio))
            conexao.commit()

    except Exception as e:
        print(f"Erro ao atualizar: {e}")

    finally:
        # Encerra conexão:
        cursor.close()
        conexao.close()

# (READ)
def get_tabela(tabela):
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
 
# (UPDATE)
def update_tabela(tabela, id, dados_envio):
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
    colunas_valores = [f"{coluna} = %s" for coluna in dados_envio.keys()]

    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tabela}' LIMIT 1")
    id_name = "".join(cursor.fetchall()[0])
    query = f"UPDATE {tabela} SET {', '.join(colunas_valores)} WHERE {id_name} = {id}"

    try:
        if not dados_envio:
            print("Nenhum dado para atualizar.")
        else:
            cursor.execute(query, tuple(dados_envio.values()))
            conexao.commit()
            print(f"Registro {id} atualizado na tabela '{tabela}' com sucesso.")

    except Exception as e:
        print(f"Erro ao atualizar: {e}")
    
    finally:
        cursor.close()
        conexao.close()

# (DELETE)
def delete_tabela(tabela, id = None):
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
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tabela}' LIMIT 1")
            id_name = "".join(cursor.fetchall()[0])

            query = f"DELETE FROM {tabela} WHERE {id_name} = {id}"
            message = f"Registro {id} removido da tabela '{tabela}' com sucesso."

        cursor.execute(query)
        print(message)
        conexao.commit()

    except Exception as e:
        print(f"Erro ao remover registro: {e}")
    
    finally:
        cursor.close()
        conexao.close()

# ============================================================   
# Cadastra um novo cliente:
def cadastrar_cliente():
    print("DADOS PESSOAIS DO CLIENTE")
    nome = input("Nome Completo: ").upper()
    cpf = input("CPF: ").upper()
    cnh = input("CNH: ").upper()
    telefone = input("Telefone (somente números): ").upper()
    print()
    print("ENDEREÇO DO CLIENTE")
    cidade = input("Cidade: ").upper()
    bairro = input("Bairro: ").upper()
    rua = input("Rua: ").upper()
    numero = input("Número: ").upper()
    print()
    
    dados = [nome, cpf, cnh, telefone, cidade, bairro, rua, numero]

    post_tabela("cliente", dados)

# Cadastra um novo carro:
def cadastrar_carro():
    print("DADOS DO CLIENTE")
    modelo = input("Modelo: ").upper()
    marca = input("Marca: ").upper()
    diaria = float(input("Diaria: "))
    disponibilidade = 1
    print()
    
    dados = [modelo, marca, diaria, disponibilidade]

    post_tabela("carro", dados)

# Cadastra um funcionário:
def cadastrar_funcionario():
    print("DADOS PESSOAIS DO FUNCIONÁRIO")
    nome = input("Nome Completo: ").upper()
    cpf = input("CPF: ").upper()
    telefone = input("Telefone (somente números): ").upper()
    print()
    
    dados = [nome, cpf, telefone]

    post_tabela("funcionarios", dados)

# Modifica os dados de um cliente:
def edita_cliente():
    dados = {
        "nome": input("Nome: ").upper(),
        "cpf": input("CPF: ").upper(),
        "cnh": input("CNH: ").upper(),
    }
    
    update_tabela("cliente", 2, dados)

# Registra uma nova locação
def registrar_aluguel():
    print("DADOS PESSOAIS DO CLIENTE")
    id_func = input("CPF: ").upper()
    id_car = input("CNH: ").upper()
    id_cli = input("Nome Completo: ").upper()
    data_ini = input("Cidade: ").upper()
    data_fim = input("Bairro: ").upper()
    preco_total = input("Telefone (somente números): ").upper()
    status = input("Rua: ").upper()
    print()

    dados = [id_func, id_car, id_cli, data_ini, data_fim, preco_total, status]

    post_tabela("aluguel", dados)

# Retorna uma lista de dados de uma tabela:
def listar_tabela(tabela):
    conexao = conectar_bd()
    cursor = conexao.cursor()

    try:
        cursor.execute(f"SELECT * FROM {tabela}")
        dados_tabela = cursor.fetchall()
    
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        dados_tabela = None

    finally:
        cursor.close()
        conexao.close()
        return dados_tabela

# Exibe a lista de clientes cadastrados:
def exibe_clientes():
    dados_clientes = listar_tabela("cliente")
    
    if not dados_clientes:
        print("Nenhum cliente cadastrado.")
    else:
        print("\n=== Lista de Clientes ===")
        for cliente in dados_clientes:
            print(cliente)

# Exibe a lista de carros cadastrados:
def exibe_carros():
    dados_carros = listar_tabela("cliente")
    
    if not dados_carros:
        print("Nenhum carro cadastrado.")
    else:
        print("\n=== Lista de Carros ===")
        for carro in dados_carros:
            print(carro)

def importar_csv_para_bd(tabela, arquivo_csv):
    """Importa dados de um arquivo CSV para a tabela especificada."""
    conexao = conectar_bd()
    cursor = conexao.cursor()

    tabelas = ["funcionario", "cliente", "carro", "aluguel"]

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

    tabelas = ["funcionario", "cliente", "carro", "aluguel"]

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

def exibir_opcoes():
    print("1. Editar")
    print("2. Remover")
    print("3. Voltar")
    return input("Escolha uma opção: ")

def verificar_id_existente (cursor, tabela, id):
    cursor.execute(f"SELECT * FROM {tabela} WHERE id = {id}")
    return cursor.fetchone() is not None

if __name__ == "__main__":
    criar_tabelas()
    menu()
