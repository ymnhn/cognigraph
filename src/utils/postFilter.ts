import type { CollectionEntry } from "astro:content";

const postFilter = ({ data }: CollectionEntry<"blog">) =>
  import.meta.env.DEV || new Date(data.pubDatetime) <= new Date();

export default postFilter;
