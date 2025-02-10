import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implementar ouvintes de eventos aqui
    },
    baseUrl: "http://localhost:5174", // altere para a URL do seu projeto
    supportFile: "cypress/support/e2e.js",
    specPattern: "cypress/e2e/**/*.{js,jsx,ts,tsx}",
  },

  component: {
    devServer: {
      framework: "react",
      bundler: "vite",
    },
  },
});
