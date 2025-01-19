from utils.database import mysql
from MySQLdb import Error, cursors
from models.ppc import PPC

class Relatorio:
    def __init__(self, ppc):
        """
        Inicializa o relatório associado a um PPC específico.
        :param ppc: Instância do PPC relacionada ao relatório.
        """
        self.ppc = ppc

    def gerarRelatorioColaboradores(self):
        """
        Gera um relatório de colaboradores associados ao PPC.
        :return: Lista de dicionários com os dados dos colaboradores.
        """
        try:
            cursor = mysql.connection.cursor(cursors.DictCursor)
            query = """
                SELECT p.id, p.nome, p.email
                FROM pessoa AS p
                INNER JOIN ppc_colaboradores AS pc ON p.id = pc.colaborador_id
                WHERE pc.ppc_id = %s
            """
            cursor.execute(query, (self.ppc.id,))
            colaboradores = cursor.fetchall()
            cursor.close()
            return colaboradores
        except Error as e:
            print(f"Erro ao gerar relatório de colaboradores: {e}")
            return []

    def gerarRelatorioAvaliadores(self):
        """
        Gera um relatório de avaliadores associados ao PPC.
        :return: Lista de dicionários com os dados dos avaliadores.
        """
        try:
            cursor = mysql.connection.cursor(cursors.DictCursor)
            query = """
                SELECT p.id, p.nome, p.email
                FROM pessoa AS p
                INNER JOIN ppc_avaliadores AS pa ON p.id = pa.avaliador_id
                WHERE pa.ppc_id = %s
            """
            cursor.execute(query, (self.ppc.id,))
            avaliadores = cursor.fetchall()
            cursor.close()
            return avaliadores
        except Error as e:
            print(f"Erro ao gerar relatório de avaliadores: {e}")
            return []

    def gerarRelatorioParticipantes(self):
        """
        Gera um relatório combinado de colaboradores e avaliadores associados ao PPC.
        :return: Dicionário com listas de colaboradores e avaliadores.
        """
        try:
            colaboradores = self.gerarRelatorioColaboradores()
            avaliadores = self.gerarRelatorioAvaliadores()
            return {
                "colaboradores": colaboradores,
                "avaliadores": avaliadores
            }
        except Error as e:
            print(f"Erro ao gerar relatório de participantes: {e}")
            return {}
