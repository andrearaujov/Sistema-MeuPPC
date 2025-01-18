from utils.database import mysql
from models.estrategiaStatus import EstrategiaStatus, AprovadoStrategy, EmCriacaoStrategy, EmAvaliacaoStrategy

class PPC:
    def __init__(self, id=None, titulo=None, descricao=None, status="Em Criacao", motivo_rejeicao=None,
                 coordenador_id=None, created_at=None, updated_at=None, colaboradores=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.motivo_rejeicao = motivo_rejeicao
        self.coordenador_id = coordenador_id
        self.colaboradores = colaboradores if colaboradores is not None else []
        self.avaliadores = []
        self.created_at = created_at
        self.updated_at = updated_at
        self.status = status
        self._set_estrategia()

    def set_status(self, novo_status):
        """
        Usa a estratégia atual para tentar alterar o status do PPC.
        """
        if self.status != novo_status:
            if self.estrategia:
                self.estrategia.set_status(self, novo_status)
            else:
                print("Estratégia não definida para o status atual.")

    def _set_estrategia(self):
        """
        Define a estratégia de status com base no estado atual do PPC.
        """
        estrategia_classes = {
            "Em Criacao": EmCriacaoStrategy,
            "Em Avaliacao": EmAvaliacaoStrategy,
            "Aprovado": AprovadoStrategy
        }
        estrategia_classe = estrategia_classes.get(self.status)
        if estrategia_classe:
            self.estrategia = estrategia_classe()
        else:
            self.estrategia = None
            print(f"Status '{self.status}' desconhecido. Nenhuma estratégia aplicada.")

    def adicionar_colaborador(self, colaborador_id):
        if isinstance(self.estrategia, EmCriacaoStrategy):
            self.colaboradores.append(colaborador_id)
            print(f"Colaborador ID {colaborador_id} adicionado ao PPC '{self.titulo}'.")
        else:
            print("Não é possível adicionar colaboradores no status atual.")

    def enviar_para_avaliacao(self, avaliadores_ids):
        if isinstance(self.estrategia, EmCriacaoStrategy):
            self.avaliadores = avaliadores_ids
            if self.status != "Em Avaliacao":
                self.set_status("Em Avaliacao")
            print(f"PPC '{self.titulo}' enviado para avaliação.")
        else:
            print("Não é possível enviar para avaliação no status atual.")

    def aprovar(self):
        if isinstance(self.estrategia, EmAvaliacaoStrategy):
            self.set_status("Aprovado")
            print(f"PPC '{self.titulo}' aprovado.")
        else:
            print("Não é possível aprovar no status atual.")

    def executar_acao(self):
        if self.estrategia:
            self.estrategia.executar_acao(self)
        else:
            print("Estratégia não definida para o status atual.")
