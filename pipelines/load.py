# pipelines/load.py
from pathlib import Path
import pandas as pd

def to_parquet_and_csv(df: pd.DataFrame):
    """
    Writes curated data under data/curated/ as:
      - products.parquet  (for Power BI Desktop)
      - products.csv      (for cloud / web usage)
    Returns both paths.
    """
    out_dir = Path("data/curated")
    out_dir.mkdir(parents=True, exist_ok=True)

    parquet_path = out_dir / "products.parquet"
    csv_path = out_dir / "products.csv"

    # Main BI file – this is already in use in Power BI Desktop
    df.to_parquet(parquet_path, index=False)

    # Extra copy – for GitHub Actions / web
    df.to_csv(csv_path, index=False)

    return parquet_path, csv_path
