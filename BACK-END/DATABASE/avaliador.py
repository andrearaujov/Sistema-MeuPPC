from DATABASE.pessoa import Pessoa
from DATABASE.ppcCRUD import PPCCrud
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