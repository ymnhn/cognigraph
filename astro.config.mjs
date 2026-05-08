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
      PUBLIC_GOOGLE_SITE_VERIFICATION: envField.string({
        context: 'client',
        access: 'public',
        optional: true, // 값이 없어도 빌드가 실패하지 않도록 설정
      }),
    },
  },
});
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