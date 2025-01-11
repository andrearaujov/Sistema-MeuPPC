from DATABASE.conexao import conectar, fechar_conexao
from DATABASE.pessoa import Pessoa
from DATABASE.ppc import PPC
from DATABASE.ppcCRUD import PPCCrud
from DATABASE.pessoaCrud import PessoaCRUD
from DATABASE.cordenador import Coordenador
from DATABASE.colaborador import Colaborador
from DATABASE.avaliador import Avaliador
from DATABASE.estrategiaStatus import EmCriacaoStrategy, EmAvaliacaoStrategy, AprovadoStrategy

def teste_coordenador(conexao):
    print("\n=== Testando Coordenador ===")
    
    # Criar um coordenador
    coordenador = Coordenador(id=1, nome="João Coordenador", email="joao@exemplo.com", papel="Coordenador")
    
    # Coordenador cria um PPC (status 'Em Criação')
    coordenador.criarPPC(conexao, "PPC 1", "Descrição do PPC 1")
    
    # Verificando estratégia inicial de 'Em Criação'
    ppc = coordenador.ppc
    print(f"Status inicial do PPC: {ppc.status}")
    ppc.executar_acao()  # Deve permitir adicionar colaboradores
    
    # Coordenador atribui um colaborador ao PPC
    coordenador.atribuirColaborador(conexao, 1, 2)  # Atribuindo colaborador com ID 2 ao PPC 1
    
    # Coordenador envia o PPC para avaliação (status 'Em Avaliação')
    avaliadores = [Avaliador(id=3, nome="Ana Avaliadora", email="ana@exemplo.com", papel="Avaliador")]
    coordenador.enviarParaAvaliacao(conexao, 1, avaliadores)

    # Verificando estratégia de 'Em Avaliação'
    ppc.set_status("Em Avaliacao")
    print(f"Status do PPC após envio para avaliação: {ppc.status}")
    ppc.executar_acao()  # Deve permitir a avaliação do PPC

def teste_colaborador(conexao):
    print("\n=== Testando Colaborador ===")
    
    # Criar um colaborador
    colaborador = Colaborador(id=2, nome="Maria Colaboradora", email="maria@exemplo.com", papel="Colaborador")
    
    # Colaborador tenta editar o PPC quando está em criação
    colaborador.editarPPC(conexao, 1, "Descrição atualizada pelo colaborador.")
    
    # Tentando adicionar colaborador no status 'Em Avaliação' (não permitido)
    colaborador.editarPPC(conexao, 1, "Outra tentativa de atualização.")

def teste_avaliador(conexao):
    print("\n=== Testando Avaliador ===")
    
    # Criar um avaliador
    avaliador = Avaliador(id=3, nome="Ana Avaliadora", email="ana@exemplo.com", papel="Avaliador")
    
    # Avaliador tenta avaliar o PPC
    avaliador.avaliarPPC(conexao, 1, aprovado=True)
    
    # Alterar status para 'Aprovado' e testar novamente
    avaliador.avaliarPPC(conexao, 1, aprovado=False)

def main():
    try:
        # Estabelecer a conexão com o banco de dados
        conexao = conectar()

        if conexao.is_connected():
            print("Conexão com o banco de dados MySQL foi estabelecida com sucesso!")

        # Inserindo dados iniciais para testes de pessoas
        PessoaCRUD.inserir(conexao, "João Coordenador", "joao@exemplo.com", "Coordenador")
        PessoaCRUD.inserir(conexao, "Maria Colaboradora", "maria@exemplo.com", "Colaborador")
        PessoaCRUD.inserir(conexao, "Ana Avaliadora", "ana@exemplo.com", "Avaliador")

        # Executando os testes
        teste_coordenador(conexao)
        teste_colaborador(conexao)
        teste_avaliador(conexao)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    finally:
        if conexao:
            # Fechar a conexão com o banco de dados
            fechar_conexao(conexao)
            print("Conexão com o MySQL foi encerrada.")

if __name__ == "__main__":
    main()
