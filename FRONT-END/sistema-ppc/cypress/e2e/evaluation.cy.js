// cypress/e2e/evaluation.cy.js

describe('Testes de Avaliação', () => {
  const timestamp = Date.now();

  const avaliador = {
    nome: 'Avaliador Teste',
    email: `avaliador${timestamp}@example.com`,
    password: 'senha123',
    papel: 'Avaliador'
  };

  const coordenador = {
    nome: 'Coordenador Teste',
    email: `coordenador${timestamp}@example.com`,
    password: 'senha123',
    papel: 'Coordenador'
  };

  const ppcTitulo = `PPC de Teste ${timestamp}`;
  const ppcDescricao = 'Descrição do PPC de Teste';

  before(() => {
    // Registrar o avaliador
    cy.visit('/register');
    cy.get('input[placeholder="Nome"]').type(avaliador.nome);
    cy.get('input[placeholder="E-mail"]').type(avaliador.email);
    cy.get('input[placeholder="Senha"]').type(avaliador.password);
    cy.get('input[placeholder="Confirme a Senha"]').type(avaliador.password);
    cy.get('select').select(avaliador.papel);
    cy.get('button[type="submit"]').click();

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

    // Criar um PPC
    cy.contains('Criar PPC').click();
    cy.get('input[placeholder="Título"]').type(ppcTitulo);
    cy.get('textarea[placeholder="Descrição"]').type(ppcDescricao);
    cy.get('button[type="submit"]').contains('Criar').click();

    // Verificar se o PPC foi criado com sucesso
    cy.contains(ppcTitulo).should('be.visible');

    // Navegar para a página de edição do PPC
    cy.contains(ppcTitulo).parent().contains('Editar').click();

    // Enviar para avaliação
    cy.get('input[placeholder="E-mails dos avaliadores, separados por vírgula"]').type(avaliador.email);
    cy.contains('Enviar para Avaliação').click();

    // Verificar se houve mensagem de sucesso
    cy.contains('PPC enviado para avaliação com sucesso!').should('be.visible');
  });

  it('Avaliador deve aprovar o PPC', () => {
    // Logar como avaliador
    cy.visit('/');
    cy.get('input[placeholder="E-mail"]').type(avaliador.email);
    cy.get('input[placeholder="Senha"]').type(avaliador.password);
    cy.get('button[type="submit"]').click();

    // Navegar para PPCs não avaliados
    cy.contains('PPCs Não Avaliados').click();

    // Aprovar PPC
    cy.contains(ppcTitulo).parent().contains('Aprovar').click();

    // Verificar se houve mensagem de sucesso
    cy.contains('PPC aprovado com sucesso!').should('be.visible');
  });

  it('Avaliador deve rejeitar o PPC', () => {
    // Logar como avaliador
    cy.visit('/');
    cy.get('input[placeholder="E-mail"]').type(avaliador.email);
    cy.get('input[placeholder="Senha"]').type(avaliador.password);
    cy.get('button[type="submit"]').click();

    // Navegar para PPCs não avaliados
    cy.contains('PPCs Não Avaliados').click();

    // Rejeitar PPC
    cy.contains(ppcTitulo).parent().find('textarea').type('Rejeitado por não atender aos critérios.');
    cy.contains(ppcTitulo).parent().contains('Rejeitar').click();

    // Verificar se houve mensagem de sucesso
    cy.contains('PPC rejeitado com sucesso!').should('be.visible');
  });

  it('Avaliador não deve poder editar o PPC', () => {
    // Logar como avaliador
    cy.visit('/');
    cy.get('input[placeholder="E-mail"]').type(avaliador.email);
    cy.get('input[placeholder="Senha"]').type(avaliador.password);
    cy.get('button[type="submit"]').click();

    // Tentar acessar a página de edição do PPC
    cy.visit(`/ppcs/${ppcTitulo}`, { failOnStatusCode: false });

    // Verificar se o acesso foi negado ou redirecionado
    cy.contains('Acesso negado').should('be.visible');
  });
});
