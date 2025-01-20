from models.pessoa import Pessoa
from models.ppcCRUD import PPCCrud

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

