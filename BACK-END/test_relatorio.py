from DATABASE.conexao import conectar, fechar_conexao
from DATABASE.relatorio import Relatorio

def testar_relatorios():
    try:
        conexao = conectar()
        if conexao.is_connected():
            print("Conexão com o banco de dados MySQL foi estabelecida com sucesso!")

        # Define o ID do PPC a ser testado
        ppc_id = 1
        
        print(f"\nTestando relatórios para o PPC com ID {ppc_id}:\n")

        # Instanciar a classe Relatorio com o ID do PPC
        relatorio = Relatorio(ppc_id=ppc_id)

        # Testar relatório de colaboradores
        print("Relatório de Colaboradores:")
        try:
            colaboradores = relatorio.gerarRelatorioColaboradores(conexao)
            if colaboradores:
                for colaborador in colaboradores:
                    print(f"- {colaborador['nome']} ({colaborador['email']})")
            else:
                print("Nenhum colaborador encontrado para este PPC.")
        except Exception as e:
            print(f"Erro ao gerar relatório de colaboradores: {e}")

        # Testar relatório de avaliadores
        print("\nRelatório de Avaliadores:")
        try:
            avaliadores = relatorio.gerarRelatorioAvaliadores(conexao)
            if avaliadores:
                for avaliador in avaliadores:
                    print(f"- {avaliador['nome']} ({avaliador['email']})")
            else:
                print("Nenhum avaliador encontrado para este PPC.")
        except Exception as e:
            print(f"Erro ao gerar relatório de avaliadores: {e}")

        # Testar relatório de participantes
        print("\nRelatório de Participantes (Colaboradores e Avaliadores):")
        try:
            participantes = relatorio.gerarRelatorioParticipantes(conexao)
            if participantes:
                for colaborador in participantes["colaboradores"]:
                    print(f"Colaborador: {colaborador['nome']} ({colaborador['email']})")
                for avaliador in participantes["avaliadores"]:
                    print(f"Avaliador: {avaliador['nome']} ({avaliador['email']})")
            else:
                print("Nenhum participante encontrado para este PPC.")
        except Exception as e:
            print(f"Erro ao gerar relatório de participantes: {e}")

    except Exception as e:
        print(f"Ocorreu um erro durante os testes de relatórios: {e}")

    finally:
        if conexao:
            fechar_conexao(conexao)
            print("Conexão com o MySQL foi encerrada.")


if __name__ == "__main__":
    testar_relatorios()
