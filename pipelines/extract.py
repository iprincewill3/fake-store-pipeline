import requests
from pathlib import Path
import json
import time

PRODUCTS_URL = "https://fakestoreapi.com/products"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

def extract_products() -> Path:
    resp = requests.get(PRODUCTS_URL, timeout=30, headers=HEADERS)
    resp.raise_for_status()  # still fail fast on bad responses
    data = resp.json()

    ts = time.strftime("%Y%m%d_%H%M%S")
    out = Path("data/raw") / f"products_{ts}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return out
