# SISTEMA DE LOCAÇÃO DE AUTOMÓVEIS

### Resumo

Projeto trata-se de um sistema para gerenciamento de aluguéis de automóveis, fazendo o uso dos métodos abordados em sala de aula.

### Descrição

O sistema de gerenciamento conta com três arquivos `crud.py`, `sistema.py` e `menu.py`. Há também uma pasta de backup para com arquivos .csv que armazena todos os dados do sistema, de modo a manter um ópia de segurança para a sincronização do sistema. O sistema ainda conta com a manipulação funções para manipular os dados dos clientes, carros, aluguéis e funcionários, protegidos com um sistema de autenticação com login e senha, atendendo aos requisitos definidos pelo dono da empresa.

### Execução do Sistema

Para realizar a execução do sistema, será necessário vincular com um banco de dados PostgresSQL, cuja conexão e configuração é definida pelos seguintes parâmetros no arquivo `crud.py`:

```python
  # Configurações do banco de dados
  DB_NAME = "locadora_carro"
  DB_USER = "postgres"
  DB_PASSWORD = "postgres"
  DB_HOST = "localhost"
  DB_PORT = "5432"
```

Após configurado, basta executar o arquivo `menu.py`, que irá entrar na sessão de login, cujo usuário e senha padrão é `admin` para ambos. Após iniciar o sistema será criado e sincronizado com o banco de dados do PostgresSQL, sendo necessário apenas importar os dados do backup, executando a opção 3 do menu inicial:

```
  === Sistema de Aluguel de Carros ===
  1. Cadastro
  2. Consulta
  3. Importar Dados
  4. Sair
```
