describe('Testes de Avaliação', () => {
    const avaliador = {
      nome: 'Avaliador Teste',
      email: 'avaliador@example.com',
      password: 'senha123',
      papel: 'Avaliador'
    };
  
    before(() => {
      // Registrar o avaliador
      cy.visit('/register');
      // Utilize os passos para registrar o avaliador
  
      // Logar como coordenador
      // Criar um PPC
      // Navegar para a página de edição do PPC
  
      // Enviar para avaliação
      cy.get('input[placeholder="IDs dos avaliadores, separados por vírgula"]').type('1'); // Use o ID do avaliador registrado
      cy.contains('Enviar para Avaliação').click();
  
      // Verificar se houve mensagem de sucesso
      cy.contains('PPC enviado para avaliação com sucesso').should('be.visible');
    });
    it('Avaliador deve aprovar o PPC', () => {
        // Logar como avaliador
        cy.visit('/');
        cy.get('input[placeholder="E-mail"]').type(avaliador.email);
        // Continue com o login
      
        // Navegar para PPCs não avaliados
        cy.contains('PPCs Não Avaliados').click();
      
        // Aprovar PPC
        cy.contains('PPC de Teste').parent().contains('Aprovar').click();
      
        // Verificar se houve mensagem de sucesso
        cy.contains('PPC aprovado com sucesso').should('be.visible');
      });
      it('Avaliador deve aprovar o PPC', () => {
        // Logar como avaliador
        cy.visit('/');
        cy.get('input[placeholder="E-mail"]').type(avaliador.email);
        // Continue com o login
      
        // Navegar para PPCs não avaliados
        cy.contains('PPCs Não Avaliados').click();
      
        // Aprovar PPC
        cy.contains('PPC de Teste').parent().contains('Aprovar').click();
      
        // Verificar se houve mensagem de sucesso
        cy.contains('PPC aprovado com sucesso').should('be.visible');
      });
      it('Avaliador deve rejeitar o PPC', () => {
        // Logar como avaliador
        // Navegar para PPCs não avaliados
      
        // Rejeitar PPC
        cy.contains('PPC de Teste').parent().find('textarea').type('Rejeitado por não atender aos critérios.');
        cy.contains('PPC de Teste').parent().contains('Rejeitar').click();
      
        // Verificar se houve mensagem de sucesso
        cy.contains('PPC rejeitado com sucesso').should('be.visible');
      });
      
  });
  