# Supondo que você tenha as estratégias e a classe PPC configuradas
from DATABASE.estrategiaStatus import AprovadoStrategy, EmCriacaoStrategy, EmAvaliacaoStrategy
from DATABASE.ppc import PPC  # Se a classe PPC estiver nesse caminho

# Criando instâncias de PPC
ppc_criacao = PPC(id=1, titulo="PPC de Matemática", status="Em Criacao")
ppc_avaliacao = PPC(id=2, titulo="PPC de Física", status="Em Avaliacao")
ppc_aprovado = PPC(id=3, titulo="PPC de Química", status="Aprovado")

# Testando PPC em criação
print(f"Status inicial do PPC '{ppc_criacao.titulo}': {ppc_criacao.status}")
ppc_criacao.adicionar_colaborador("João")
ppc_criacao.enviar_para_avaliacao(["Carlos", "Ana"])
ppc_criacao.executar_acao()

# Testando PPC em avaliação
print(f"\nStatus inicial do PPC '{ppc_avaliacao.titulo}': {ppc_avaliacao.status}")
ppc_avaliacao.adicionar_colaborador("Maria")  # Não deve permitir adicionar
ppc_avaliacao.enviar_para_avaliacao(["Felipe", "Lucas"])
ppc_avaliacao.aprovar()
ppc_avaliacao.executar_acao()

# Testando PPC aprovado
print(f"\nStatus inicial do PPC '{ppc_aprovado.titulo}': {ppc_aprovado.status}")
ppc_aprovado.adicionar_colaborador("Paulo")  # Não deve permitir adicionar
ppc_aprovado.enviar_para_avaliacao(["Simone", "Gustavo"])  # Não deve permitir enviar
ppc_aprovado.aprovar()  # Não deve permitir aprovar novamente
ppc_aprovado.executar_acao()
