import { defineConfig } from "vite";

export default defineConfig({
  server: {
    port: 5173,
    host: "0.0.0.0", // सभी नेटवर्क से एक्सेस की अनुमति  
    strictPort: true,
    cors: true,
    allowedHosts: [
      "localhost",
      "fe118761-bd62-46a8-8b9e-5174d9779133-00-3444qikyspnsi.sisko.replit.dev"
    ]
  }
});
