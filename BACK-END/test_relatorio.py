# Importar as dependências necessárias para os testes
from DATABASE.conexao import conectar, fechar_conexao
from DATABASE.ppcCRUD import PPCCrud
from DATABASE.pessoaCrud import PessoaCRUD
from DATABASE.relatorio import Relatorio

# Função de teste completa
def executar_teste():
    try:
        # Estabelecer conexão com o banco de dados
        conexao = conectar()

        if conexao and conexao.is_connected():
            print("Conexão estabelecida para os testes.\n")

            # Inserir dados de teste para Pessoa
            PessoaCRUD.inserir(conexao, nome="João Coordenador", email="joao@exemplo.com", papel="Coordenador")
            PessoaCRUD.inserir(conexao, nome="Maria Colaboradora", email="maria@exemplo.com", papel="Colaborador")
            PessoaCRUD.inserir(conexao, nome="Ana Avaliadora", email="ana@exemplo.com", papel="Avaliador")

            # Criar um PPC
            print("\nCriando PPC...")
            PPCCrud.criar(conexao, titulo="PPC Teste", descricao="Descrição do PPC de Teste", coordenador_id=1)

            # Recuperar PPC criado
            ppc_criado = PPCCrud.buscar_por_id(conexao, 1)
            if not ppc_criado:
                print("Erro: PPC não foi criado corretamente!")
                return

            print(f"PPC criado: {ppc_criado}")

            # Adicionar colaborador ao PPC
            print("\nAdicionando colaborador...")
            PPCCrud.atualizar(conexao, ppc_id=1, colaboradores=["Maria Colaboradora"])

            # Enviar PPC para avaliação
            print("\nEnviando PPC para avaliação...")
            PPCCrud.atualizar(conexao, ppc_id=1, status="Em Avaliacao")

            # Aprovar o PPC
            print("\nAprovando PPC...")
            PPCCrud.atualizar(conexao, ppc_id=1, status="Aprovado")

            # Gerar relatórios
            print("\nGerando relatórios...")
            relatorio = Relatorio(ppc_id=1)
            colaboradores = relatorio.gerarRelatorioColaboradores(conexao)
            avaliadores = relatorio.gerarRelatorioAvaliadores(conexao)
            participantes = relatorio.gerarRelatorioParticipantes(conexao)

            print(f"Colaboradores: {colaboradores}")
            print(f"Avaliadores: {avaliadores}")
            print(f"Participantes: {participantes}")

    except Exception as e:
        print(f"Ocorreu um erro durante os testes: {e}")

    finally:
        # Fechar conexão com o banco de dados
        if conexao:
            fechar_conexao(conexao)
            print("\nConexão com o banco de dados foi encerrada.")

# Executar o teste
executar_teste()
