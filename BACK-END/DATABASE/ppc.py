from DATABASE.conexao import conectar
from mysql.connector import Error

class PPC:
    def __init__(self, id=None, titulo=None, descricao=None, status="Em Criacao", motivo_rejeicao=None, coordenador_id=None):
        """
        Inicializa uma instância da classe PPC.
        :param id: ID único do PPC.
        :param titulo: Título do PPC.
        :param descricao: Descrição do PPC.
        :param status: Status do PPC (padrão: "Em Criacao").
        :param motivo_rejeicao: Justificativa para rejeição (se aplicável).
        :param coordenador_id: ID do coordenador responsável.
        """
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.motivo_rejeicao = motivo_rejeicao
        self.coordenador_id = coordenador_id

    @staticmethod
    def criar(conexao, titulo, descricao, coordenador_id):
        """
        Cria um novo PPC no banco de dados.
        """
        try:
            cursor = conexao.cursor()
            query = """
                INSERT INTO ppc (titulo, descricao, coordenador_id, status)
                VALUES (%s, %s, %s, 'Em Criacao')
            """
            valores = (titulo, descricao, coordenador_id)
            cursor.execute(query, valores)
            conexao.commit()
            print("PPC criado com sucesso!")
        except Error as e:
            print(f"Erro ao criar PPC: {e}")

    @staticmethod
    def listar_todos(conexao):
        """
        Lista todos os PPCs no banco de dados.
        """
        try:
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT * FROM ppc"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao listar PPCs: {e}")
            return []

    @staticmethod
    def buscar_por_id(conexao, id):
        """
        Busca um PPC no banco de dados pelo ID.
        """
        try:
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT * FROM ppc WHERE id = %s"
            cursor.execute(query, (id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Erro ao buscar PPC por ID: {e}")
            return None

    @staticmethod
    def atualizar(conexao, id, titulo=None, descricao=None, status=None, motivo_rejeicao=None):
        """
        Atualiza os dados de um PPC no banco de dados.
        """
        try:
            cursor = conexao.cursor()
            campos = []
            valores = []

            if titulo:
                campos.append("titulo = %s")
                valores.append(titulo)
            if descricao:
                campos.append("descricao = %s")
                valores.append(descricao)
            if status:
                campos.append("status = %s")
                valores.append(status)
            if motivo_rejeicao:
                campos.append("motivo_rejeicao = %s")
                valores.append(motivo_rejeicao)

            query = f"UPDATE ppc SET {', '.join(campos)} WHERE id = %s"
            valores.append(id)
            cursor.execute(query, valores)
            conexao.commit()
            print("PPC atualizado com sucesso!")
        except Error as e:
            print(f"Erro ao atualizar PPC: {e}")

    @staticmethod
    def deletar(conexao, id):
        """
        Deleta um PPC do banco de dados.
        """
        try:
            cursor = conexao.cursor()
            query = "DELETE FROM ppc WHERE id = %s"
            cursor.execute(query, (id,))
            conexao.commit()
            print("PPC deletado com sucesso!")
        except Error as e:
            print(f"Erro ao deletar PPC: {e}")

    @staticmethod
    def adicionar_colaborador(conexao, ppc_id, colaborador_id):
        """
        Adiciona um colaborador ao PPC.
        """
        try:
            cursor = conexao.cursor()
            query = "INSERT INTO ppc_colaboradores (ppc_id, colaborador_id) VALUES (%s, %s)"
            valores = (ppc_id, colaborador_id)
            cursor.execute(query, valores)
            conexao.commit()
            print("Colaborador adicionado com sucesso ao PPC!")
        except Error as e:
            print(f"Erro ao adicionar colaborador: {e}")

    @staticmethod
    def listar_colaboradores(conexao, ppc_id):
        """
        Lista os colaboradores de um PPC.
        """
        try:
            cursor = conexao.cursor(dictionary=True)
            query = """
                SELECT p.id, p.nome, p.email
                FROM pessoa p
                INNER JOIN ppc_colaboradores pc ON p.id = pc.colaborador_id
                WHERE pc.ppc_id = %s
            """
            cursor.execute(query, (ppc_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao listar colaboradores: {e}")
            return []

    @staticmethod
    def adicionar_avaliador(conexao, ppc_id, avaliador_id):
        """
        Adiciona um avaliador ao PPC.
        """
        try:
            cursor = conexao.cursor()
            query = "INSERT INTO ppc_avaliadores (ppc_id, avaliador_id) VALUES (%s, %s)"
            valores = (ppc_id, avaliador_id)
            cursor.execute(query, valores)
            conexao.commit()
            print("Avaliador adicionado com sucesso ao PPC!")
        except Error as e:
            print(f"Erro ao adicionar avaliador: {e}")

    @staticmethod
    def listar_avaliadores(conexao, ppc_id):
        """
        Lista os avaliadores de um PPC.
        """
        try:
            cursor = conexao.cursor(dictionary=True)
            query = """
                SELECT p.id, p.nome, p.email
                FROM pessoa p
                INNER JOIN ppc_avaliadores pa ON p.id = pa.avaliador_id
                WHERE pa.ppc_id = %s
            """
            cursor.execute(query, (ppc_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao listar avaliadores: {e}")
            return []

    @staticmethod
    def alterar_status(conexao, ppc_id, novo_status, motivo_rejeicao=None):
        """
        Altera o status de um PPC.
        """
        try:
            cursor = conexao.cursor()
            if novo_status == "Rejeitado" and motivo_rejeicao:
                query = "UPDATE ppc SET status = %s, motivo_rejeicao = %s WHERE id = %s"
                valores = (novo_status, motivo_rejeicao, ppc_id)
            else:
                query = "UPDATE ppc SET status = %s WHERE id = %s"
                valores = (novo_status, ppc_id)
            cursor.execute(query, valores)
            conexao.commit()
            print(f"Status do PPC alterado para {novo_status} com sucesso!")
        except Error as e:
            print(f"Erro ao alterar status do PPC: {e}")
