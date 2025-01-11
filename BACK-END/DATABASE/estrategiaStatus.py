from abc import ABC, abstractmethod

# Interface para todas as ações (estratégias)
class EstrategiaStatus(ABC):
    @abstractmethod
    def executar_acao(self, ppc):
        pass

# Estratégia para o status "Aprovado"
class AprovadoStrategy(EstrategiaStatus):
    def executar_acao(self, ppc):
        # Não permite alterações após a aprovação.
        print(f"PPC '{ppc.titulo}' está aprovado. Não é permitido fazer alterações.")
        # Aqui, você pode adicionar uma verificação para impedir alterações no PPC após aprovação.
        if ppc.status == 'Aprovado':
            raise Exception("Não é possível modificar um PPC aprovado.")

# Estratégia para o status "Em Criação"
class EmCriacaoStrategy(EstrategiaStatus):
    def executar_acao(self, ppc):
        # Acesse os atributos usando ponto
        print(f"PPC '{ppc.titulo}' está em criação. Você pode adicionar colaboradores.")
        # Aqui, podemos permitir a adição de colaboradores, por exemplo.
        # ppc.add_colaboradores()

# Estratégia para o status "Em Avaliação"
class EmAvaliacaoStrategy(EstrategiaStatus):
    def executar_acao(self, ppc):
        # Acesse os atributos usando ponto
        print(f"PPC '{ppc.titulo}' está em avaliação. Você pode adicionar avaliadores.")
        # Aqui, podemos permitir que avaliadores adicionem suas avaliações, por exemplo.
        # ppc.add_avaliadores()



