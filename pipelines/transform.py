from pathlib import Path
import pandas as pd
import json

def normalize_products(raw_path: Path) -> pd.DataFrame:
    """
    Read the raw JSON file, flatten to a table, clean columns/types,
    add a simple derived metric, and return a DataFrame.
    """
    # Load the JSON file into Python
    payload = json.loads(Path(raw_path).read_text())

    # Convert nested JSON data into a flat table
    df = pd.json_normalize(payload)

    # Clean column names (lowercase, replace spaces and dots with underscores)
    df.columns = [
        c.strip().lower().replace(" ", "_").replace(".", "_") for c in df.columns
    ]

    # Make sure these important columns always exist
    required = ["id", "title", "price", "category", "rating_rate", "rating_count"]
    for col in required:
        if col not in df.columns:
            df[col] = None

    # Convert data to correct types
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["rating_rate"] = pd.to_numeric(df.get("rating_rate"), errors="coerce")
    df["rating_count"] = pd.to_numeric(df.get("rating_count"), errors="coerce")
    df["title"] = df["title"].astype("string")
    df["category"] = df["category"].astype("string")

    # Example derived metric: price with 20% VAT added
    df["price_with_vat"] = (df["price"] * 1.20).round(2)

    # Remove any duplicates and reset the index
    df = df.drop_duplicates(subset=["id"]).reset_index(drop=True)

    # Return the cleaned DataFrame
    return df
