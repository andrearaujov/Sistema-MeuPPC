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
    def atualizar(conexao, ppc_id, **kwargs):
        """
        Atualiza os dados de um PPC no banco de dados.
        """
        try:
            cursor = conexao.cursor(cursors.DictCursor)
            
            # Verificar o status atual do PPC
            cursor.execute("SELECT status FROM ppc WHERE id = %s", (ppc_id,))
            resultado = cursor.fetchone()
            
            if resultado and resultado['status'] in ['Em Avaliacao', 'Aprovado', 'Rejeitado']:
                print("PPC em avaliação ou já avaliado não pode ser modificado.")
                cursor.close()
                return False

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
            conexao.commit()
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

    @staticmethod
    def listar_por_usuario(user_id):
        """
        Lista todos os PPCs relacionados ao usuário logado.
        """
        try:
            cursor = mysql.connection.cursor(cursors.DictCursor)
            query = "SELECT * FROM ppc WHERE coordenador_id = %s"
            cursor.execute(query, (user_id,))
            resultados = cursor.fetchall()
            cursor.close()
            return [PPC(**resultado) for resultado in resultados]
        except Error as e:
            print(f"Erro ao listar PPCs por usuário: {e}")
            if cursor:
                cursor.close()
            return []

    @staticmethod
    def listar_por_colaborador(colaborador_id):
        """
        Lista todos os PPCs aos quais um colaborador foi adicionado.
        """
        try:
            cursor = mysql.connection.cursor(cursors.DictCursor)
            print(f"Buscando PPCs para colaborador_id: {colaborador_id}")  # Log de depuração

            query = """
                SELECT ppc.*, GROUP_CONCAT(ppc_colaboradores.colaborador_id) as colaboradores
                FROM ppc
                INNER JOIN ppc_colaboradores ON ppc.id = ppc_colaboradores.ppc_id
                WHERE ppc_colaboradores.colaborador_id = %s
                GROUP BY ppc.id
            """
            cursor.execute(query, (colaborador_id,))
            resultados = cursor.fetchall()
            cursor.close()
            print(f"Resultados da consulta: {resultados}")  # Log de depuração

            ppcs = [PPC(**resultado) for resultado in resultados]
            for ppc in ppcs:
                if ppc.colaboradores:
                    ppc.colaboradores = ppc.colaboradores.split(',')  # Converter string para lista
                else:
                    ppc.colaboradores = []
            
            print(f"PPCs formatados: {[ppc.__dict__ for ppc in ppcs]}")  # Log de depuração
            return ppcs
        except Error as e:
            print(f"Erro ao listar PPCs por colaborador: {e}")
            if cursor:
                cursor.close()
            return []

@staticmethod
def criar(titulo, descricao, coordenador_id, arquivo=None):
    try:
        cursor = mysql.connection.cursor()
        query = """
            INSERT INTO ppc (titulo, descricao, coordenador_id, status, arquivo)
            VALUES (%s, %s, %s, 'Em Criacao', %s)
        """
        valores = (titulo, descricao, coordenador_id, arquivo)
        cursor.execute(query, valores)
        mysql.connection.commit()
        ppc_id = cursor.lastrowid
        cursor.close()
        print("PPC criado com sucesso!")

        ppc = PPC(id=ppc_id, titulo=titulo, descricao=descricao, coordenador_id=coordenador_id, arquivo=arquivo)
        return ppc
    except Error as e:
        print(f"Erro ao criar PPC: {e}")
        if cursor:
            cursor.close()
        return None
