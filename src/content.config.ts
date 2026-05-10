import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const blog = defineCollection({
  loader: glob({ pattern: "**/[^_]*.md", base: "./src/data/blog" }),
  schema: z.object({
    pubDatetime: z.date(),
    title: z.string(),
    link: z.string().url(),
    koreanSummary: z.string().optional(),
  }),
});

export const collections = { blog };
