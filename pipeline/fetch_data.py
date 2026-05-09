import os
import re
import time
import urllib.request
import urllib.parse
import urllib.error
import feedparser
from datetime import datetime, timezone
from sentence_transformers import SentenceTransformer, util

# ── Configuration ────────────────────────────────────────────────────────────

SEARCH_QUERY = (
    'all:"cognitive science" OR all:"neural manifolds" OR all:"active inference"'
)
FETCH_POOL_SIZE = 50      # arXiv papers to pull per run
TARGET_SAVED_COUNT = 15   # max new papers to save per run
MODEL_NAME = "all-MiniLM-L6-v2"
OUTPUT_DIR = "src/data/blog"  # must match BLOG_PATH in content.config.ts

TARGET_CONCEPT = (
    "Cognitive science research involving neural representations, "
    "computational modeling, active inference, and brain functions."
)

# ── Gemini setup ─────────────────────────────────────────────────────────────

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_ENABLED = bool(GEMINI_API_KEY)

def generate_korean_summary(title: str, abstract: str) -> str:
    """Call Gemini Flash to produce a 2–3 sentence Korean summary."""
    if not GEMINI_ENABLED:
        print("  [Gemini] GEMINI_API_KEY not set — skipping Korean summary.")
        return ""

    import urllib.request, json
    prompt = (
        "다음 논문의 제목과 초록을 읽고, 핵심 내용을 한국어로 2~3문장으로 "
        "간결하게 요약해 주세요. 학술적이고 명확한 어조를 사용하세요.\n\n"
        f"제목: {title}\n\n"
        f"초록: {abstract[:1500]}\n\n"
        "한국어 요약:"
    )
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 256, "temperature": 0.3},
    }).encode()

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    )
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}, method="POST"
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read())
            return (
                data["candidates"][0]["content"]["parts"][0]["text"].strip()
            )
        except Exception as e:
            print(f"  [Gemini] attempt {attempt+1} failed: {e}")
            time.sleep(5 * (attempt + 1))
    return ""

# ── arXiv helpers ─────────────────────────────────────────────────────────────

def fetch_arxiv_papers(max_results: int = 50) -> bytes:
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
                print(f"  Rate limited (429). Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise Exception("arXiv API unreachable after 3 attempts.")

# ── Filename / YAML helpers ──────────────────────────────────────────────────

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

# ── Backfill: add Korean summaries to existing posts that lack them ──────────

def backfill_korean_summaries():
    """Scan OUTPUT_DIR for posts without koreanSummary and add them via Gemini."""
    if not GEMINI_ENABLED:
        print("Backfill skipped — GEMINI_API_KEY not set.")
        return

    md_files = [
        os.path.join(OUTPUT_DIR, f)
        for f in os.listdir(OUTPUT_DIR)
        if f.endswith(".md")
    ]
    backfilled = 0
    for filepath in md_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Skip if already has koreanSummary
        if "koreanSummary:" in content:
            continue

        # Extract title and abstract from the file
        title_match = re.search(r'^title:\s*"(.+)"', content, re.MULTILINE)
        abstract_match = re.search(
            r"## Abstract\s*\n\n(.+?)(?:\n\n---|\Z)", content, re.DOTALL
        )

        if not title_match or not abstract_match:
            continue

        title = title_match.group(1).replace('\\"', '"')
        abstract = abstract_match.group(1).strip()

        print(f"  Backfilling Korean summary for: {title[:60]}...")
        summary = generate_korean_summary(title, abstract)
        if not summary:
            continue

        # Inject koreanSummary before the closing --- of the frontmatter
        updated = content.replace(
            "\n---\n\n## Abstract",
            f'\nkoreanSummary: "{escape_yaml(summary)}"\n---\n\n## Abstract',
            1,
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated)
        backfilled += 1
        # Be polite to Gemini rate limits
        time.sleep(2)

    print(f"Backfill complete. {backfilled} post(s) updated with Korean summaries.")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # 1. Load semantic model
    print(f"Loading semantic model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)
    target_embedding = model.encode(TARGET_CONCEPT, convert_to_tensor=True)

    # 2. Fetch and score papers from arXiv
    try:
        xml_data = fetch_arxiv_papers(max_results=FETCH_POOL_SIZE)
        feed = feedparser.parse(xml_data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    entries = feed.get("entries", [])
    print(f"Received {len(entries)} entries. Scoring...")

    scored = []
    for entry in entries:
        title = entry.get("title", "").strip().replace("\n", " ")
        summary = entry.get("summary", "").strip().replace("\n", " ")
        if not title or not summary:
            continue
        emb = model.encode(f"{title}. {summary}", convert_to_tensor=True)
        score = util.pytorch_cos_sim(target_embedding, emb).item()
        scored.append({"score": score, "entry": entry, "title": title, "summary": summary})

    scored.sort(key=lambda x: x["score"], reverse=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 3. Save top papers
    saved = 0
    for item in scored:
        if saved >= TARGET_SAVED_COUNT:
            break

        entry = item["entry"]
        title = item["title"]
        abstract = item["summary"]
        score = item["score"]

        slug = sanitize_filename(title)
        if not slug:
            continue

        filepath = os.path.join(OUTPUT_DIR, f"{slug}.md")
        if os.path.exists(filepath):
            continue

        try:
            pub_date = format_astro_date(entry.get("published", ""))
        except ValueError:
            continue

        link = entry.get("link", "")

        # Generate Korean summary via Gemini
        print(f"  [{score:.2f}] {title[:60]}...")
        korean_summary = generate_korean_summary(title, abstract)
        korean_line = (
            f'koreanSummary: "{escape_yaml(korean_summary)}"\n' if korean_summary else ""
        )

        content = (
            f'---\n'
            f'author: "CogniGraph Bot"\n'
            f'pubDatetime: {pub_date}\n'
            f'title: "{escape_yaml(title)}"\n'
            f'featured: false\n'
            f'draft: false\n'
            f'tags: ["research", "cognitive-science"]\n'
            f'description: "[arXiv]({link}) — relevance score: {score:.2f}"\n'
            f'{korean_line}'
            f'---\n\n'
            f'## Abstract\n\n'
            f'{abstract[:2000]}\n\n'
            f'---\n\n'
            f'*Relevance score: {score:.4f}*\n'
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Saved: {title[:60]}")
        saved += 1
        time.sleep(2)  # Gemini rate limit courtesy

    print(f"\nFetch complete. {saved} new paper(s) saved.")

    # 4. Backfill Korean summaries for existing posts that don't have one
    print("\nChecking for existing posts without Korean summaries...")
    backfill_korean_summaries()


if __name__ == "__main__":
    main()
