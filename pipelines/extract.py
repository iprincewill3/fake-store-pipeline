# pipelines/extract.py
import os
import json
import time
from pathlib import Path

import requests
from requests import HTTPError, RequestException

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


def _load_seed_payload() -> list:
    """
    Load the static snapshot we commit to the repo.
    Used as a fallback when the live API is unavailable.
    """
    snapshot_path = Path("sample_data/products_seed.json")
    return json.loads(snapshot_path.read_text())


def extract_products() -> Path:
    """
    Extract products data.

    - On GitHub Actions (GITHUB_ACTIONS="true"): always use the snapshot,
      to avoid API blocking or rate limits.
    - Locally: try the live API first; if it fails, fall back to the snapshot.
    """
    # Detect GitHub Actions environment
    if os.getenv("GITHUB_ACTIONS") == "true":
        print("GITHUB_ACTIONS detected → using snapshot data only.")
        payload = _load_seed_payload()
        return _write_snapshot(payload)

    # Local run: try live API with graceful fallback
    try:
        print(f"Requesting live data from {PRODUCTS_URL} ...")
        resp = requests.get(PRODUCTS_URL, timeout=30, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        print(f"✅ Live API call succeeded, got {len(data)} records.")
        return _write_snapshot(data)

    except (HTTPError, RequestException) as e:
        print(f"⚠ Live API call failed: {e}")
        print("   Falling back to snapshot data from sample_data/products_seed.json ...")
        payload = _load_seed_payload()
        return _write_snapshot(payload)
