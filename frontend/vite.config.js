import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
  define: {
    __API_URL__: JSON.stringify(
      process.env.NODE_ENV === "production"
        ? "https://world-cup-predictor-y3bc.onrender.com"
        : "http://localhost:8000"
    ),
  },
});