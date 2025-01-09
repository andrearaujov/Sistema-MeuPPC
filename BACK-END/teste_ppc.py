from DATABASE.conexao import conectar, fechar_conexao
from DATABASE.ppc import PPC

def testar_ppc():
    try:
        # Conectar ao banco de dados
        conexao = conectar()

        print("\n--- TESTANDO CRUD DA CLASSE PPC ---\n")

        # Teste 1: Criar PPC
        print("1. Criando PPC...")
        PPC.criar(conexao, "PPC de Matemática", "Curso voltado para ensino básico de matemática.", 1)  # Substituir '1' pelo coordenador_id válido
        PPC.criar(conexao, "PPC de Física", "Curso de física moderna e clássica.", 2)  # Substituir '2' pelo coordenador_id válido
        print("PPCs criados com sucesso!\n")

        # Teste 2: Listar todos os PPCs
        print("2. Listando todos os PPCs...")
        ppcs = PPC.listar_todos(conexao)
        for ppc in ppcs:
            print(ppc)
        print("\n")

        # Teste 3: Buscar PPC por ID
        print("3. Buscando PPC com ID = 1...")
        ppc = PPC.buscar_por_id(conexao, 1)
        print(ppc)
        print("\n")

        # Teste 4: Atualizar PPC
        print("4. Atualizando PPC com ID = 1...")
        PPC.atualizar(conexao, 1, titulo="PPC de Matemática Avançada", descricao="Curso revisado com foco em matemática aplicada.")
        ppc_atualizado = PPC.buscar_por_id(conexao, 1)
        print("PPC atualizado:", ppc_atualizado)
        print("\n")

        # Teste 5: Deletar PPC
        print("5. Deletando PPC com ID = 2...")
        PPC.deletar(conexao, 2)
        ppcs_restantes = PPC.listar_todos(conexao)
        print("PPCs restantes:", ppcs_restantes)
        print("\n")

        print("--- FIM DOS TESTES ---\n")

    except Exception as e:
        print(f"Ocorreu um erro durante os testes: {e}")

    finally:
        if conexao:
            fechar_conexao(conexao)

if __name__ == "__main__":
    testar_ppc()
