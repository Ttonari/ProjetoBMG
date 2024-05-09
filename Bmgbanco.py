import mysql.connector
from mysql.connector import errorcode

print('Conectando...')

try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='root123',
        database = 'bmgbanco'
    )

except mysql.connector.Error as err:
    if err.errno == errorcode.ERACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)
else:
    print('Conectado')

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS bmg_project;")

cursor.execute("CREATE DATABASE bmg_project;")

cursor.execute("USE bmg_project")

# criando tabelas
TABLES = {}

TABLES['Clientes'] = ('''
    CREATE TABLE `clientes` (
      `id` INT(11) NOT NULL AUTO_INCREMENT,
      `nome` VARCHAR(100) NOT NULL,
      `cpf` INT NOT NULL,
      `telefone` INT NOT NULL,
      `nascimento` INT NOT NULL,
      `email`  VARCHAR(50) NOT NULL,
      `plano`  VARCHAR(50) NOT NULL,
      `pagamento`  VARCHAR(50) NOT NULL,
      `datadeinicio`  INT NOT NULL,
      PRIMARY KEY (`id`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin; ''')

TABLES['Usuario'] = ('''
    CREATE TABLE `usuarios` (      
      `nome` VARCHAR(50) NOT NULL,
      `nickname` VARCHAR(50) NOT NULL,
      `senha` VARCHAR(50) NOT NULL,
      PRIMARY KEY (`nickname`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin;  ''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print(f'Criando tabela {tabela_nome}')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Tabela já existe')
        else:
            print(err.msg)
    else:
        print('ok')

# inserindo usuários
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) values (%s,%s,%s)'

usuarios = [
    ('lucas oliveira nunes', 'lucas', 'lucas12345'),
    ('leandro de oliveira costa', 'leandro', 'leandro12345'),
    ('raul de oliveira barbosa', 'raul', 'raul12345'),
    ('milena marcondes dos santos', 'milena', 'milena12345'),
]

cursor.executemany(usuario_sql,usuarios)

cursor.execute('select * from bmg_project.usuarios')
print('---------------- Usuários ----------------')
for user in cursor.fetchall():
    print(user[0])

TABLES['Planos'] = ('''
    CREATE TABLE `Planos` (      
      `nome_plano` VARCHAR(50) NOT NULL,
      `tempo_plano` VARCHAR(50) NOT NULL,
      `valor_plano` VARCHAR(50) NOT NULL,
      PRIMARY KEY (`nome_plano`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin;  ''')

TABLES['Despesas'] = ('''
    CREATE TABLE `Despesas` (      
      `nome_despesa` VARCHAR(50) NOT NULL,
      `valor_despesa` INT NOT NULL,
      `vencimento_despesa` VARCHAR(50) NOT NULL,
      PRIMARY KEY (`nome_despesa`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin;  ''')

# commitando pra gravar no banco
conn.commit()

cursor.close()
conn.close()
