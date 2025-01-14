# models/pessoa.py

class Pessoa:
    def __init__(self, id=None, nome=None, email=None, senha=None, papel=None, created_at=None, updated_at=None):
        """
        Inicializa uma instância da classe Pessoa.

        :param id: ID único da pessoa.
        :param nome: Nome da pessoa.
        :param email: E-mail único da pessoa.
        :param senha: Senha da pessoa (hasheada).
        :param papel: Papel da pessoa (Coordenador, Colaborador, Avaliador).
        :param created_at: Timestamp de criação.
        :param updated_at: Timestamp da última atualização.
        """
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.papel = papel
        self.created_at = created_at
        self.updated_at = updated_at

    def exibirDados(self):
        """
        Retorna os dados básicos da pessoa em formato legível.
        """
        return f"ID: {self.id}, Nome: {self.nome}, E-mail: {self.email}, Papel: {self.papel}"
