from DATABASE.conexao import conectar, fechar_conexao
from DATABASE.ppc import PPC
from DATABASE.estrategiaStatus import AprovadoStrategy, EmCriacaoStrategy, EmAvaliacaoStrategy
from mysql.connector import Error

class PPCCrud:
    @staticmethod
    def criar(conexao, titulo, descricao, coordenador_id):
        """
        Cria um novo PPC no banco de dados e executa a ação inicial com base no status 'Em Criacao'.
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
            ppc_id = cursor.lastrowid  # Recupera o ID do último PPC inserido
            print("PPC criado com sucesso!")

            # Inicializar a instância PPC e executar a ação com base no status
            ppc = PPC(id=ppc_id, titulo=titulo, descricao=descricao, coordenador_id=coordenador_id)
            ppc.executar_acao()  # Executa a ação com base no status 'Em Criacao'
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
    def atualizar(conexao, ppc_id, **kwargs):
        """
        Atualiza os dados de um PPC no banco de dados.
        """
        try:
            # Verifica se o status fornecido é válido
            if "status" in kwargs and kwargs["status"] not in ["Em Criacao", "Em Avaliacao", "Aprovado", "Rejeitado"]:
                raise ValueError("Status inválido!")

            cursor = conexao.cursor()
            
            # Gera a parte do SET da query SQL
            set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
            query = f"UPDATE ppc SET {set_clause} WHERE id = %s"
            
            # Executa a atualização
            cursor.execute(query, (*kwargs.values(), ppc_id))
            conexao.commit()

            print(f"PPC ID {ppc_id} atualizado com sucesso!")
        except Exception as e:
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
