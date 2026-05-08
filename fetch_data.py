import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# Import your settings
import config

def fetch_arxiv_papers():
    """Fetches recent papers from the arXiv API."""
    print(f"Fetching top {config.MAX_RESULTS} papers from arXiv...")
    
    # Format the query for the URL
    query = urllib.parse.quote(config.SEARCH_QUERY)
    url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results={config.MAX_RESULTS}&sortBy=submittedDate&sortOrder=descending"
    
    response = urllib.request.urlopen(url)
    xml_data = response.read()
    root = ET.fromstring(xml_data)
    
    papers = []
    # arXiv XML namespace
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    for entry in root.findall('atom:entry', ns):
        paper = {
            'id': entry.find('atom:id', ns).text.split('/')[-1],
            'title': entry.find('atom:title', ns).text.replace('\n', ' ').strip(),
            'abstract': entry.find('atom:summary', ns).text.replace('\n', ' ').strip(),
            'date': entry.find('atom:published', ns).text
        }
        papers.append(paper)
        
    return papers

def clean_filename(title):
    """Makes a string safe to use as a file name."""
    clean = re.sub(r'[^\w\s-]', '', title).strip().lower()
    return re.sub(r'\s+', '-', clean)[:50] # Limit length

def save_to_markdown(paper, score):
    """Saves a paper as an AstroPaper-compatible Markdown file."""
    # Ensure the output directory exists
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    filename = f"{clean_filename(paper['title'])}.md"
    filepath = os.path.join(config.OUTPUT_DIR, filename)
    
    # Format the date for AstroPaper (ISO format)
    pub_date = datetime.strptime(paper['date'], "%Y-%m-%dT%H:%M:%SZ")
    
    # AstroPaper Frontmatter
    content = f"""---
author: "CogniGraph Bot"
pubDatetime: {pub_date.isoformat()}
title: "{paper['title']}"
postSlug: "{clean_filename(paper['title'])}"
featured: false
draft: false
tags:
  - "research"
  - "cognitive science"
description: "Semantic Match: {score:.2f} | ArXiv ID: {paper['id']}"
---

### Abstract
{paper['abstract']}

---
**Source:** [Read Full Paper on arXiv](https://arxiv.org/abs/{paper['id']})
*Curated via Semantic Scoring (Threshold: {config.SIMILARITY_THRESHOLD})*
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved: {filename} (Score: {score:.2f})")

def main():
    print("Initializing Semantic Gatekeeper...")
    # Load the AI model
    model = SentenceTransformer(config.MODEL_NAME)
    target_embedding = model.encode(config.TARGET_CONCEPT, convert_to_tensor=True)
    
    # Get raw data
    raw_papers = fetch_arxiv_papers()
    
    curated_count = 0
    print("\nScoring Papers...")
    
    for paper in raw_papers:
        # Calculate semantic similarity
        abstract_embedding = model.encode(paper['abstract'], convert_to_tensor=True)
        score = util.cos_sim(target_embedding, abstract_embedding).item()
        
        # Filter based on your config threshold
        if score >= config.SIMILARITY_THRESHOLD:
            save_to_markdown(paper, score)
            curated_count += 1
            
    print(f"\nPipeline Complete! Curated {curated_count} out of {len(raw_papers)} papers.")

if __name__ == "__main__":
    main()