import { defineConfig, envField } from "astro/config"; // envField 추가
import tailwind from "@astrojs/tailwind";
import react from "@astrojs/react";
import remarkToc from "remark-toc";
import remarkCollapse from "remark-collapse";
import sitemap from "@astrojs/sitemap";
import mdx from "@astrojs/mdx";
import path from "path";

export default defineConfig({
  site: "https://ymnhn.github.io",
  base: "/cognigraph",
  
  // astro:env 모듈 에러 해결을 위한 스마 정의
  experimental: {
    env: {
      schema: {
        // 실제 Layout 등에서 환경변수를 쓰지 않더라도 
        // 빈 스키마나 기본값을 정의해야 모듈이 생성됩니다.
      },
    },
  },

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
      [remarkCollapse, { test: "Table of contents" }],
    ],
    shikiConfig: {
      theme: "one-dark-pro",
      wrap: true,
    },
  },

  vite: {
    resolve: {
      alias: {
        "@": path.resolve("./src"),
      },
    },
    optimizeDeps: {
      exclude: ["@resvg/resvg-js"],
    },
  },
});