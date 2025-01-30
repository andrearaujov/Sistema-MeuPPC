// cypress/support/commands.js

Cypress.Commands.add('register', (user) => {
    cy.visit('/register');
    cy.get('input[name="nome"]').type(user.nome);
    cy.get('input[name="email"]').type(user.email);
    cy.get('input[name="password"]').type(user.password);
    cy.get('select[name="papel"]').select(user.papel);
    cy.get('button[type="submit"]').click();
  });
  
  Cypress.Commands.add('login', (email, password) => {
    cy.visit('/login');
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="password"]').type(password);
    cy.get('button[type="submit"]').click();
  });
  