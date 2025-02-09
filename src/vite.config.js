import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    host: "0.0.0.0", // सभी नेटवर्क से एक्सेस के लिए
    strictPort: true, 
    port: 5173, // आप इसे कोई भी पोर्ट दे सकते हैं
    allowedHosts: "all", // यह सबसे जरूरी है!
  }
});
