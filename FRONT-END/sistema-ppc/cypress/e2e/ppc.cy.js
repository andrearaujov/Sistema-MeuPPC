describe('Gestão de PPCs para Coordenador', () => {
    before(() => {
      // Registrando e logando como coordenador
      cy.visit('/register');
      // Utilize os códigos do passo 2 para registrar e logar
    });
  
    it('Deve criar um novo PPC', () => {
      // A partir do dashboard
      cy.contains('Criar PPC').click();
  
      cy.get('input').contains(/Título:/i).next('input').type('PPC de Teste');
      cy.get('textarea').contains(/Descrição:/i).next('textarea').type('Descrição do PPC de Teste');
      cy.contains('Criar').click();
  
      // Verificar se o PPC aparece na lista
      cy.contains('PPC de Teste').should('be.visible');
    });

    it('Deve editar um PPC existente', () => {
        // Navegar para a página de PPCs
        cy.contains('Gerenciar PPCs').click();
      
        // Encontrar o PPC criado e clicar em "Editar"
        cy.contains('PPC de Teste').parent().contains('Editar').click();
      
        // Alterar o título e salvar
        cy.get('input').contains(/Título:/i).next('input').clear().type('PPC de Teste Editado');
        cy.contains('Salvar').click();
      
        // Verificar se as mudanças foram aplicadas
        cy.contains('PPC de Teste Editado').should('be.visible');
      });

      it('Deve deletar um PPC', () => {
        // Navegar para a página de PPCs
        cy.contains('Gerenciar PPCs').click();
      
        // Encontrar o PPC e clicar em "Excluir"
        cy.contains('PPC de Teste Editado').parent().find('.delete-btn').click();
      
        // Confirmar o diálogo, se houver
        cy.on('window:confirm', () => true);
      
        // Verificar se o PPC foi removido
        cy.contains('PPC de Teste Editado').should('not.exist');
      });
      
      
  });
  