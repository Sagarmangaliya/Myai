import { defineConfig } from "vite";

export default defineConfig({
  server: {
    port: 5173,
    host: "0.0.0.0",
    strictPort: true,
    cors: true,  // CORS इनेबल करें
    hmr: {
      clientPort: 443, // Replit पर HMR के लिए सही पोर्ट सेट करें
    }
  }
});
