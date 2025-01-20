import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implementar ouvintes de eventos aqui
    },
    baseUrl: 'http://localhost:5173', // altere para a URL do seu projeto
    supportFile: false,
  },
});
