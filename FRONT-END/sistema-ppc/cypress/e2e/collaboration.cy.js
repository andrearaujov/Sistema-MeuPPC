describe('Testes de Colaboração', () => {
    const timestamp = Date.now();
    const colaborador = {
      nome: 'Colaborador Teste',
      email: `colaborador${timestamp}@example.com`,
      password: 'senha123',
      papel: 'Colaborador'
    };
  
    const coordenador = {
      nome: 'Coordenador Teste',
      email: `coordenador${timestamp}@example.com`,
      password: 'senha123',
      papel: 'Coordenador'
    };
  
    const ppcTitulo = 'PPC de Teste';
    const ppcDescricao = 'Descrição do PPC de Teste';
  
    before(() => {
      // Registrar o colaborador
      cy.visit('/register');
      cy.get('input[placeholder="Nome"]').type(colaborador.nome);
      cy.get('input[placeholder="E-mail"]').type(colaborador.email);
      cy.get('input[placeholder="Senha"]').type(colaborador.password);
      cy.get('input[placeholder="Confirme a Senha"]').type(colaborador.password);
      cy.get('select').select(colaborador.papel);
      cy.get('button[type="submit"]').click();
  
      // Registrar o coordenador
      cy.visit('/register');
      cy.get('input[placeholder="Nome"]').type(coordenador.nome);
      cy.get('input[placeholder="E-mail"]').type(coordenador.email);
      cy.get('input[placeholder="Senha"]').type(coordenador.password);
      cy.get('input[placeholder="Confirme a Senha"]').type(coordenador.password);
      cy.get('select').select(coordenador.papel);
      cy.get('button[type="submit"]').click();
    });
  
    it('Coordenador deve adicionar um colaborador ao PPC', () => {
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
  
      // Navegar para a página de edição do PPC
      cy.contains(ppcTitulo).parent().contains('Editar').click();
  
      // Adicionar colaborador
      cy.get('input[placeholder="Email do colaborador"]').type(colaborador.email);
      cy.contains('Adicionar Colaborador').click();
  
      // Verificar se houve mensagem de sucesso
      cy.contains('Colaborador adicionado com sucesso', { timeout: 10000 }).should('be.visible');
    });
  
 
  
  
    it('Colaborador deve editar o PPC ao qual foi adicionado', () => {
      // Logar como colaborador
      cy.visit('/');
      cy.get('input[placeholder="E-mail"]').type(colaborador.email);
      cy.get('input[placeholder="Senha"]').type(colaborador.password);
      cy.get('button[type="submit"]').click();
  
      // Navegar para a lista de PPCs
      cy.contains('Gerenciar PPCs').click();
  
      // Editar PPC
      cy.contains(ppcTitulo).parent().contains('Editar').click();
      cy.get('textarea[placeholder="Descrição"]').clear().type(`${ppcDescricao} - Editado pelo colaborador`);
      cy.contains('Salvar').click();
  
      // Verificar se as mudanças foram aplicadas
      cy.contains(`${ppcDescricao} - Editado pelo colaborador`).should('be.visible');
    });
  });
  