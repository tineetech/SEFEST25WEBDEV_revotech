import { defineConfig } from 'vite'
// import tailwindcss from '@tailwindcss/vite'
import tailwindcss from "tailwindcss";
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    tailwindcss(),
    react()
  ],
  server: {
    // allowedHosts: ["e114-114-10-76-31.ngrok-free.app"], 
  },
})
