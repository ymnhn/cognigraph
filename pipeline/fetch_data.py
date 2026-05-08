import os
import time
import urllib.request
import feedparser
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# --- CONFIGURATION ---
# The 'Cognitive Science' focus for your college project
SEARCH_QUERY = 'all:"cognitive science" OR all:"neural manifolds" OR all:"active inference"'
MAX_RESULTS = 10
# Similarity threshold (0.0 to 1.0)
THRESHOLD = 0.5 
MODEL_NAME = 'all-MiniLM-L6-v2'

def fetch_arxiv_papers():
    """Fetches papers from ArXiv with basic retry logic for 429 errors."""
    base_url = "http://export.arxiv.org/api/query?"
    params = f"search_query={SEARCH_QUERY}&start=0&max_results={MAX_RESULTS}&sortBy=submittedDate&sortOrder=descending"
    url = base_url + params
    
    print(f"Fetching papers from arXiv...")
    for attempt in range(3):
        try:
            response = urllib.request.urlopen(url)
            return response.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 15 * (attempt + 1)
                print(f"Rate limited (429). Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise e
    raise Exception("ArXiv API unreachable after multiple attempts.")

def main():
    # 1. Initialize the Semantic Gatekeeper
    print(f"Initializing Semantic Gatekeeper with {MODEL_NAME}...")
    # HF_TOKEN env var is used automatically by the library if present
    model = SentenceTransformer(MODEL_NAME)
    
    # Define your "Ideal" research topic for scoring
    target_concept = "Applications of cognitive science, neural representations, and computational modeling of brain functions."
    target_embedding = model.encode(target_concept, convert_to_tensor=True)

    # 2. Get Data
    xml_data = fetch_arxiv_papers()
    feed = feedparser.parse(xml_data)
    
    # Ensure output directory exists
    os.makedirs("src/content/blog", exist_ok=True)

    count = 0
    for entry in feed.entries:
        # 3. Semantic Scoring
        text_to_score = f"{entry.title}. {entry.summary}"
        entry_embedding = model.encode(text_to_score, convert_to_tensor=True)
        score = util.pytorch_cos_sim(target_embedding, entry_embedding).item()

        if score >= THRESHOLD:
            # 4. Generate Frontmatter
            # Clean title for filename
            clean_title = "".join(c for c in entry.title if c.isalnum() or c==' ').rstrip()
            filename = f"src/content/blog/{clean_title.replace(' ', '-').lower()[:50]}.md"
            
            # Format date for Astro
            pub_date = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%SZ')
            
            content = f"""---
author: "CogniGraph Bot"
pubDatetime: {pub_date.strftime('%Y-%m-%dT%H:%M:%SZ')}
title: "{entry.title}"
postSlug: "{clean_title.replace(' ', '-').lower()[:50]}"
featured: false
draft: false
tags: ["research", "cognitive-science"]
description: "Semantic Relevance Score: {score:.4f}"
score: {score:.4f}
sourceUrl: "{entry.link}"
---

## Abstract
{entry.summary}

---
*This paper was automatically curated based on semantic similarity to core Cognitive Science themes.*
"""
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"Saved: {entry.title} (Score: {score:.2f})")
            count += 1

    print(f"Pipeline complete. {count} papers curated.")

if __name__ == "__main__":
    main()
