# Importando a função de conexão de 'DATABASE.conexao'
from DATABASE.conexao import conectar, fechar_conexao
from DATABASE.pessoa import Pessoa

def main():
    try:
        # Conectando ao banco de dados
        conexao = conectar()

        if conexao.is_connected():
            print("Conexão com o banco de dados MySQL foi estabelecida com sucesso!")

        # Inserir uma nova pessoa
        Pessoa.inserir(conexao, "João Silva", "joao@exemplo.com", "Coordenador")
        Pessoa.inserir(conexao, "Maria Oliveira", "maria@exemplo.com", "Colaborador")
        Pessoa.inserir(conexao, "Ana Costa", "ana@exemplo.com", "Avaliador")
        
        # Listar todas as pessoas
        pessoas = Pessoa.listar_todas(conexao)
        print("Pessoas cadastradas:", pessoas)

        # Buscar pessoa por ID
        pessoa = Pessoa.buscar_por_id(conexao, 1)
        print("Pessoa encontrada:", pessoa)

        # Atualizar uma pessoa
        Pessoa.atualizar(conexao, 1, nome="João Pedro", email="joao.pedro@exemplo.com")

        # Buscar novamente para verificar a atualização
        pessoa_atualizada = Pessoa.buscar_por_id(conexao, 1)
        print("Pessoa após atualização:", pessoa_atualizada)

        # Deletar uma pessoa

        # Verificar a exclusão
        pessoas_restantes = Pessoa.listar_todas(conexao)
        print("Pessoas restantes após exclusão:", pessoas_restantes)

        # Deletar todas as pessoas

        # Verificar se todas foram deletadas
        pessoas_vazias = Pessoa.listar_todas(conexao)
        print("Pessoas restantes após deletar todas:", pessoas_vazias)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    finally:
        if conexao:
            fechar_conexao(conexao)

if __name__ == "__main__":
    main()
