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
FETCH_POOL_SIZE   = 50   # papers pulled from arXiv per run
TARGET_SAVED      = 15   # max new papers saved per run
BACKFILL_PER_RUN  = 5    # existing posts to backfill per run (keeps CI fast)
MODEL_NAME        = "all-MiniLM-L6-v2"
OUTPUT_DIR        = "src/data/blog"   # must match BLOG_PATH in content.config.ts

TARGET_CONCEPT = (
    "Cognitive science research involving neural representations, "
    "computational modeling, active inference, and brain functions."
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_ENABLED = bool(GEMINI_API_KEY)

# ── Gemini ────────────────────────────────────────────────────────────────────

def _gemini_post(payload: dict) -> dict:
    """Raw POST to Gemini 1.5-flash. Returns parsed JSON response."""
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
            with urllib.request.urlopen(req, timeout=25) as resp:
                return json.loads(resp.read())
        except Exception as e:
            print(f"    [Gemini] attempt {attempt + 1} failed: {e}")
            time.sleep(5 * (attempt + 1))
    return {}

def generate_metadata(title: str, abstract: str) -> dict:
    """
    Single Gemini call that returns BOTH tags and Korean summary.
    Calling once per paper (not twice) halves API usage.
    """
    if not GEMINI_ENABLED:
        return {"tags": ["cognitive-science"], "korean_summary": ""}

    prompt = (
        "다음 논문을 분석하여 아래 JSON만 반환하세요. 다른 텍스트는 절대 포함하지 마세요.\n\n"
        f"제목: {title}\n"
        f"초록: {abstract[:1500]}\n\n"
        "{\n"
        '  "tags": ["소문자 영어 태그 3~5개"],\n'
        '  "korean_summary": "핵심 내용을 한국어로 2~3문장 요약"\n'
        "}"
    )
    result = _gemini_post({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 300, "temperature": 0.2},
    })

    try:
        raw = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
        if not raw:
            print("    [Gemini] empty response")
            return {"tags": ["cognitive-science"], "korean_summary": ""}
        # Strip markdown code fences if model wraps the JSON
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()
        parsed = json.loads(raw)
        tags = [str(t).lower().replace(" ", "-") for t in parsed.get("tags", [])][:5]
        summary = str(parsed.get("korean_summary", "")).strip()
        return {"tags": tags or ["cognitive-science"], "korean_summary": summary}
    except Exception as e:
        print(f"    [Gemini] parse error: {e}  raw={raw[:120]!r}")
        return {"tags": ["cognitive-science"], "korean_summary": ""}

# ── arXiv ─────────────────────────────────────────────────────────────────────

def fetch_arxiv(max_results: int = 50) -> list[dict]:
    """Fetch papers from arXiv and return a flat list of dicts."""
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

# ── Backfill ──────────────────────────────────────────────────────────────────

def backfill(model, target_emb):
    """
    Add koreanSummary + dynamic tags to existing posts that still have the
    old hardcoded tags or no Korean summary.
    Capped at BACKFILL_PER_RUN per CI run to keep runtime short.
    """
    if not GEMINI_ENABLED:
        print("Backfill skipped — GEMINI_API_KEY not set.")
        return

    candidates = []
    for fname in os.listdir(OUTPUT_DIR):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(OUTPUT_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        needs_work = (
            "koreanSummary:" not in content
            or 'tags: ["research", "cognitive-science"]' in content
        )
        if needs_work:
            candidates.append((fpath, content))

    if not candidates:
        print("Backfill: all posts are up to date.")
        return

    print(f"Backfill: {len(candidates)} post(s) need updating, "
          f"processing up to {BACKFILL_PER_RUN} this run...")

    done = 0
    for fpath, content in candidates:
        if done >= BACKFILL_PER_RUN:
            break

        tm = re.search(r'^title:\s*"(.+)"', content, re.MULTILINE)
        am = re.search(r"## Abstract\s*\n\n(.+?)(?:\n\n---|\Z)", content, re.DOTALL)
        if not tm or not am:
            continue

        title    = tm.group(1).replace('\\"', '"')
        abstract = am.group(1).strip()

        print(f"  Backfilling: {title[:60]}...")
        meta = generate_metadata(title, abstract)
        summary = meta["korean_summary"]
        new_tags = tags_yaml(meta["tags"])

        # Replace hardcoded tags line
        updated = re.sub(
            r'^tags:\s*\[.*?\]',
            f'tags: {new_tags}',
            content,
            flags=re.MULTILINE,
        )

        # Inject koreanSummary if missing
        if "koreanSummary:" not in updated and summary:
            updated = updated.replace(
                "\n---\n\n## Abstract",
                f'\nkoreanSummary: "{esc(summary)}"\n---\n\n## Abstract',
                1,
            )
        elif "koreanSummary:" in updated and summary:
            updated = re.sub(
                r'^koreanSummary:\s*".*"',
                f'koreanSummary: "{esc(summary)}"',
                updated,
                flags=re.MULTILINE,
            )

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(updated)
        done += 1
        time.sleep(2)

    print(f"Backfill complete: {done} post(s) updated.")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # ── Phase 1: Load model + fetch ──────────────────────────────────────────
    print(f"Loading semantic model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)
    target_emb = model.encode(TARGET_CONCEPT, convert_to_tensor=True)

    entries = fetch_arxiv(max_results=FETCH_POOL_SIZE)
    if not entries:
        print("No entries returned from arXiv.")
        return

    # ── Phase 2: Batch-score ALL papers in one shot (fast) ───────────────────
    # Encoding one at a time (50 calls) is slow; batch encodes all at once.
    print(f"Batch-scoring {len(entries)} papers...")
    texts = [f"{e['title']}. {e['summary']}" for e in entries]
    embeddings = model.encode(
        texts, convert_to_tensor=True, batch_size=32, show_progress_bar=False
    )
    scores = util.pytorch_cos_sim(target_emb, embeddings)[0].tolist()

    for entry, score in zip(entries, scores):
        entry["score"] = score

    # Sort by score descending; keep only new (not already saved) papers
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

    # ── Phase 3: Gemini only for winners ─────────────────────────────────────
    saved = 0
    for entry in winners:
        title    = entry["title"]
        abstract = entry["summary"]
        score    = entry["score"]

        print(f"  [{score:.2f}] {title[:65]}...")
        meta    = generate_metadata(title, abstract)
        summary = meta["korean_summary"]
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
            f'{abstract[:2000]}\n\n'
            f'---\n\n'
            f'*Relevance score: {score:.4f}*\n'
        )

        with open(entry["fpath"], "w", encoding="utf-8") as f:
            f.write(content)
        saved += 1
        time.sleep(1)  # gentle rate-limit

    print(f"\nFetch complete. {saved} new paper(s) saved.")

    # ── Phase 4: Backfill existing posts (capped) ────────────────────────────
    print("\nChecking existing posts for backfill...")
    backfill(model, target_emb)


if __name__ == "__main__":
    main()
