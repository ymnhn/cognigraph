import os
import re
import time
import urllib.request
import urllib.parse
import urllib.error
import feedparser
from datetime import datetime, timezone
from sentence_transformers import SentenceTransformer, util
from googletrans import Translator

# ── Configuration ─────────────────────────────────────────────────────────────

SEARCH_QUERY = (
    'all:"cognitive science" OR all:"neural manifolds" OR all:"active inference"'
)
FETCH_POOL_SIZE = 50
TARGET_SAVED    = 5
MODEL_NAME      = "all-MiniLM-L6-v2"
OUTPUT_DIR      = "src/data/blog"

TARGET_CONCEPT = (
    "Cognitive science research involving neural representations, "
    "computational modeling, active inference, and brain functions."
)

# ── Translation ───────────────────────────────────────────────────────────────

def make_korean_summary(abstract: str) -> str:
    """
    Translate the first ~3 sentences of the abstract to Korean using
    Google Translate (no API key, no rate limit quota).
    """
    # Take first 3 sentences (up to 600 chars) as the source for summary
    sentences = re.split(r'(?<=[.!?])\s+', abstract.strip())
    snippet = " ".join(sentences[:3])[:600]

    translator = Translator()
    for attempt in range(3):
        try:
            result = translator.translate(snippet, src="en", dest="ko")
            return result.text.strip()
        except Exception as e:
            print(f"  [Translate] attempt {attempt + 1} failed: {e}")
            time.sleep(3)
    print("  [Translate] all attempts failed — saving without Korean summary")
    return ""

# ── arXiv ─────────────────────────────────────────────────────────────────────

def fetch_arxiv(max_results: int = 50) -> list[dict]:
    params = {
        "search_query": SEARCH_QUERY,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    print(f"Fetching {max_results} papers from arXiv...")

    for attempt in range(3):
        try:
            response = urllib.request.urlopen(url, timeout=30)
            feed = feedparser.parse(response.read())
            entries = []
            for e in feed.get("entries", []):
                title   = e.get("title", "").strip().replace("\n", " ")
                summary = e.get("summary", "").strip().replace("\n", " ")
                if title and summary:
                    entries.append({
                        "title":     title,
                        "summary":   summary,
                        "link":      e.get("link", ""),
                        "published": e.get("published", ""),
                    })
            return entries
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 20 * (attempt + 1)
                print(f"  Rate limited. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise Exception("arXiv API unreachable after 3 attempts.")

# ── Helpers ───────────────────────────────────────────────────────────────────

def slugify(title: str, max_length: int = 50) -> str:
    clean = "".join(c if c.isalnum() or c == " " else "" for c in title).strip()
    slug  = clean.replace(" ", "-").lower()
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:max_length].rstrip("-")

def astro_date(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")

def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Loading semantic model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)
    target_emb = model.encode(TARGET_CONCEPT, convert_to_tensor=True)

    entries = fetch_arxiv(max_results=FETCH_POOL_SIZE)
    if not entries:
        print("No entries returned from arXiv.")
        return

    print(f"Batch-scoring {len(entries)} papers...")
    texts = [f"{e['title']}. {e['summary']}" for e in entries]
    embeddings = model.encode(
        texts, convert_to_tensor=True, batch_size=32, show_progress_bar=False
    )
    scores = util.pytorch_cos_sim(target_emb, embeddings)[0].tolist()
    for entry, score in zip(entries, scores):
        entry["score"] = score
    entries.sort(key=lambda x: x["score"], reverse=True)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    winners = []
    for entry in entries:
        if len(winners) >= TARGET_SAVED:
            break
        slug = slugify(entry["title"])
        if not slug:
            continue
        fpath = os.path.join(OUTPUT_DIR, f"{slug}.md")
        if os.path.exists(fpath):
            continue
        try:
            entry["pub_date"] = astro_date(entry["published"])
        except ValueError:
            continue
        entry["slug"]  = slug
        entry["fpath"] = fpath
        winners.append(entry)

    print(f"Scoring done. {len(winners)} new paper(s) to save.")
    if not winners:
        print("Nothing new to save today.")
        return

    saved = 0
    for entry in winners:
        title   = entry["title"]
        score   = entry["score"]
        abstract = entry["summary"]

        print(f"  [{score:.2f}] {title[:65]}")
        print(f"    Translating summary...")
        korean_summary = make_korean_summary(abstract)
        korean_line = f'koreanSummary: "{esc(korean_summary)}"\n' if korean_summary else ""

        content = (
            f'---\n'
            f'author: "CogniGraph Bot"\n'
            f'pubDatetime: {entry["pub_date"]}\n'
            f'title: "{esc(title)}"\n'
            f'featured: false\n'
            f'draft: false\n'
            f'tags: ["cognitive-science"]\n'
            f'description: "[arXiv]({entry["link"]}) — relevance score: {score:.2f}"\n'
            f'{korean_line}'
            f'---\n\n'
            f'## Abstract\n\n'
            f'{abstract[:2000]}\n\n'
            f'---\n\n'
            f'*Relevance score: {score:.4f}*\n'
        )

        with open(entry["fpath"], "w", encoding="utf-8") as f:
            f.write(content)
        print(f"    Saved.")
        saved += 1

    print(f"\nDone. {saved} new paper(s) saved.")


if __name__ == "__main__":
    main()
