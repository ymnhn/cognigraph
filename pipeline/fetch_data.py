import os
import re
import json
import time
import urllib.request
import urllib.parse
import urllib.error
import feedparser
from datetime import datetime, timezone
from sentence_transformers import SentenceTransformer, util

# ── Configuration ─────────────────────────────────────────────────────────────

SEARCH_QUERY = (
    'all:"cognitive science" OR all:"neural manifolds" OR all:"active inference"'
)
FETCH_POOL_SIZE = 50   # papers pulled from arXiv per run
TARGET_SAVED    = 5    # new papers to save per run
MODEL_NAME      = "all-MiniLM-L6-v2"
OUTPUT_DIR      = "src/data/blog"

TARGET_CONCEPT = (
    "Cognitive science research involving neural representations, "
    "computational modeling, active inference, and brain functions."
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_ENABLED = bool(GEMINI_API_KEY)

# ── Gemini ────────────────────────────────────────────────────────────────────

def _gemini_post(payload: dict) -> dict:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash-lite:generateContent?key={GEMINI_API_KEY}"
    )
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())
        except Exception as e:
            print(f"  [Gemini] attempt {attempt + 1} failed: {e}")
            # Free tier resets every 60s. Sleep 65s to guarantee a new window.
            time.sleep(65)
    return {}


def generate_metadata_batch(papers: list[dict]) -> list[dict]:
    """
    Single Gemini call for all winners at once.
    5 papers = 1 API call, well within the 15 RPM free tier.
    """
    fallback = [{"tags": ["cognitive-science"], "korean_summary": ""} for _ in papers]
    if not GEMINI_ENABLED:
        print("  [Gemini] GEMINI_API_KEY not set — skipping metadata.")
        return fallback

    numbered = "\n\n".join(
        f"[{i+1}] Title: {p['title']}\nAbstract: {p['abstract'][:800]}"
        for i, p in enumerate(papers)
    )
    prompt = (
        f"Analyze the following {len(papers)} papers and return ONLY a JSON array. "
        "No markdown, no explanation, nothing else. "
        "Array order must match paper number order.\n\n"
        f"{numbered}\n\n"
        "Return format:\n"
        "[\n"
        '  {"tags": ["lowercase-english-tag1", "tag2", "tag3"], '
        '"korean_summary": "2~3 sentence Korean summary of the paper"},\n'
        "  ...\n"
        "]"
    )

    print(f"  [Gemini] batch request for {len(papers)} paper(s)...")
    result = _gemini_post({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 2048, "temperature": 0.2},
    })

    raw = ""
    try:
        raw = (
            result.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
        )
        if not raw:
            print("  [Gemini] empty response — papers will be saved without summaries")
            return fallback
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()
        parsed = json.loads(raw)
        results = []
        for item in parsed:
            tags = [str(t).lower().replace(" ", "-") for t in item.get("tags", [])][:5]
            summary = str(item.get("korean_summary", "")).strip()
            results.append({"tags": tags or ["cognitive-science"], "korean_summary": summary})
        while len(results) < len(papers):
            results.append({"tags": ["cognitive-science"], "korean_summary": ""})
        print(f"  [Gemini] done: {len(results)} paper(s) processed")
        return results
    except Exception as e:
        print(f"  [Gemini] parse error: {e}  raw={raw[:200]!r}")
        return fallback

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

def tags_yaml(tags: list[str]) -> str:
    return "[" + ", ".join(f'"{t}"' for t in tags) + "]"

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Phase 1: load model + fetch arXiv
    print(f"Loading semantic model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)
    target_emb = model.encode(TARGET_CONCEPT, convert_to_tensor=True)

    entries = fetch_arxiv(max_results=FETCH_POOL_SIZE)
    if not entries:
        print("No entries returned from arXiv.")
        return

    # Phase 2: batch-score all papers in one tensor op
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

    # Pick top-scoring papers not already saved
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

    # Phase 3: one batch Gemini call for all winners
    papers_for_gemini = [
        {"title": w["title"], "abstract": w["summary"]} for w in winners
    ]
    meta_list = generate_metadata_batch(papers_for_gemini)

    # Phase 4: write files
    saved = 0
    for entry, meta in zip(winners, meta_list):
        title    = entry["title"]
        score    = entry["score"]
        summary  = meta["korean_summary"]
        new_tags = tags_yaml(meta["tags"])
        korean_line = f'koreanSummary: "{esc(summary)}"\n' if summary else ""

        content = (
            f'---\n'
            f'author: "CogniGraph Bot"\n'
            f'pubDatetime: {entry["pub_date"]}\n'
            f'title: "{esc(title)}"\n'
            f'featured: false\n'
            f'draft: false\n'
            f'tags: {new_tags}\n'
            f'description: "[arXiv]({entry["link"]}) — relevance score: {score:.2f}"\n'
            f'{korean_line}'
            f'---\n\n'
            f'## Abstract\n\n'
            f'{entry["summary"][:2000]}\n\n'
            f'---\n\n'
            f'*Relevance score: {score:.4f}*\n'
        )

        with open(entry["fpath"], "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Saved [{score:.2f}]: {title[:65]}")
        saved += 1

    print(f"\nDone. {saved} new paper(s) saved.")


if __name__ == "__main__":
    main()
