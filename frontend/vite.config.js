// /frontend/vite.config.js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 8000, // Set the port to 8000
    proxy: {
      '/upload': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    },
  },
  cache: false,
});
