import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    rollupOptions: {
      external: [
        'vuetify/styles',
        '@mdi/font/css/materialdesignicons.css',
        'vuetify',
        'vuetify/iconsets/mdi',
        'vuetify/components',
      ],
    },
  },
});
