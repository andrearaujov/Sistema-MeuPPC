describe('Testes de Relatórios', () => {
    it('Deve visualizar o relatório de participantes de um PPC', () => {
      // Logar como coordenador
      // Criar um PPC e adicionar colaborador e avaliador, se ainda não feito
  
      // Navegar para seleção de PPC
      cy.contains('Relatórios').click();
      cy.get('select').select('PPC de Teste');
      cy.contains('Relatório de Participantes').click();
  
      // Verificar se os dados estão presentes
      cy.contains('Colaboradores').should('be.visible');
      cy.contains('Avaliadores').should('be.visible');
    });
  });
  