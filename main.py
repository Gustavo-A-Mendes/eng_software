class Funcionario:
    def __init__(self, id_func, nome, email, cpf, telefones):
        self.id_func = id_func
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.telefones = telefones


class Carro:
    def __init__(self, id_carro, modelo, marca, diaria=0.00, disponibilidade=True):
        self.id_carro = id_carro
        self.modelo = modelo
        self.marca = marca
        self.diaria = diaria
        self.disponibilidade = disponibilidade


class Cliente:
    def __init__(self, id_cliente, nome, email, cpf, cnh, telefone, cidade, bairro, rua, numero):
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.cnh = cnh
        self.telefone = telefone
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero = numero


class Aluguel:
    def __init__(self, id_aluguel, id_func, id_carro, id_cliente, preco, data_inicio, data_fim):
        self.id_aluguel = id_aluguel
        self.id_func = id_func
        self.id_carro = id_carro
        self.id_cliente = id_cliente
        self.preco = preco
        self.data_inicio = data_inicio
        self.data_fim = data_fim

