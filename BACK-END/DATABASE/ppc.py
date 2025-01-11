from DATABASE.estrategiaStatus import AprovadoStrategy, EmCriacaoStrategy, EmAvaliacaoStrategy

class PPC:
    def __init__(self, id=None, titulo=None, descricao=None, status="Em Criacao", motivo_rejeicao=None, coordenador_id=None, created_at=None, updated_at=None):
        """
        Inicializa uma instância da classe PPC.
        :param id: ID único do PPC.
        :param titulo: Título do PPC.
        :param descricao: Descrição do PPC.
        :param status: Status atual do PPC.
        :param motivo_rejeicao: Justificativa para rejeição.
        :param coordenador_id: ID do coordenador responsável.
        """
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.motivo_rejeicao = motivo_rejeicao
        self.coordenador_id = coordenador_id
        self.colaboradores = []
        self.avaliadores = []
        self.created_at = created_at
        self.updated_at = updated_at

        # Definir a estratégia de status inicial
        self._set_estrategia()

    def _set_estrategia(self):
        """
        Define a estratégia de status dependendo do estado atual do PPC.
        """
        if self.status == "Em Criacao":
            self.estrategia = EmCriacaoStrategy()
        elif self.status == "Em Avaliacao":
            self.estrategia = EmAvaliacaoStrategy()
        elif self.status == "Aprovado":
            self.estrategia = AprovadoStrategy()

    def set_status(self, novo_status):
        """
        Altera o status do PPC e redefine a estratégia de acordo.
        """
        self.status = novo_status
        self._set_estrategia()

    def adicionar_colaborador(self, colaborador):
        """
        Adiciona um colaborador à lista de colaboradores.
        """
        if isinstance(self.estrategia, EmCriacaoStrategy):
            self.colaboradores.append(colaborador)
            print(f"Colaborador {colaborador} adicionado ao PPC '{self.titulo}'.")
        else:
            print("Não é possível adicionar colaboradores no status atual.")

    def enviar_para_avaliacao(self, avaliadores):
        """
        Define os avaliadores e altera o status para 'Em Avaliação'.
        """
        if isinstance(self.estrategia, EmCriacaoStrategy):
            self.avaliadores = avaliadores
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
        self.estrategia.executar_acao(self)
