import { defineConfig } from "vite";

export default defineConfig({
  server: {
    port: 5173,
    host: "0.0.0.0", // External access allow करने के लिए
    strictPort: true, 
    allowedHosts: "all" // सभी होस्ट को अलाउ करने के लिए
  }
});
