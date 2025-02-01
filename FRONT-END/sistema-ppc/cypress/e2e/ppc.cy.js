describe('Gestão de PPCs para Coordenador', () => {
  const timestamp = Date.now();
  const coordenador = {
    nome: 'Coordenador Teste',
    email: `coordenador${timestamp}@example.com`,
    password: 'senha123',
    papel: 'Coordenador'
  };

  const ppcTitulo = 'PPC de Teste';
  const ppcDescricao = 'Descrição do PPC de Teste';
  let novoTitulo; // Declarar 'novoTitulo' no escopo superior

  before(() => {
    // Registrar o coordenador
    cy.visit('/register');
    cy.get('input[placeholder="Nome"]').type(coordenador.nome);
    cy.get('input[placeholder="E-mail"]').type(coordenador.email);
    cy.get('input[placeholder="Senha"]').type(coordenador.password);
    cy.get('input[placeholder="Confirme a Senha"]').type(coordenador.password);
    cy.get('select').select(coordenador.papel);
    cy.get('button[type="submit"]').click();

    // Logar como coordenador
    cy.visit('/');
    cy.get('input[placeholder="E-mail"]').type(coordenador.email);
    cy.get('input[placeholder="Senha"]').type(coordenador.password);
    cy.get('button[type="submit"]').click();
  });

  it('Deve criar e editar um novo PPC', () => {
    // A partir do dashboard
    cy.contains('Criar PPC').click();

    // Preencher o formulário de criação de PPC
    cy.get('input[placeholder="Título"]').type(ppcTitulo);
    cy.get('textarea[placeholder="Descrição"]').type(ppcDescricao);
    cy.get('button[type="submit"]').contains('Criar').click();

    // Verificar se o PPC aparece na lista
    cy.contains(ppcTitulo, { timeout: 10000 }).should('be.visible');

    // Encontrar o PPC criado e clicar em "Editar"
    cy.contains(ppcTitulo).parent().contains('Editar').click();

    // Esperar o PPC ser carregado
    cy.contains('h1', 'Editar PPC').should('be.visible');

    novoTitulo = `${ppcTitulo} Editado`;

    // Alterar o título
    cy.get('input[placeholder="Título"]').clear().type(novoTitulo);

    // Alterar a descrição
    cy.get('textarea[placeholder="Descrição"]').clear().type(`${ppcDescricao} - Editada pelo coordenador`);

    // Clicar em "Salvar"
    cy.get('button').contains('Salvar').click();

    // Verificar se a mensagem de sucesso é exibida

    // Verificar se foi redirecionado para a lista de PPCs
    cy.url().should('include', '/ppcs');

    // Verificar se as mudanças foram aplicadas
    cy.contains(novoTitulo, { timeout: 10000 }).should('be.visible');

    // Verificar se o PPC aparece na lista usando 'novoTitulo'
    cy.contains(novoTitulo, { timeout: 10000 }).should('exist');

    // Encontrar o PPC e clicar em "Excluir"
    cy.contains(novoTitulo).parent().find('.delete-btn').click();

    // Confirmar o diálogo de confirmação, se houver
    cy.on('window:confirm', () => true);

    // Verificar se o PPC foi removido
    cy.contains(novoTitulo).should('not.exist');
  
    // Confirmar o diálogo de confirmação, se houver
    cy.on('window:confirm', () => true);

    // Verificar se o PPC foi removido
    cy.contains(novoTitulo).should('not.exist');
  });

  
});
