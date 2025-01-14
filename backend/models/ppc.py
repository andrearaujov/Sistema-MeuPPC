# models/ppc.py

from utils.database import mysql
from models.estrategiaStatus import EstrategiaStatus, AprovadoStrategy, EmCriacaoStrategy, EmAvaliacaoStrategy

class PPC:
    def __init__(self, id=None, titulo=None, descricao=None, status="Em Criacao", motivo_rejeicao=None,
                 coordenador_id=None, created_at=None, updated_at=None):
        """
        Inicializa uma instância da classe PPC.
        """
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.motivo_rejeicao = motivo_rejeicao
        self.coordenador_id = coordenador_id
        self.colaboradores = []
        self.avaliadores = []
        self.created_at = created_at
        self.updated_at = updated_at

        # Define o status inicial e a estratégia correspondente
        self.status = status
        self._set_estrategia()

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
            self.estrategia = None  # Caso de status desconhecido
            print(f"Status '{self.status}' desconhecido. Nenhuma estratégia aplicada.")

    def set_status(self, novo_status):
        """
        Usa a estratégia atual para tentar alterar o status do PPC.
        """
        if self.estrategia:
            self.estrategia.set_status(self, novo_status)
        else:
            print("Estratégia não definida para o status atual.")

    def adicionar_colaborador(self, colaborador_id):
        """
        Adiciona um colaborador ao PPC.
        """
        if isinstance(self.estrategia, EmCriacaoStrategy):
            self.colaboradores.append(colaborador_id)
            print(f"Colaborador ID {colaborador_id} adicionado ao PPC '{self.titulo}'.")
        else:
            print("Não é possível adicionar colaboradores no status atual.")

    def enviar_para_avaliacao(self, avaliadores_ids):
        """
        Define os avaliadores e altera o status para 'Em Avaliação'.
        """
        if isinstance(self.estrategia, EmCriacaoStrategy):
            self.avaliadores = avaliadores_ids
            self.set_status("Em Avaliacao")
            print(f"PPC '{self.titulo}' enviado para avaliação.")
        else:
            print("Não é possível enviar para avaliação no status atual.")

    def aprovar(self):
        """
        Altera o status do PPC para 'Aprovado'.
        """
        if isinstance(self.estrategia, EmAvaliacaoStrategy):
            self.set_status("Aprovado")
            print(f"PPC '{self.titulo}' aprovado.")
        else:
            print("Não é possível aprovar no status atual.")

    def executar_acao(self):
        """
        Executa a ação de acordo com a estratégia de status.
        """
        if self.estrategia:
            self.estrategia.executar_acao(self)
        else:
            print("Estratégia não definida para o status atual.")
