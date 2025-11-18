# pipelines/extract.py
import os
import json
import time
from pathlib import Path

import requests

PRODUCTS_URL = "https://fakestoreapi.com/products"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def _write_snapshot(payload) -> Path:
    """
    Helper: write the given payload to data/raw/products_<timestamp>.json
    and return the path.
    """
    ts = time.strftime("%Y%m%d_%H%M%S")
    out = Path("data/raw") / f"products_{ts}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return out


def extract_products() -> Path:
    """
    Extract products data.

    - Locally: calls the live Fake Store API.
    - On GitHub Actions: uses a static snapshot from sample_data/products_seed.json
      to avoid 403 errors/remote blocking.
    """
    # Detect GitHub Actions environment
    if os.getenv("GITHUB_ACTIONS") == "true":
        # Use snapshot instead of live API
        snapshot_path = Path("sample_data/products_seed.json")
        payload = json.loads(snapshot_path.read_text())
        return _write_snapshot(payload)

    # Otherwise: normal live API call (for local runs)
    resp = requests.get(PRODUCTS_URL, timeout=30, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    return _write_snapshot(data)
