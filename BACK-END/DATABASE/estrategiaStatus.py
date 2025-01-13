from abc import ABC, abstractmethod

# Interface para todas as ações (estratégias)
class EstrategiaStatus(ABC):
    @abstractmethod
    def executar_acao(self, ppc):
        pass

# Estratégia para o status "Aprovado"
class AprovadoStrategy:
    def executar_acao(self, ppc):
        """
        Executa a ação de acordo com o status 'Aprovado'.
        Não deve permitir modificações após aprovação.
        """
        print(f"PPC '{ppc.titulo}' está aprovado. Não é permitido fazer alterações.")
    
    def set_status(self, ppc, status):
        """
        Permite mudanças de status somente se o status for válido.
        """
        if status != "Aprovado":
            ppc.set_status(status)
        else:
            print("Não é permitido alterar o status de um PPC aprovado.")


# Estratégia para o status "Em Criação"
class EmCriacaoStrategy(EstrategiaStatus):
    def executar_acao(self, ppc):
        # Acesse os atributos usando ponto
        print(f"PPC '{ppc.titulo}' está em criação. Você pode adicionar colaboradores.")
        # Aqui, podemos permitir a adição de colaboradores, por exemplo.
        # ppc.add_colaboradores()

# Estratégia para o status "Em Avaliação"
class EmAvaliacaoStrategy:
    def executar_acao(self, ppc):
        """
        Executa a ação de acordo com o status 'Em Avaliação'.
        Permite avaliação do PPC.
        """
        print(f"PPC '{ppc.titulo}' está em avaliação. Você pode adicionar avaliadores.")
    
    def set_status(self, ppc, status):
        """
        Permite mudanças de status entre avaliação e outros estados.
        """
        if status in ["Em Criacao", "Aprovado"]:
            ppc.set_status(status)
        else:
            print(f"Status '{status}' não permitido para o PPC em avaliação.")




