// cypress/e2e/relatorios.cy.js

describe('Testes de Relatórios', () => {
  const timestamp = Date.now();
  const coordenador = {
    nome: 'Coordenador Relatorio',
    email: `coordenador.relatorio${timestamp}@example.com`,
    password: 'senha123',
    papel: 'Coordenador'
  };

  const colaborador = {
    nome: 'Colaborador Relatorio',
    email: `colaborador.relatorio${timestamp}@example.com`,
    password: 'senha123',
    papel: 'Colaborador'
  };

  const avaliador = {
    nome: 'Avaliador Relatorio',
    email: `avaliador.relatorio${timestamp}@example.com`,
    password: 'senha123',
    papel: 'Avaliador'
  };

  const ppcTitulo = `PPC Relatorio ${timestamp}`;
  const ppcDescricao = 'Descrição do PPC para testes de relatório';

  before(() => {
    // Registrar o coordenador
    cy.visit('/register');
    cy.get('input[placeholder="Nome"]').type(coordenador.nome);
    cy.get('input[placeholder="E-mail"]').type(coordenador.email);
    cy.get('input[placeholder="Senha"]').type(coordenador.password);
    cy.get('input[placeholder="Confirme a Senha"]').type(coordenador.password);
    cy.get('select').select(coordenador.papel);
    cy.get('button[type="submit"]').click();

    // Registrar o colaborador
    cy.visit('/register');
    cy.get('input[placeholder="Nome"]').type(colaborador.nome);
    cy.get('input[placeholder="E-mail"]').type(colaborador.email);
    cy.get('input[placeholder="Senha"]').type(colaborador.password);
    cy.get('input[placeholder="Confirme a Senha"]').type(colaborador.password);
    cy.get('select').select(colaborador.papel);
    cy.get('button[type="submit"]').click();

    // Registrar o avaliador
    cy.visit('/register');
    cy.get('input[placeholder="Nome"]').type(avaliador.nome);
    cy.get('input[placeholder="E-mail"]').type(avaliador.email);
    cy.get('input[placeholder="Senha"]').type(avaliador.password);
    cy.get('input[placeholder="Confirme a Senha"]').type(avaliador.password);
    cy.get('select').select(avaliador.papel);
    cy.get('button[type="submit"]').click();
  });

  it('Fluxo completo de relatórios e avaliação de PPC', () => {
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

    // Verificar se o PPC aparece na lista
    cy.contains(ppcTitulo, { timeout: 10000 }).should('be.visible');
    cy.contains(ppcTitulo).parent().contains('Editar').click();

    // Adicionar colaborador
    cy.get('input[placeholder="Email do colaborador"]').type(colaborador.email);
    cy.contains('Adicionar Colaborador').click();
    cy.contains('Colaborador adicionado com sucesso!', { timeout: 10000 }).should('be.visible');

    // Voltar ao dashboard
    cy.contains('Voltar').click();
    cy.contains('Home').click();

    // Navegar para seleção de PPC para relatórios
    cy.contains('Relatórios').click();

    // Aguarde o carregamento do select e das opções
    cy.get('select').should('be.visible');

    // Aguarde até que o PPC esteja disponível na lista
    cy.get('select').contains('option', ppcTitulo, { timeout: 10000 }).should('exist');

    // Selecionar o PPC criado
    cy.get('select').select(ppcTitulo);

    // **Teste do Relatório de Participantes**
    cy.contains('Relatório de Participantes').click();
    cy.contains('Relatório de Participantes').should('be.visible');
    cy.contains('Colaboradores').should('be.visible');
    cy.contains(colaborador.nome).should('be.visible');
    cy.contains(colaborador.email).should('be.visible');

    // Voltar para a seleção de relatórios
    cy.contains('Voltar').click();

    // Voltar para o PPC para enviar para avaliação
    cy.contains('Home').click();
    cy.contains('Gerenciar PPCs').click();
    cy.contains(ppcTitulo).parent().contains('Editar').click();

    // Enviar para avaliação
    cy.get('input[placeholder="E-mails dos avaliadores, separados por vírgula"]').type(avaliador.email);
    cy.contains('Enviar para Avaliação').click();
    cy.contains('PPC enviado para avaliação com sucesso!', { timeout: 10000 }).should('be.visible');

    // Logar como avaliador para avaliar o PPC
    cy.visit('/');
    cy.get('input[placeholder="E-mail"]').type(avaliador.email);
    cy.get('input[placeholder="Senha"]').type(avaliador.password);
    cy.get('button[type="submit"]').click();

    // Avaliar o PPC
    cy.contains('PPCs Não Avaliados').click();
    cy.contains(ppcTitulo).should('be.visible');
    cy.contains(ppcTitulo).parent().find('button').contains('Aprovar').click();
    cy.contains('PPC aprovado com sucesso!', { timeout: 10000 }).should('be.visible');

    // Logar como colaborador para verificar PPCs avaliados
    cy.visit('/');
    cy.get('input[placeholder="E-mail"]').type(colaborador.email);
    cy.get('input[placeholder="Senha"]').type(colaborador.password);
    cy.get('button[type="submit"]').click();

    // Verificar 'PPCs Avaliados' no dashboard do colaborador
    cy.contains('PPCs Avaliados').click();
    cy.contains(ppcTitulo, { timeout: 10000 }).should('be.visible');
    cy.contains(ppcTitulo).should('be.visible');
    cy.contains('Status: Aprovado').should('be.visible');

    // Voltar para o dashboard
    cy.contains('Voltar').click();

    // Navegar para "PPCs Avaliados Relatórios"
    cy.contains('PPCs Avaliados Relatórios').click();

    // Verificar se o PPC avaliado aparece
    cy.contains(ppcTitulo, { timeout: 10000 }).should('be.visible');
    cy.contains(ppcTitulo).should('be.visible');

    // Opcional: Verificar relatórios como colaborador
    cy.contains(ppcTitulo).parent().contains('Relatório de Participantes').click();
    cy.contains('Relatório de Participantes').should('be.visible');
    cy.contains('Colaboradores').should('be.visible');
    cy.contains(colaborador.nome).should('be.visible');
    cy.contains('Avaliadores').should('be.visible');
    cy.contains(avaliador.nome).should('be.visible');

    // Voltar para o dashboard
    cy.contains('Voltar').click();
  });
});
