import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import sitemap from "@astrojs/sitemap";
import remarkToc from "remark-toc";
import remarkCollapse from "remark-collapse";
import { SITE } from "./src/config";

export default defineConfig({
  // site must be the root origin only; base carries the subdirectory.
  // Without base, Astro builds all hrefs as /posts, /search, etc. which 404
  // under the GitHub Pages subdirectory https://ymnhn.github.io/cognigraph/.
  site: "https://ymnhn.github.io",
  base: "/cognigraph",
  integrations: [
    sitemap({
      filter: page => SITE.showArchives || !page.endsWith("/archives"),
    }),
  ],
  markdown: {
    remarkPlugins: [remarkToc, [remarkCollapse, { test: "Table of contents" }]],
    shikiConfig: {
      // Dual light/dark themes so --shiki-light-bg and --shiki-dark-bg variables are available
      themes: { light: "github-light", dark: "one-dark-pro" },
      defaultColor: false,
      wrap: true,
    },
  },
  vite: {
    plugins: [tailwindcss()],
    optimizeDeps: {
      exclude: ["@resvg/resvg-js"],
    },
  },
});