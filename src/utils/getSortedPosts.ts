import type { CollectionEntry } from "astro:content";

const getSortedPosts = (posts: CollectionEntry<"blog">[]) =>
  posts
    .filter(({ data }) => import.meta.env.DEV || new Date(data.pubDatetime) <= new Date())
    .sort((a, b) => new Date(b.data.pubDatetime).getTime() - new Date(a.data.pubDatetime).getTime());

export default getSortedPosts;
