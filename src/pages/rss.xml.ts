import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import getSortedPosts from "@/utils/getSortedPosts";
import { SITE } from "@/config";

export async function GET() {
  const posts = getSortedPosts(await getCollection("blog"));
  return rss({
    title: SITE.title,
    description: SITE.desc,
    site: SITE.website,
    items: posts.map(({ data }) => ({
      link: data.link,
      title: data.title,
      description: data.koreanSummary ?? data.title,
      pubDate: new Date(data.pubDatetime),
    })),
  });
}
