
from DATABASE.conexao import conectar
from mysql.connector import Error

class Pessoa:
    def __init__(self, id=None, nome=None, email=None, papel=None):
        """
        Inicializa uma instância da classe Pessoa.
        :param id: ID único da pessoa (opcional, geralmente gerado pelo banco de dados).
        :param nome: Nome da pessoa.
        :param email: E-mail único da pessoa.
        :param papel: Papel da pessoa (Coordenador, Colaborador, Avaliador).
        """
        self.id = id
        self.nome = nome
        self.email = email
        self.papel = papel

    @staticmethod
    def inserir(conexao, nome, email, papel):
        """
        Insere uma nova pessoa no banco de dados.
        """
        try:
            cursor = conexao.cursor()
            query = "INSERT INTO pessoa (nome, email, papel) VALUES (%s, %s, %s)"
            valores = (nome, email, papel)
            cursor.execute(query, valores)
            conexao.commit()
            print("Pessoa inserida com sucesso!")
        except Error as e:
            print(f"Erro ao inserir pessoa: {e}")

    @staticmethod
    def listar_todas(conexao):
        """
        Lista todas as pessoas do banco de dados.
        """
        try:
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT * FROM pessoa"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao listar pessoas: {e}")
            return []

    @staticmethod
    def buscar_por_id(conexao, id):
        """
        Busca uma pessoa no banco de dados pelo ID.
        """
        try:
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT * FROM pessoa WHERE id = %s"
            cursor.execute(query, (id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Erro ao buscar pessoa por ID: {e}")
            return None

    @staticmethod
    def atualizar(conexao, id, nome=None, email=None, papel=None):
        """
        Atualiza os dados de uma pessoa no banco de dados.
        """
        try:
            cursor = conexao.cursor()
            campos = []
            valores = []

            if nome:
                campos.append("nome = %s")
                valores.append(nome)
            if email:
                campos.append("email = %s")
                valores.append(email)
            if papel:
                campos.append("papel = %s")
                valores.append(papel)

            query = f"UPDATE pessoa SET {', '.join(campos)} WHERE id = %s"
            valores.append(id)
            cursor.execute(query, valores)
            conexao.commit()
            print("Pessoa atualizada com sucesso!")
        except Error as e:
            print(f"Erro ao atualizar pessoa: {e}")

    @staticmethod
    def deletar(conexao, id):
        """
        Deleta uma pessoa do banco de dados.
        """
        try:
            cursor = conexao.cursor()
            query = "DELETE FROM pessoa WHERE id = %s"
            cursor.execute(query, (id,))
            conexao.commit()
            print("Pessoa deletada com sucesso!")
        except Error as e:
            print(f"Erro ao deletar pessoa: {e}")

    @staticmethod
    def deletar_todas(conexao):
        """
        Deleta todas as pessoas da tabela 'pessoa'.
        """
        try:
            cursor = conexao.cursor()
            query = "DELETE FROM pessoa"
            cursor.execute(query)
            conexao.commit()
            print("Todas as pessoas foram deletadas com sucesso!")
        except Error as e:
            print(f"Erro ao deletar todas as pessoas: {e}")
