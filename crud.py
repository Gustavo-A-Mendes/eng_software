import psycopg2
from psycopg2.extras import RealDictCursor
import csv
import os
from time import sleep


# Configurações do banco de dados
DB_NAME = "locadora_carro"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

# Estabelece conexão no banco de dados:
def conectar_bd():
    """ 
    Estabele e retorna uma conexão no banco de dados.
    """
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Cria as tabelas no banco de dados, caso ainda não exista:
def criar_tabelas():
    """ 
    Cria as tabelas no banco de dados, caso ainda não exista. 
    """
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionario(
            id_funcionario SERIAL,
            nome VARCHAR(80) not null,
            cpf VARCHAR(11) not null,
            telefone VARCHAR(11) not null,
            cargo VARCHAR(30) not null,
            id_gerente INTEGER,
            
            PRIMARY key (id_funcionario),
                   
            FOREIGN key (id_gerente) REFERENCES funcionario
            ON UPDATE CASCADE ON DELETE CASCADE
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
            status_aluguel BOOLEAN default FALSE,
            
            PRIMARY key (id_cliente)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carro(
            id_carro SERIAL,
            modelo VARCHAR(30) not null,
            marca VARCHAR(30) not null,
            diaria NUMERIC(6, 2) not null,
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
            data_inicio DATE not null,
            data_fim DATE,
            preco_total NUMERIC(7, 2) not null,
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
            return False
        else:
            # Adiciona os valores na tabela:
            cursor.execute(f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({valores})", tuple(dados_envio))
            conexao.commit()
            return True

    except Exception as e:
        print(f"Erro ao atualizar: {e}")
        return False

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
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute(f"SELECT * FROM {tabela}")
        clientes = cursor.fetchall()
        # Caso o resultado seja vazio, encerra a função:
        if not clientes:
            print("Nenhum cliente cadastrado.")
            return None
        
        return clientes
        

    except Exception as e:
        print(f"Erro ao atualizar: {e}")
        clientes = None
    
    finally:
        # Encerra conexão:
        cursor.close()
        conexao.close()
 
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
            return False
        else:
            cursor.execute(query, tuple(dados_envio.values()))
            conexao.commit()
            print(f"Registro {id} atualizado na tabela '{tabela}' com sucesso.")
            return True

    except Exception as e:
        print(f"Erro ao atualizar: {e}")
        return False
    
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
                return False

        else:
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tabela}' LIMIT 1")
            id_name = "".join(cursor.fetchall()[0])

            query = f"DELETE FROM {tabela} WHERE {id_name} = {id}"
            message = f"Registro {id} removido da tabela '{tabela}' com sucesso."

        cursor.execute(query)
        print(message)
        conexao.commit()
        return True

    except Exception as e:
        print(f"Erro ao remover registro: {e}")
        return False
    
    finally:
        cursor.close()
        conexao.close()

# ===============================================================================
# Retorna uma lista de dados de uma tabela:
def listar_tabela(tabela):
    conexao = conectar_bd()
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute(f"SELECT * FROM {tabela}")
        dados_tabela = cursor.fetchall()
        return dados_tabela
    
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return None

    finally:
        cursor.close()
        conexao.close()

# Exibe a lista de uma tabela:
def exibe_tabela(nome_tabela):
    dados_tabela = listar_tabela(f"{nome_tabela}")

    if not dados_tabela:
        print(f"Nenhum(a) {nome_tabela} cadastrado(a).")
        return False
    else:
        colunas = f"({', '.join([coluna.upper() for coluna in dados_tabela[0].keys()])})"
        print(f"{colunas}")
        
        for linha in dados_tabela:
            valores = f"({', '.join([str(valor).upper() for valor in linha.values()])})"
            print(valores)
        print()
        
        return True
    
# Exibe os dados de uma linha:
def exibe_dados(dado):

    colunas = f"({', '.join([coluna.upper() for coluna in dado.keys()])})"
    
    valores = f"({', '.join([str(valor).upper() for valor in dado.values()])})"
    
    print(f"{colunas}\n{valores}")

# Busca o ID do gerente daquele funcionário:
def get_gerenteID():
    conexao = conectar_bd()
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    cursor.execute(f"SELECT id_funcionario FROM funcionario WHERE cargo = 'GERENTE'")

    gerente = cursor.fetchone()
    id_gerente = None
    if gerente:
        id_gerente = gerente['id_funcionario']
    
    cursor.close()
    conexao.close()

    return id_gerente

# Conta quantos funcionários pertencem a um cargo:
def conta_cargo(cargo):
    conexao = conectar_bd()
    cursor = conexao.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM funcionario WHERE cargo = '{cargo}';")
    cargo_func = cursor.fetchone()[0]
    
    cursor.close()
    conexao.close()

    return cargo_func

# Calcula o preço do aluguel:
def preco_carro(id_carro, tempo_aluguel):
    conexao = conectar_bd()
    cursor = conexao.cursor()

    cursor.execute(f"SELECT diaria FROM carro WHERE id_carro = {id_carro};")

    diaria = cursor.fetchone()[0]

    cursor.close()
    conexao.close()

    return diaria * tempo_aluguel

# Retorna um dicionário dos dados de uma linha:
def dados_tabela(tabela, id):
    conexao = conectar_bd()
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    cursor.execute(f"SELECT * FROM {tabela} WHERE id_{tabela} = {id}")

    dados_id = cursor.fetchone()

    cursor.close()
    conexao.close()

    return dados_id

def inicia_aluguel(id_cliente, id_carro):
    update_tabela('cliente', id_cliente, {'status_aluguel': True})
    update_tabela('carro', id_carro, {'disponibilidade': False})

def encerra_aluguel(dados_aluguel):
    id_cli = dados_aluguel['id_cliente']
    id_car = dados_aluguel['id_carro']

    update_tabela('cliente', id_cli, {'status_aluguel': False})
    update_tabela('carro', id_car, {'disponibilidade': True})


# Importa dados dos arquivos ".csv" para o banco de dados:
def importar_csv_para_bd():
    """Importa dados de um arquivo CSV para a tabela especificada."""
    conexao = conectar_bd()
    cursor = conexao.cursor()

    tabelas = {"id_funcionario": "funcionario", "id_cliente": "cliente", "id_carro": "carro", "id_aluguel": "aluguel"}
    
    for id, nome_tabela in tabelas.items():
        try:
            with open("./backup/"+nome_tabela+".csv", mode="r", encoding="utf-8") as arquivo:
                leitor_csv = csv.reader(arquivo)
                colunas = next(leitor_csv)  # Lê a primeira linha (nomes das colunas)

                # Criando um placeholder para os valores (%s, %s, ...)
                placeholders = ", ".join(["%s"] * len(colunas))
                query = f"INSERT INTO {nome_tabela} ({', '.join(colunas)}) VALUES ({placeholders}) ON CONFLICT ({id}) DO NOTHING;"

                for linha in leitor_csv:
                    linha_corrigida = [None if valor.strip() == "" else valor for valor in linha]
                    cursor.execute(query, linha_corrigida)

            conexao.commit()
            print(f"Dados do arquivo \"{nome_tabela+'.csv'}\" importados para a tabela \"{nome_tabela}\" com sucesso!")


        except Exception as e:
            print(f"Erro ao importar dados: {e}")

    cursor.close()
    conexao.close()
    sleep(3)

# Exporta dodas do banco de dados, para um arquivo ".csv":
def exportar_tabelas_para_csv():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    tabelas = ["funcionario", "cliente", "carro", "aluguel"]

    for tabela in tabelas:
        arquivo_csv = f"./backup/{tabela}.csv"
        
        # Executa a consulta para pegar todos os dados da tabela
        cursor.execute(f"SELECT * FROM {tabela}")
        dados = cursor.fetchall()  # Recupera todos os registros
        
        # Obtém os nomes das colunas
        colunas = [desc[0] for desc in cursor.description]

        # Escreve os dados no arquivo CSV
        with open(arquivo_csv, mode="w+", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(colunas)  # Escreve os cabeçalhos das colunas
            writer.writerows(dados)   # Escreve os dados

        print(f"Tabela '{tabela}' exportada para '{arquivo_csv}'")

    cursor.close()
    conexao.close()