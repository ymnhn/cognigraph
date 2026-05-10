import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://ymnhn.github.io",
  base: "/cognigraph",
  integrations: [sitemap()],
  vite: { plugins: [tailwindcss()] },
});
