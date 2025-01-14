# models/pessoa_crud.py

from utils.database import mysql
from MySQLdb import Error, cursors
from models.pessoa import Pessoa

class PessoaCRUD:
    @staticmethod
    def inserir(nome, email, senha, papel):
        """
        Insere uma nova pessoa no banco de dados.
        """
        try:
            cursor = mysql.connection.cursor()
            query = "INSERT INTO pessoa (nome, email, senha, papel) VALUES (%s, %s, %s, %s)"
            valores = (nome, email, senha, papel)
            cursor.execute(query, valores)
            mysql.connection.commit()
            pessoa_id = cursor.lastrowid
            cursor.close()
            print("Pessoa inserida com sucesso!")
            return pessoa_id  # Retorna o ID da pessoa inserida
        except Error as e:
            print(f"Erro ao inserir pessoa: {e}")
            if cursor:
                cursor.close()
            return None

    @staticmethod
    def listar_todas():
        """
        Lista todas as pessoas do banco de dados.
        """
        try:
            cursor = mysql.connection.cursor(cursors.DictCursor)
            query = "SELECT * FROM pessoa"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            # Converte cada resultado em uma instância de Pessoa
            pessoas = [Pessoa(**resultado) for resultado in resultados]
            return pessoas
        except Error as e:
            print(f"Erro ao listar pessoas: {e}")
            if cursor:
                cursor.close()
            return []

    @staticmethod
    def buscar_por_id(id):
        """
        Busca uma pessoa no banco de dados pelo ID.
        """
        try:
            cursor = mysql.connection.cursor(cursors.DictCursor)
            query = "SELECT * FROM pessoa WHERE id = %s"
            cursor.execute(query, (id,))
            resultado = cursor.fetchone()
            cursor.close()
            if resultado:
                return Pessoa(**resultado)
            else:
                return None
        except Error as e:
            print(f"Erro ao buscar pessoa por ID: {e}")
            if cursor:
                cursor.close()
            return None

    @staticmethod
    def buscar_por_email(email):
        """
        Busca uma pessoa no banco de dados pelo email.
        """
        try:
            cursor = mysql.connection.cursor(cursors.DictCursor)
            query = "SELECT * FROM pessoa WHERE email = %s"
            cursor.execute(query, (email,))
            resultado = cursor.fetchone()
            cursor.close()
            if resultado:
                return Pessoa(**resultado)
            else:
                return None
        except Error as e:
            print(f"Erro ao buscar pessoa por email: {e}")
            if cursor:
                cursor.close()
            return None

    @staticmethod
    def atualizar(id, nome=None, email=None, senha=None, papel=None):
        """
        Atualiza os dados de uma pessoa no banco de dados.
        """
        try:
            cursor = mysql.connection.cursor()
            campos = []
            valores = []

            if nome:
                campos.append("nome = %s")
                valores.append(nome)
            if email:
                campos.append("email = %s")
                valores.append(email)
            if senha:
                campos.append("senha = %s")
                valores.append(senha)
            if papel:
                campos.append("papel = %s")
                valores.append(papel)

            if not campos:
                print("Nenhum campo para atualizar.")
                cursor.close()
                return False

            query = f"UPDATE pessoa SET {', '.join(campos)} WHERE id = %s"
            valores.append(id)
            cursor.execute(query, valores)
            mysql.connection.commit()
            cursor.close()
            print("Pessoa atualizada com sucesso!")
            return True
        except Error as e:
            print(f"Erro ao atualizar pessoa: {e}")
            if cursor:
                cursor.close()
            return False

    @staticmethod
    def deletar(id):
        """
        Deleta uma pessoa do banco de dados.
        """
        try:
            cursor = mysql.connection.cursor()
            query = "DELETE FROM pessoa WHERE id = %s"
            cursor.execute(query, (id,))
            mysql.connection.commit()
            cursor.close()
            print("Pessoa deletada com sucesso!")
            return True
        except Error as e:
            print(f"Erro ao deletar pessoa: {e}")
            if cursor:
                cursor.close()
            return False

    @staticmethod
    def deletar_todas():
        """
        Deleta todas as pessoas da tabela 'pessoa'.
        """
        try:
            cursor = mysql.connection.cursor()
            query = "DELETE FROM pessoa"
            cursor.execute(query)
            mysql.connection.commit()
            cursor.close()
            print("Todas as pessoas foram deletadas com sucesso!")
            return True
        except Error as e:
            print(f"Erro ao deletar todas as pessoas: {e}")
            if cursor:
                cursor.close()
            return False
