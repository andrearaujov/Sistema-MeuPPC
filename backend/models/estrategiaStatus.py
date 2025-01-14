from abc import ABC, abstractmethod

# Interface para todas as ações (estratégias)
class EstrategiaStatus(ABC):
    @abstractmethod
    def executar_acao(self, ppc):
        pass

    @abstractmethod
    def set_status(self, ppc, novo_status):
        pass

# Estratégia para o status "Aprovado"
class AprovadoStrategy(EstrategiaStatus):
    def executar_acao(self, ppc):
        print(f"PPC '{ppc.titulo}' está aprovado. Não é permitido fazer alterações.")

    def set_status(self, ppc, novo_status):
        if novo_status != "Aprovado":
            print("Não é permitido alterar o status de um PPC aprovado.")
        else:
            print("O PPC já está no status 'Aprovado'.")

# Estratégia para o status "Em Criação"
class EmCriacaoStrategy(EstrategiaStatus):
    def executar_acao(self, ppc):
        print(f"PPC '{ppc.titulo}' está em criação. Você pode adicionar colaboradores.")

    def set_status(self, ppc, novo_status):
        if novo_status in ["Em Avaliacao", "Rejeitado"]:
            ppc.set_status(novo_status)
            print(f"Status do PPC '{ppc.titulo}' alterado para '{novo_status}'.")
        else:
            print(f"Transição de status para '{novo_status}' não é permitida a partir de 'Em Criacao'.")

# Estratégia para o status "Em Avaliação"
class EmAvaliacaoStrategy(EstrategiaStatus):
    def executar_acao(self, ppc):
        print(f"PPC '{ppc.titulo}' está em avaliação. Avaliadores estão analisando o PPC.")

    def set_status(self, ppc, novo_status):
        if novo_status in ["Aprovado", "Rejeitado"]:
            ppc.set_status(novo_status)
            print(f"Status do PPC '{ppc.titulo}' alterado para '{novo_status}'.")
        else:
            print(f"Transição de status para '{novo_status}' não é permitida a partir de 'Em Avaliacao'.")
