from pipelines.extract import extract_products
from pipelines.transform import normalize_products
from pipelines.load import to_parquet

def main():
    # 1) EXTRACT
    raw_path = extract_products()
    print(f"✅ Extracted raw data to {raw_path}")

    # 2) TRANSFORM
    df = normalize_products(raw_path)
    print(f"✅ Transformed {len(df)} records")

    # 3) LOAD
    pq = to_parquet(df)
    print(f"✅ Saved curated data to {pq}")

    print("🎉 Pipeline completed successfully!")

if __name__ == "__main__":
    main()
