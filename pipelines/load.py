from pathlib import Path
import pandas as pd

def to_parquet(df: pd.DataFrame) -> Path:
    """
    Save the cleaned DataFrame to data/curated/products.parquet and return the file path.
    """
    # Define where to save the final dataset
    out = Path("data/curated") / "products.parquet"

    # Make sure the folder exists before saving
    out.parent.mkdir(parents=True, exist_ok=True)

    # Save the DataFrame as a Parquet file (a compact, fast format)
    df.to_parquet(out, index=False)

    # Return the file path so the next step can use it
    return out
