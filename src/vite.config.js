import { defineConfig } from "vite";

export default defineConfig({
  server: {
    port: 5173,
    host: "0.0.0.0", // External access allow करने के लिए
    strictPort: true, 
    allowedHosts: [
      "fe118761-bd62-46a8-8b9e-5174d9779133-00-3444qikyspnsi.sisko.replit.dev", // Replit का होस्ट जोड़ें
      "localhost"
    ]
  }
});
