import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const API_HOST = process.env.API_HOST || "api";

// El proxy corre *dentro* del contenedor de Vite, que sí está en la red Docker.
// Por eso puede resolver untdf-api. El navegador de tu máquina no.
export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      "/api": {
        target: `http://${API_HOST}:8000`,
        changeOrigin: true,
      },
    },
  },
});
