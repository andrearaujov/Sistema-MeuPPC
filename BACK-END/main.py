# Importando a função de conexão de 'DATABASE.conexao'
from DATABASE.conexao import conectar
from DATABASE.pessoa import Pessoa

def main():
    try:
        # Conectando ao banco de dados
        conexao = conectar()

        if conexao.is_connected():
            print("Conexão com o banco de dados MySQL foi estabelecida com sucesso!")

        # Inserir uma nova pessoa
        Pessoa.inserir(conexao, "João Silva", "joao@exemplo.com", "Coordenador")

        # Listar todas as pessoas
        pessoas = Pessoa.listar_todas(conexao)
        print("Pessoas cadastradas:", pessoas)

        # Buscar pessoa por ID
        pessoa = Pessoa.buscar_por_id(conexao, 1)
        print("Pessoa encontrada:", pessoa)

        # Atualizar uma pessoa
        Pessoa.atualizar(conexao, 1, nome="João Pedro", email="joao.pedro@exemplo.com")

        # Deletar uma pessoa

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()
            print("Conexão com o MySQL foi encerrada.")

if __name__ == "__main__":
    main()
