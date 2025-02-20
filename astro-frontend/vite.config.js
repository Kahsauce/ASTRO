import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",     // Écoute sur toutes les interfaces
    port: 5173,         // Port utilisé par Vite
    strictPort: true,   // Empêche le changement automatique de port
    hmr: {
      clientPort: 443,  // Corrige l'accès HTTPS via Cloudflare
    },
    allowedHosts: ["astro.doctoral.fr", "192.168.1.188"], // Autorise Cloudflare & IP locale

    // 💡 Pas de "rewrite", pour conserver "/api" intact
    proxy: {
      "/api": {
        target: "http://192.168.1.188:8100", // FastAPI
        changeOrigin: true,
        secure: false,
        ws: true,   // Autorise WebSocket, utile si tu en as besoin
        // ❌ Retirer la partie rewrite
        // rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
