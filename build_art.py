"""
Builds the compressed card art library for the Master Duel Companion App.

For every card that's in Master Duel (per the companion's cards.json), downloads the full card
image from YGOPRODeck once, shrinks it to 421x614 (the size the app shows cards at) and saves it
as art/<card id>.avif. Cards already in art/ are skipped, so weekly runs only add new cards.
"""
import io, json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

CARDS = "https://gabegriffin16-commits.github.io/ygo-md-companion/cards.json"
IMG = "https://images.ygoprodeck.com/images/cards/{}.jpg"
SIZE = (421, 614)
QUALITY = 60
HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "art")
UA = {"User-Agent": "MasterDuelCompanion-art/1.0 (personal use; images re-hosted per YGOPRODeck API guidance)"}

def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))

def convert(card_id):
    out = os.path.join(ART, f"{card_id}.avif")
    if os.path.exists(out):
        return "skip"
    try:
        im = Image.open(io.BytesIO(get(IMG.format(card_id)))).convert("RGB")
        im = im.resize(SIZE, Image.LANCZOS)
        tmp = out + ".tmp"
        im.save(tmp, "AVIF", quality=QUALITY)
        os.replace(tmp, out)
        time.sleep(0.12)            # stay well under YGOPRODeck's rate limit
        return "new"
    except Exception as e:
        print(f"  {card_id}: {e}", file=sys.stderr)
        return "fail"

def main():
    os.makedirs(ART, exist_ok=True)
    cards = json.loads(get(CARDS))["cards"]
    ids = [c["id"] for c in cards if c.get("md")]
    limit = int(os.environ.get("ART_LIMIT", "0") or 0)
    missing = [i for i in ids if not os.path.exists(os.path.join(ART, f"{i}.avif"))]
    todo = missing[:limit] if limit else missing
    print(f"{len(ids)} Master Duel cards, {len(ids) - len(missing)} already done, converting {len(todo)}")
    stats = {"new": 0, "skip": 0, "fail": 0}
    with ThreadPoolExecutor(max_workers=6) as pool:
        for n, res in enumerate(pool.map(convert, todo), 1):
            stats[res] += 1
            if n % 500 == 0:
                print(f"  {n}/{len(todo)} ...", flush=True)
    total = sum(os.path.getsize(os.path.join(ART, f)) for f in os.listdir(ART) if f.endswith(".avif"))
    print(f"Done: {stats}. Library: {len(os.listdir(ART))} files, {total / 1e6:.0f} MB")

if __name__ == "__main__":
    main()
