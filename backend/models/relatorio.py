from models.conexao import conectar, fechar_conexao
from models.ppcCRUD import PPCCrud
from models.pessoa import Pessoa

class Relatorio:
    def __init__(self, ppc_id):
        """
        Inicializa um relatório associado a um PPC específico.
        :param ppc_id: ID do PPC relacionado.
        """
        self.ppc_id = ppc_id

    def gerarRelatorioColaboradores(self, conexao):
        """
        Gera um relatório de colaboradores associados ao PPC.
        """
        try:
            cursor = conexao.cursor(dictionary=True)
            query = """
                SELECT p.id, p.nome, p.email
                FROM pessoa AS p
                INNER JOIN ppc_colaboradores AS pc
                ON p.id = pc.colaborador_id
                WHERE pc.ppc_id = %s
            """
            cursor.execute(query, (self.ppc_id,))
            colaboradores = cursor.fetchall()
            return colaboradores
        except Exception as e:
            print(f"Erro ao gerar relatório de colaboradores: {e}")
            return []

    def gerarRelatorioAvaliadores(self, conexao):
        """
        Gera um relatório de avaliadores associados ao PPC.
        """
        try:
            cursor = conexao.cursor(dictionary=True)
            query = """
                SELECT p.id, p.nome, p.email
                FROM pessoa AS p
                INNER JOIN ppc_avaliadores AS pa
                ON p.id = pa.avaliador_id
                WHERE pa.ppc_id = %s
            """
            cursor.execute(query, (self.ppc_id,))
            avaliadores = cursor.fetchall()
            return avaliadores
        except Exception as e:
            print(f"Erro ao gerar relatório de avaliadores: {e}")
            return []

    def gerarRelatorioParticipantes(self, conexao):
        """
        Gera um relatório combinado de colaboradores e avaliadores associados ao PPC.
        """
        try:
            colaboradores = self.gerarRelatorioColaboradores(conexao)
            avaliadores = self.gerarRelatorioAvaliadores(conexao)
            return {
                "colaboradores": colaboradores,
                "avaliadores": avaliadores
            }
        except Exception as e:
            print(f"Erro ao gerar relatório de participantes: {e}")
            return {}
