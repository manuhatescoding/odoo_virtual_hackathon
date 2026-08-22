import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  publicDir: false,
  server: {
    host: process.env.VITE_HOST || '127.0.0.1',
    port: Number(process.env.VITE_PORT || 5173),
    proxy: {
      '/api': process.env.VITE_API_URL || 'http://127.0.0.1:8000',
      '/ws': { target: process.env.VITE_API_URL || 'http://127.0.0.1:8000', ws: true },
    },
  },
  test: {
    environment: 'jsdom',
  },
});
