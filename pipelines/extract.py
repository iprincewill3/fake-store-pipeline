import requests
import json
from pathlib import Path
import time

PRODUCTS_URL = "https://fakestoreapi.com/products"

def extract_products() -> Path:
    """
    Call the Fake Store API and save a timestamped raw JSON snapshot under data/raw/.
    Return the file path so the next step can use it.
    """
    resp = requests.get(PRODUCTS_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # timestamp for unique file name, e.g. 20250130_141530
    ts = time.strftime("%Y%m%d_%H%M%S")

    out = Path("data/raw") / f"products_{ts}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return out
