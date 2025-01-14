# models/ppc_crud.py

from utils.database import mysql
from MySQLdb import Error, cursors
from models.ppc import PPC

class PPCCrud:
    @staticmethod
    def criar(titulo, descricao, coordenador_id):
        """
        Cria um novo PPC no banco de dados e retorna a instância criada.
        """
        try:
            cursor = mysql.connection.cursor()
            query = """
                INSERT INTO ppc (titulo, descricao, coordenador_id, status)
                VALUES (%s, %s, %s, 'Em Criacao')
            """
            valores = (titulo, descricao, coordenador_id)
            cursor.execute(query, valores)
            mysql.connection.commit()
            ppc_id = cursor.lastrowid
            cursor.close()
            print("PPC criado com sucesso!")

            # Inicializar a instância PPC
            ppc = PPC(id=ppc_id, titulo=titulo, descricao=descricao, coordenador_id=coordenador_id)
            return ppc
        except Error as e:
            print(f"Erro ao criar PPC: {e}")
            if cursor:
                cursor.close()
            return None

    @staticmethod
    def listar_todos():
        """
        Lista todos os PPCs no banco de dados.
        """
        try:
            cursor = mysql.connection.cursor(cursors.DictCursor)
            query = "SELECT * FROM ppc"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            ppcs = [PPC(**resultado) for resultado in resultados]
            return ppcs
        except Error as e:
            print(f"Erro ao listar PPCs: {e}")
            if cursor:
                cursor.close()
            return []

    @staticmethod
    def buscar_por_id(ppc_id):
        """
        Busca um PPC no banco de dados pelo ID.
        """
        try:
            cursor = mysql.connection.cursor(cursors.DictCursor)
            query = "SELECT * FROM ppc WHERE id = %s"
            cursor.execute(query, (ppc_id,))
            resultado = cursor.fetchone()
            cursor.close()
            if resultado:
                ppc = PPC(**resultado)
                return ppc
            else:
                return None
        except Error as e:
            print(f"Erro ao buscar PPC por ID: {e}")
            if cursor:
                cursor.close()
            return None

    @staticmethod
    def atualizar(ppc_id, **kwargs):
        """
        Atualiza os dados de um PPC no banco de dados.
        """
        try:
            cursor = mysql.connection.cursor()
            campos = []
            valores = []

            for key, value in kwargs.items():
                if key == 'status' and value not in ["Em Criacao", "Em Avaliacao", "Aprovado", "Rejeitado"]:
                    raise ValueError("Status inválido!")
                campos.append(f"{key} = %s")
                valores.append(value)

            if not campos:
                print("Nenhum campo para atualizar.")
                cursor.close()
                return False

            query = f"UPDATE ppc SET {', '.join(campos)} WHERE id = %s"
            valores.append(ppc_id)
            cursor.execute(query, valores)
            mysql.connection.commit()
            cursor.close()
            print(f"PPC ID {ppc_id} atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar PPC: {e}")
            if cursor:
                cursor.close()
            return False

    @staticmethod
    def deletar(ppc_id):
        """
        Deleta um PPC do banco de dados.
        """
        try:
            cursor = mysql.connection.cursor()
            query = "DELETE FROM ppc WHERE id = %s"
            cursor.execute(query, (ppc_id,))
            mysql.connection.commit()
            cursor.close()
            print("PPC deletado com sucesso!")
            return True
        except Error as e:
            print(f"Erro ao deletar PPC: {e}")
            if cursor:
                cursor.close()
            return False
