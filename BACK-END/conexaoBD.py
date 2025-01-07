import mysql.connector
from mysql.connector import Error

try:
    # Configuração da conexão
    conexao = mysql.connector.connect(
        host='127.0.0.1',         # Host do servidor MySQL
        user='root',       # Usuário do banco de dados
        password='Queijominas5*',     # Senha do usuário
        database='projeto_ppc'    # Nome do banco de dados
    )

    if conexao.is_connected():
        print("Conexão com o banco de dados MySQL foi estabelecida com sucesso!")

except Error as e:
    print(f"Erro ao conectar ao MySQL: {e}")

finally:
    if 'conexao' in locals() and conexao.is_connected():
        conexao.close()
        print("Conexão com o MySQL foi encerrada.")
