import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Queijominas5*',
            database='projeto_ppc'
        )
        if conexao.is_connected():
            print("Conexão com o banco de dados MySQL foi estabelecida com sucesso!")
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def fechar_conexao(conexao):
    if conexao.is_connected():
        conexao.close()
        print("Conexão com o MySQL foi encerrada.")
