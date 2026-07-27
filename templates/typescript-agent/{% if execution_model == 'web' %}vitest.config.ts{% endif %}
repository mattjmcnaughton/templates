import react from "@vitejs/plugin-react";
import { resolve } from "node:path";
// `defineConfig` comes from vitest, not vite: the `test` block below is not part
// of vite's own UserConfig and `tsc` rejects it when imported from "vite".
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { "@": resolve(import.meta.dirname, "./src") },
  },
  test: {
    environment: "jsdom",
    setupFiles: "./tests/setup.ts",
    include: ["tests/unit/**/*.test.{ts,tsx}", "tests/integration/**/*.test.{ts,tsx}"],
  },
});
