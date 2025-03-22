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
            id_cliente INTEGER not null,
            id_carro INTEGER not null,
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login(
            id_login SERIAL,
            usuario VARCHAR(30) not null,
            senha VARCHAR(30) not null,            
            tipo_usuario VARCHAR(15) not null CHECK (tipo_usuario IN ('cliente', 'funcionario')),
            
            id_cliente INTEGER,
            id_funcionario INTEGER,
            
            PRIMARY key (id_login),
            
            CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES cliente ON DELETE CASCADE,
            CONSTRAINT fk_funcionario FOREIGN KEY (id_funcionario) REFERENCES funcionario ON DELETE CASCADE,
            CONSTRAINT chk_tipo_usuario CHECK (
                (id_cliente IS NOT NULL AND id_funcionario IS NULL) OR
                (id_cliente IS NULL AND id_funcionario IS NOT NULL)
            )
        );
    ''')
    conexao.commit()
    cursor.close()
    conexao.close()

# ============================== DEFINIÇÃO DO CRUD ==============================   
# (CREATE)
def post_tabela(conexao, tabela, dados_envio, autocommit=True):
    """
    Envia os dados para uma tabela do banco de dados.

    :param tabela: Nome da tabela.
    :param dado_envio: Lista dos valores que devem ser adicionados.
    """
    
    try:
        cursor = conexao.cursor()

        valores = ', '.join(["%s"] * len(dados_envio))

        # Obtém as colunas da tabela (excluindo a coluna SERIAL, se houver):
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tabela}' AND column_default IS NULL")
        colunas = [coluna[0] for coluna in cursor.fetchall()]
        if not colunas:
            print("Erro: Não foi possível obter as colunas da tabela.")
            sleep(0.25)
            return None
        else:
            # Adiciona os valores na tabela:
            cursor.execute(f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({valores}) RETURNING id_{tabela}", tuple(dados_envio))
            id_gerado = cursor.fetchone()[0]

            if autocommit:
                conexao.commit()
            return id_gerado

    except Exception as e:
        print(f"Erro ao atualizar: {e}")
        sleep(0.25)
        return None

    finally:
        cursor.close()

# (READ)
def get_tabela(conexao, tabela):
    """
    Solicita os dados de uma tabela do banco de dados.

    :param tabela: Nome da tabela.
    """
    
    try:
        cursor = conexao.cursor(cursor_factory=RealDictCursor)

        cursor.execute(f"SELECT * FROM {tabela}")
        dados_tabela = cursor.fetchall()
        return dados_tabela
        
    except Exception as e:
        print(f"Erro ao atualizar: {e}")
        sleep(0.25)
        return None
    
    finally:
        cursor.close()
 
# (UPDATE)
def update_tabela(conexao, tabela, id, dados_envio):
    """
    Atualiza um registro em uma tabela específica.

    :param tabela: Nome da tabela.
    :param id: ID do registro a ser atualizado.
    :param dados_envio: Dicionário com as colunas e valores a serem atualizados.
    """
    
    try:
        cursor = conexao.cursor()
        
        # Cria os pares "coluna = valor" dinamicamente:
        colunas_valores = [f"{coluna} = %s" for coluna in dados_envio.keys()]

        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tabela}' LIMIT 1")
        id_name = "".join(cursor.fetchall()[0])
        query = f"UPDATE {tabela} SET {', '.join(colunas_valores)} WHERE {id_name} = {id}"

        if not dados_envio:
            print("Nenhum dado para atualizar.")
            sleep(0.25)
            return False
        else:
            cursor.execute(query, tuple(dados_envio.values()))
            conexao.commit()
            print(f"Registro {id} atualizado na tabela '{tabela}' com sucesso.")
            return True

    except Exception as e:
        print(f"Erro ao atualizar: {e}")
        sleep(0.25)
        return False
    
    finally:
        cursor.close()

# (DELETE)
def delete_tabela(tabela, id = None):
    """
    Remove um registro de uma tabela específica.

    :param tabela: Nome da tabela.
    :param id: ID do registro a ser removido.
    """
    
    try:
        # Inicia uma conexão ao banco de dados:
        conexao = conectar_bd()
        cursor = conexao.cursor()

        if id is None:
            confirmacao = input(f"Tem certeza que deseja excluir TODOS os registros da tabela '{tabela}'? (sim/não): ").strip().lower()
            if confirmacao == "sim":
                query = f"DELETE FROM {tabela}"
                message = f"TODOS os registros da tabela '{tabela}' foram removidos!"
            else:
                print("Operação cancelada.")
                sleep(0.25)
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
        sleep(0.25)
        return False
    
    finally:
        # Fecha a conexão:
        cursor.close()
        conexao.close()

# ===============================================================================
# Exibe as linhas uma tabela:
def exibe_tabela(nome_tabela):
    try:
        # Inicia uma conexão:
        conexao = conectar_bd()

        dados_tabela = get_tabela(conexao, f"{nome_tabela}")

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
    
    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return False
    
    finally:
        # Fecha a conexão:
        conexao.close()

# Exibe os dados de uma linha:
def exibe_dados(dado):
    try:
        colunas = f"({', '.join([coluna.upper() for coluna in dado.keys()])})"
        valores = f"({', '.join([str(valor).upper() for valor in dado.values()])})"
        
        print(f"{colunas}\n{valores}")
    
    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return False

# Busca o ID do gerente daquele funcionário:
def get_gerenteID():
    try:
        conexao = conectar_bd()
        cursor = conexao.cursor(cursor_factory=RealDictCursor)

        cursor.execute(f"SELECT id_funcionario FROM funcionario WHERE cargo = 'GERENTE'")

        gerente = cursor.fetchone()
        if gerente:
            id_gerente = gerente['id_funcionario']
            return id_gerente
    
    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return None
    
    finally:
        cursor.close()
        conexao.close()

# Conta quantos funcionários pertencem a um cargo:
def conta_cargo(cargo):
    try:
        conexao = conectar_bd()
        cursor = conexao.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM funcionario WHERE cargo = '{cargo}';")
        cargo_func = cursor.fetchone()[0]
        return cargo_func
    
    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return None
    
    finally:
        cursor.close()
        conexao.close()

# Calcula o preço do aluguel:
def preco_carro(id_carro, tempo_aluguel):
    try:
        conexao = conectar_bd()
        cursor = conexao.cursor()

        cursor.execute(f"SELECT diaria FROM carro WHERE id_carro = {id_carro};")

        diaria = cursor.fetchone()[0]
        return diaria * tempo_aluguel
    
    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return None
    
    finally:
        cursor.close()
        conexao.close()

# Retorna um dicionário dos dados de uma linha:
def dados_tabela(tabela, id):
    try:
        conexao = conectar_bd()
        cursor = conexao.cursor(cursor_factory=RealDictCursor)

        cursor.execute(f"SELECT * FROM {tabela} WHERE id_{tabela} = {id}")

        dados_id = cursor.fetchone()
        return dados_id
    
    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return False

    finally:
        cursor.close()
        conexao.close()

# Atualiza status de cliente e carro ao iniciar aluguel:
def inicia_aluguel(id_cliente, id_carro):
    try:
        # Inicia a conexão:
        conexao = conectar_bd()

        update_tabela(conexao, 'cliente', id_cliente, {'status_aluguel': True})
        update_tabela(conexao, 'carro', id_carro, {'disponibilidade': False})
        return True
    
    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return False
    
    finally:
        # Fecha a conexão:
        conexao.close()

# Atualiza status de cliente e carro ao encerrar aluguel:
def encerra_aluguel(dados_aluguel):
    try:
        # Inicia a conexão:
        conexao = conectar_bd()

        id_cli = dados_aluguel['id_cliente']
        id_car = dados_aluguel['id_carro']

        update_tabela(conexao, 'cliente', id_cli, {'status_aluguel': False})
        update_tabela(conexao, 'carro', id_car, {'disponibilidade': True})
        return True

    except Exception as e:
        print(f"Erro : {e}")
        sleep(0.25)
        return False

    finally:
        # Fecha a conexão:
        conexao.close()

# Importa dados dos arquivos ".csv" para o banco de dados:
def importar_csv_para_bd():
    """Importa dados de um arquivo CSV para a tabela especificada."""
    
    try:
        conexao = conectar_bd()
        cursor = conexao.cursor()

        tabelas = {"id_funcionario": "funcionario", "id_cliente": "cliente", "id_carro": "carro", "id_aluguel": "aluguel", "id_login":"login"}
        
        for id, nome_tabela in tabelas.items():
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
        
        return True

    except Exception as e:
        print(f"Erro ao importar dados: {e}")
        sleep(0.25)
        return False

    finally:
        cursor.close()
        conexao.close()

# Exporta dodas do banco de dados, para um arquivo ".csv":
def exportar_tabelas_para_csv():
    try:
        conexao = conectar_bd()
        cursor = conexao.cursor()

        tabelas = ["funcionario", "cliente", "carro", "aluguel", "login"]

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
        
        return True
    
    except Exception as e:
        print(f"Erro ao exportar dados: {e}")
        sleep(0.25)
        return False
    
    finally:
        cursor.close()
        conexao.close()