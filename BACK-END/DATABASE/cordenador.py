from DATABASE.pessoa import Pessoa
from DATABASE.ppcCRUD import PPCCrud
from DATABASE.ppc import PPC

class Coordenador(Pessoa):
    def criarPPC(self, conexao, titulo, descricao):
        """
        Cria um novo PPC e associa ao coordenador atual.
        """
        try:
            PPCCrud.criar(conexao, titulo, descricao, self.id)
            # Atribuir o PPC criado ao coordenador
            self.ppc = PPC(id=1, titulo=titulo, descricao=descricao, coordenador_id=self.id, status="Em Criacao")  # Substitua o id 1 com o id real do PPC criado
            print(f"PPC '{titulo}' criado com sucesso pelo coordenador {self.nome}.")
        except Exception as e:
            print(f"Erro ao criar PPC: {e}")

    def atribuirColaborador(self, conexao, ppc_id, colaborador_id):
        """
        Adiciona um colaborador ao PPC.
        """
        try:
            cursor = conexao.cursor()
            query = """
                INSERT INTO ppc_colaboradores (ppc_id, colaborador_id)
                VALUES (%s, %s)
            """
            cursor.execute(query, (ppc_id, colaborador_id))
            conexao.commit()
            print(f"Colaborador ID {colaborador_id} atribuído ao PPC ID {ppc_id}.")
        except Exception as e:
            print(f"Erro ao atribuir colaborador: {e}")

    def enviarParaAvaliacao(self, conexao, ppc_id, avaliadores):
        """
        Altera o status do PPC para "Em Avaliação" e associa avaliadores ao PPC.
        """
        try:
            # Atualizar o status do PPC
            PPCCrud.atualizar(conexao, ppc_id, status="Em Avaliacao")
            
            # Associar avaliadores ao PPC
            cursor = conexao.cursor()
            query = """
                INSERT INTO ppc_avaliadores (ppc_id, avaliador_id)
                VALUES (%s, %s)
            """
            for avaliador in avaliadores:
                cursor.execute(query, (ppc_id, avaliador.id))
            conexao.commit()
            print(f"PPC ID {ppc_id} enviado para avaliação.")
        except Exception as e:
            print(f"Erro ao enviar PPC para avaliação: {e}")
