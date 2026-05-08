import os
import time
import urllib.request
import urllib.parse
import urllib.error
import feedparser
from datetime import datetime, timezone
from sentence_transformers import SentenceTransformer, util

# --- CONFIGURATION ---
SEARCH_QUERY = 'all:"cognitive science" OR all:"neural manifolds" OR all:"active inference"'
MAX_RESULTS = 15
THRESHOLD = 0.25
MODEL_NAME = "all-MiniLM-L6-v2"

# Must match BLOG_PATH in src/content.config.ts
OUTPUT_DIR = "src/data/blog"

TARGET_CONCEPT = (
    "Cognitive science research involving neural representations, "
    "computational modeling, active inference, and brain functions."
)


def fetch_arxiv_papers():
    """Fetch papers from arXiv with proper URL encoding and retry logic."""
    base_url = "http://export.arxiv.org/api/query?"
    params = {
        "search_query": SEARCH_QUERY,
        "start": 0,
        "max_results": MAX_RESULTS,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = base_url + urllib.parse.urlencode(params)
    print(f"Fetching papers from arXiv...")

    for attempt in range(3):
        try:
            response = urllib.request.urlopen(url, timeout=30)
            return response.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 20 * (attempt + 1)
                print(f"Rate limited (429). Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise Exception("arXiv API unreachable after 3 attempts.")


def sanitize_filename(title: str, max_length: int = 50) -> str:
    """Convert a paper title into a safe slug-style filename."""
    clean = "".join(c if c.isalnum() or c == " " else "" for c in title).strip()
    slug = clean.replace(" ", "-").lower()
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:max_length].rstrip("-")


def format_astro_date(date_str: str) -> str:
    """Parse arXiv date string and return ISO 8601 format accepted by Astro z.date()."""
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def escape_yaml(s: str) -> str:
    """Escape a string for use inside YAML double-quotes."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def main():
    print(f"Loading model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)
    target_embedding = model.encode(TARGET_CONCEPT, convert_to_tensor=True)

    try:
        xml_data = fetch_arxiv_papers()
        feed = feedparser.parse(xml_data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    entries = feed.get("entries", [])
    print(f"Received {len(entries)} entries from arXiv.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    count = 0
    for entry in entries:
        title = entry.get("title", "").strip().replace("\n", " ")
        summary = entry.get("summary", "").strip().replace("\n", " ")
        link = entry.get("link", "")
        published = entry.get("published", "")

        if not title or not published:
            continue

        # Semantic scoring
        text_to_score = f"{title}. {summary}"
        entry_embedding = model.encode(text_to_score, convert_to_tensor=True)
        score = util.pytorch_cos_sim(target_embedding, entry_embedding).item()

        if score < THRESHOLD:
            continue

        slug = sanitize_filename(title)
        if not slug:
            continue

        filepath = os.path.join(OUTPUT_DIR, f"{slug}.md")
        if os.path.exists(filepath):
            print(f"Skipping (already exists): {title}")
            continue

        try:
            pub_date = format_astro_date(published)
        except ValueError:
            print(f"Skipping (bad date '{published}'): {title}")
            continue

        # Description uses only Zod-schema-compliant fields
        description = f"[arXiv]({link}) — relevance score: {score:.2f}"
        body_summary = summary[:2000] + ("..." if len(summary) > 2000 else "")

        content = f"""---
author: "CogniGraph Bot"
pubDatetime: {pub_date}
title: "{escape_yaml(title)}"
featured: false
draft: false
tags: ["research", "cognitive-science"]
description: "{escape_yaml(description)}"
---

## Abstract

{body_summary}

---

*Automatically curated based on semantic similarity to core Cognitive Science themes.*
*Relevance score: {score:.4f}*
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Saved [{score:.2f}]: {title}")
        count += 1

    print(f"\nPipeline complete. {count} new paper(s) saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
