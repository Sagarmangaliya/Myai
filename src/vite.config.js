import { defineConfig } from "vite";

export default defineConfig({
  server: {
    port: 5173,
    host: "0.0.0.0", // सभी नेटवर्क से एक्सेस की अनुमति  
    strictPort: true,
    allowedHosts: "all" // सभी होस्ट को अलाउ करने के लिए  
  }
});

