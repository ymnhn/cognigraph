import { defineCollection, z } from "astro:content";

const blog = defineCollection({
  type: "content",
  schema: z.object({
    author: z.string().default("CogniGraph Bot"),
    pubDatetime: z.date(),
    title: z.string(),
    postSlug: z.string().optional(),
    featured: z.boolean().optional(),
    draft: z.boolean().optional(),
    tags: z.array(z.string()).default(["research"]),
    description: z.string(),
    canonicalURL: z.string().optional(),
  }),
});

export const collections = { blog };
