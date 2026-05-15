import os
import re
import time
import urllib.request
import urllib.parse
import urllib.error
import feedparser
from datetime import datetime, timezone
from sentence_transformers import SentenceTransformer, util
from deep_translator import GoogleTranslator

SEARCH_QUERY = (
    'all:"cognitive science" OR all:"neural manifolds" OR all:"active inference"'
)
FETCH_POOL  = 50
SAVE_TARGET = 5
MODEL       = "all-MiniLM-L6-v2"
OUT_DIR     = "src/data"
CONCEPT     = (
    "Cognitive science research involving neural representations, "
    "computational modeling, active inference, and brain functions."
)


def translate(text: str) -> str:
    for attempt in range(3):
        try:
            result = GoogleTranslator(source="en", target="ko").translate(text)
            if result:
                return result.strip()
        except Exception as e:
            print(f"  [translate] attempt {attempt + 1}: {e}")
            time.sleep(3)
    return ""


def fetch_arxiv(n: int) -> list[dict]:
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({
        "search_query": SEARCH_QUERY,
        "start": 0,
        "max_results": n,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    print(f"Fetching {n} papers from arXiv...")
    
    # Define a clean request with a custom User-Agent to avoid getting auto-blocked
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'CognigraphBot/1.0 (github.com/runner/work/cognigraph; contact-your-email@example.com)'
        }
    )
    
    for attempt in range(3):
        try:
            # Added a 30s timeout here to avoid hanging infinitely
            with urllib.request.urlopen(req, timeout=30) as response:
                feed = feedparser.parse(response.read())
                
            return [
                {
                    "title":     e.get("title", "").strip().replace("\n", " "),
                    "summary":   e.get("summary", "").strip().replace("\n", " "),
                    "link":      e.get("link", ""),
                    "published": e.get("published", ""),
                }
                : e.get("title") and e.get("link")
            ]
            
        except urllib.error.HTTPError as e:
            # Handle rate limiting (429) or temporary server errors (5xx)
            sleep_time = 20 * (attempt + 1)
            print(f"  [arXiv HTTP Error {e.code}] Attempt {attempt + 1} failed. Waiting {sleep_time}s...")
            time.sleep(sleep_time)
            
        except (urllib.error.URLError, Exception) as e:
            # Crucial: Catch timeouts and network drops, and apply an exponential backoff
            sleep_time = 10 * (attempt + 1)
            print(f"  [arXiv Network Error] {e}. Attempt {attempt + 1} failed. Waiting {sleep_time}s...")
            time.sleep(sleep_time)
            
    raise Exception("arXiv unreachable after 3 attempts")

def to_slug(title: str, max_len: int = 50) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:max_len].rstrip("-")


def to_astro_date(s: str) -> str:
    dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def main():
    print(f"Loading {MODEL}...")
    model = SentenceTransformer(MODEL)
    anchor = model.encode(CONCEPT, convert_to_tensor=True)

    entries = fetch_arxiv(FETCH_POOL)
    if not entries:
        print("No entries from arXiv.")
        return

    print(f"Scoring {len(entries)} papers...")
    embs = model.encode(
        [f"{e['title']}. {e['summary']}" for e in entries],
        convert_to_tensor=True, batch_size=32, show_progress_bar=False,
    )
    for entry, score in zip(entries, util.pytorch_cos_sim(anchor, embs)[0].tolist()):
        entry["score"] = score
    entries.sort(key=lambda x: x["score"], reverse=True)

    os.makedirs(OUT_DIR, exist_ok=True)

    saved = 0
    for entry in entries:
        if saved >= SAVE_TARGET:
            break
        slug = to_slug(entry["title"])
        if not slug or os.path.exists(os.path.join(OUT_DIR, f"{slug}.md")):
            continue
        try:
            pub = to_astro_date(entry["published"])
        except ValueError:
            continue

        title = entry["title"]
        score = entry["score"]
        print(f"  [{score:.2f}] {title[:65]}")

        korean = translate(title)
        korean_line = f'koreanSummary: "{esc(korean)}"\n' if korean else ""

        with open(os.path.join(OUT_DIR, f"{slug}.md"), "w", encoding="utf-8") as f:
            f.write(
                f'---\n'
                f'pubDatetime: {pub}\n'
                f'title: "{esc(title)}"\n'
                f'link: "{entry["link"]}"\n'
                f'{korean_line}'
                f'---\n\n'
                f'{entry["summary"][:2000]}\n'
            )
        saved += 1

    print(f"\nDone. {saved} paper(s) saved.")


if __name__ == "__main__":
    main()
