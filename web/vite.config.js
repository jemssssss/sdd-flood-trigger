import { defineConfig } from 'vite'
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import babel from '@rolldown/plugin-babel'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    babel({ presets: [reactCompilerPreset()] })
  ],
  base: '/sdd-flood-trigger/',
  server: { 
    proxy: { 
      "/ecmwf": { 
        target: "http://127.0.0.1:8000", 
        changeOrigin: true, 
      }, 
      "/health": { 
        target: "http://127.0.0.1:8000", 
        changeOrigin: true, 
      }, 
    }, 
  },
})
