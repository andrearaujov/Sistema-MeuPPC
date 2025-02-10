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

  const ppcTitulo1 = `PPC de Teste 1 ${timestamp}`;
  const ppcDescricao1 = 'Descrição do PPC de Teste 1';
  
  const ppcTitulo2 = `PPC de Teste 2 ${timestamp}`;
  const ppcDescricao2 = 'Descrição do PPC de Teste 2';

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

    // Criar PPC 1
    cy.contains('Criar PPC').click();
    cy.get('input[placeholder="Título"]').type(ppcTitulo1);
    cy.get('textarea[placeholder="Descrição"]').type(ppcDescricao1);
    cy.get('button[type="submit"]').contains('Criar').click();
    cy.contains(ppcTitulo1).should('be.visible');
    cy.contains(ppcTitulo1).parent().contains('Editar').click();
    cy.get('input[placeholder="E-mails dos avaliadores, separados por vírgula"]').type(avaliador.email);
    cy.contains('Enviar para Avaliação').click();
    cy.contains('PPC enviado para avaliação com sucesso!').should('be.visible');

    // Voltar ao dashboard
    cy.contains('Voltar').click(); 

    // Criar PPC 2
    cy.contains('Criar Novo PPC').click();
    cy.get('input[placeholder="Título"]').type(ppcTitulo2);
    cy.get('textarea[placeholder="Descrição"]').type(ppcDescricao2);
    cy.get('button[type="submit"]').contains('Criar').click();
    cy.contains(ppcTitulo2).should('be.visible');
    cy.contains(ppcTitulo2).parent().contains('Editar').click();
    cy.get('input[placeholder="E-mails dos avaliadores, separados por vírgula"]').type(avaliador.email);
    cy.contains('Enviar para Avaliação').click();
    cy.contains('PPC enviado para avaliação com sucesso!').should('be.visible');
  });

  it('Avaliador deve aprovar o PPC 1', () => {
    // Logar como avaliador
    cy.visit('/');
    cy.get('input[placeholder="E-mail"]').type(avaliador.email);
    cy.get('input[placeholder="Senha"]').type(avaliador.password);
    cy.get('button[type="submit"]').click();

    // Navegar para PPCs não avaliados
    cy.contains('PPCs Não Avaliados').click();

    // Aprovar PPC 1
    cy.contains(ppcTitulo1).parent().contains('Aprovar').click();

    // Verificar se houve mensagem de sucesso
    cy.contains('PPC aprovado com sucesso!').should('be.visible');
  });

  it('Avaliador deve rejeitar o PPC 2', () => {
    // Logar como avaliador
    cy.visit('/');
    cy.get('input[placeholder="E-mail"]').type(avaliador.email);
    cy.get('input[placeholder="Senha"]').type(avaliador.password);
    cy.get('button[type="submit"]').click();

    // Navegar para PPCs não avaliados
    cy.contains('PPCs Não Avaliados').click();

    // Rejeitar PPC 2
    cy.contains(ppcTitulo2).parent().find('textarea').type('Rejeitado por não atender aos critérios.');
    cy.contains(ppcTitulo2).parent().contains('Rejeitar').click();

    // Verificar se houve mensagem de sucesso
    cy.contains('PPC rejeitado com sucesso!').should('be.visible');
  });

  it('Deve exibir PPCs já avaliados', () => {
    // Logar como avaliador
    cy.visit('/');
    cy.get('input[placeholder="E-mail"]').type(avaliador.email);
    cy.get('input[placeholder="Senha"]').type(avaliador.password);
    cy.get('button[type="submit"]').click();

    // Navegar para PPCs avaliados
    cy.contains('PPCs Avaliados').click();

    // Verificar se o PPC 1 aprovado está na lista de PPCs avaliados
    cy.contains(ppcTitulo1).should('be.visible');
    cy.contains('Status: Aprovado').should('be.visible');

    // Verificar se o PPC 2 rejeitado está na lista de PPCs avaliados
    cy.contains(ppcTitulo2).should('be.visible');
    cy.contains('Status: Rejeitado').should('be.visible');
    cy.contains('Motivo de Rejeição: Rejeitado por não atender aos critérios.').should('be.visible');
  });
});
