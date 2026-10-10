import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/todos": "http://127.0.0.1:8000",
      "/auth": "http://127.0.0.1:8000",
      "/suggestions": "http://127.0.0.1:8000",
      "/study": "http://127.0.0.1:8000",
      "/health": "http://127.0.0.1:8000",
    },
  },
});
