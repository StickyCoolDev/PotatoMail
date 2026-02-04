import { defineConfig } from 'vite'
import preact from '@preact/preset-vite'
import tanstackRouter from '@tanstack/router-plugin/vite'
// https://vite.dev/config/
export default defineConfig({
  plugins: [preact(), tanstackRouter()],
  resolve: {
    alias: {
      'react': 'preact/compat',
      'react-dom': 'preact/compat',
      'react-dom/test-utils': 'preact/compat/test-utils',
      'react/jsx-runtime': 'preact/jsx-runtime',
    },
  },
})
