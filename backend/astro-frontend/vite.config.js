import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,
    cors: true,
    allowedHosts: ["astro.doctoral.fr"],  // 🔥 Ajoute ceci pour autoriser le domaine
    proxy: {
      "/api": {
        target: "http://192.168.1.188:8100",
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
