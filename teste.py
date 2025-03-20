import psycopg2
import csv

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
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            telefone VARCHAR(15) NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS veiculos (
            id SERIAL PRIMARY KEY,
            modelo VARCHAR(100) NOT NULL,
            ano INT NOT NULL,
            disponivel BOOLEAN DEFAULT TRUE
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alugueis (
            id SERIAL PRIMARY KEY,
            cliente_id INT REFERENCES clientes(id),
            veiculo_id INT REFERENCES veiculos(id),
            data_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_fim TIMESTAMP
        );
    ''')
    conexao.commit()
    cursor.close()
    conexao.close()

def menu():
    while True:
        print("\n=== Sistema de Aluguel de Carros ===")
        print("1. Cadastrar Cliente")
        print("2. Cadastrar Veículo")
        print("3. Registrar Aluguel")
        print("4. Registrar Devolução")
        print("5. Listar Clientes")
        print("6. Listar Veículos")
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

def cadastrar_cliente():
    nome = input("Nome do cliente: ")
    telefone = input("Telefone do cliente: ")
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO clientes (nome, telefone) VALUES (%s, %s)", (nome, telefone))
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
    cursor.execute("SELECT * FROM clientes")
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
