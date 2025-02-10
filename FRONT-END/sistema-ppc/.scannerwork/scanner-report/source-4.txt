describe('Testes de Autenticação', () => {
    const user = {
      nome: 'Usuário Teste',
      email: 'teste@example.com',
      password: 'senha123',
      papel: 'Coordenador'
    };
  
   

    it('Deve registrar um novo usuário', () => {
      cy.visit('/register');
  
      cy.get('input[placeholder="Nome"]').type(user.nome);
      cy.get('input[placeholder="E-mail"]').type(user.email);
      cy.get('input[placeholder="Senha"]').type(user.password);
      cy.get('input[placeholder="Confirme a Senha"]').type(user.password);
      cy.get('select').select(user.papel);
      cy.contains('Registrar').click();
  
      // Verifica se foi redirecionado para a página de login
      cy.url().should('include', '/');
    });
    
     it('Deve realizar login com usuário registrado', () => {
    cy.visit('/');
  
    cy.get('input[placeholder="E-mail"]').type(user.email);
    cy.get('input[placeholder="Senha"]').type(user.password);
    cy.contains('Login').click();
  
    // Verifica se foi redirecionado para o dashboard
    cy.url().should('include', '/dashboard');
    cy.contains('PPC CRUD').should('be.visible');
  });
  });

  
  