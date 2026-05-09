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
FETCH_POOL_SIZE = 50     
TARGET_SAVED_COUNT = 15  
MODEL_NAME = "all-MiniLM-L6-v2"

# Output directory set to src/data/blog
OUTPUT_DIR = "src/data/blog"

TARGET_CONCEPT = (
    "Cognitive science research involving neural representations, "
    "computational modeling, active inference, and brain functions."
)

def fetch_arxiv_papers(max_results=50):
    base_url = "http://export.arxiv.org/api/query?"
    params = {
        "search_query": SEARCH_QUERY,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = base_url + urllib.parse.urlencode(params)
    print(f"Fetching {max_results} candidate papers from arXiv...")

    for attempt in range(3):
        try:
            response = urllib.request.urlopen(url, timeout=30)
            return response.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 20 * (attempt + 1)
                time.sleep(wait)
            else:
                raise
    raise Exception("arXiv API unreachable.")

def sanitize_filename(title: str, max_length: int = 50) -> str:
    clean = "".join(c if c.isalnum() or c == " " else "" for c in title).strip()
    slug = clean.replace(" ", "-").lower()
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:max_length].rstrip("-")

def format_astro_date(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")

def escape_yaml(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')

def main():
    print(f"Loading model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)
    target_embedding = model.encode(TARGET_CONCEPT, convert_to_tensor=True)

    try:
        xml_data = fetch_arxiv_papers(max_results=FETCH_POOL_SIZE)
        feed = feedparser.parse(xml_data)
    except Exception as e:
        print(f"Error: {e}")
        return

    entries = feed.get("entries", [])
    scored_entries = []

    for entry in entries:
        title = entry.get("title", "").strip().replace("\n", " ")
        summary = entry.get("summary", "").strip().replace("\n", " ")
        if not title or not summary: continue

        text_to_score = f"{title}. {summary}"
        entry_embedding = model.encode(text_to_score, convert_to_tensor=True)
        score = util.pytorch_cos_sim(target_embedding, entry_embedding).item()
        
        scored_entries.append({"score": score, "entry": entry, "title": title, "summary": summary})

    scored_entries.sort(key=lambda x: x["score"], reverse=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    saved_count = 0
    for item in scored_entries:
        if saved_count >= TARGET_SAVED_COUNT: break

        entry, score, title, summary = item["entry"], item["score"], item["title"], item["summary"]
        slug = sanitize_filename(title)
        filepath = os.path.join(OUTPUT_DIR, f"{slug}.md")

        if os.path.exists(filepath): continue

        try:
            pub_date = format_astro_date(entry.get("published", ""))
        except: continue

        content = f"""---
author: "CogniGraph Bot"
pubDatetime: {pub_date}
title: "{escape_yaml(title)}"
featured: false
draft: false
tags: ["research", "cognitive-science"]
description: "[arXiv]({entry.get('link', '')}) — relevance score: {score:.2f}"
---

## Abstract

{summary[:2000]}

---

*Relevance score: {score:.4f}*
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        saved_count += 1
        print(f"Saved: {title}")

if __name__ == "__main__":
    main()
