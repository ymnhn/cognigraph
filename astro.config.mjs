import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";
import react from "@astrojs/react";
import remarkToc from "remark-toc";
import remarkCollapse from "remark-collapse";
import sitemap from "@astrojs/sitemap";
import mdx from "@astrojs/mdx";
import path from "path"; // 경로 설정을 위해 추가

// https://astro.build/config
export default defineConfig({
  // IMPORTANT: Replace with your actual GitHub Pages URL
  site: "https://ymnhn.github.io",
  
  // IMPORTANT: If your repo is named 'cognigraph', uncomment the line below.
  base: "/cognigraph",

  integrations: [
    tailwind({
      applyBaseStyles: false,
    }),
    react(),
    sitemap(),
    mdx(),
  ],
  markdown: {
    remarkPlugins: [
      remarkToc,
      [
        remarkCollapse,
        {
          test: "Table of contents",
        },
      ],
    ],
    shikiConfig: {
      theme: "one-dark-pro",
      wrap: true,
    },
  },
  vite: {
    resolve: {
      alias: {
        "@": path.resolve("./src"), // @ 기호를 src 폴더 절대 경로로 연결
      },
    },
    optimizeDeps: {
      exclude: ["@resvg/resvg-js"],
    },
  },
  scopedStyleStrategy: "where",
});