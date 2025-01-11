from DATABASE.pessoa import Pessoa
from DATABASE.ppcCRUD import PPCCrud

class Colaborador(Pessoa):
    def editarPPC(self, conexao, ppc_id, conteudo):
        """
        Ajuda na modificação do conteúdo de um PPC.
        """
        try:
            PPCCrud.atualizar(conexao, ppc_id, descricao=conteudo)
            print(f"PPC ID {ppc_id} atualizado pelo colaborador {self.nome}.")
        except Exception as e:
            print(f"Erro ao editar PPC: {e}")

class Avaliador(Pessoa):
    def avaliarPPC(self, conexao, ppc_id, aprovado, motivo_rejeicao=None):
        """
        Avalia o PPC, aprovando ou rejeitando.
        """
        try:
            status = "Aprovado" if aprovado else "Rejeitado"
            PPCCrud.atualizar(conexao, ppc_id, status=status, motivo_rejeicao=motivo_rejeicao)
            print(f"PPC ID {ppc_id} avaliado como '{status}' pelo avaliador {self.nome}.")
        except Exception as e:
            print(f"Erro ao avaliar PPC: {e}")