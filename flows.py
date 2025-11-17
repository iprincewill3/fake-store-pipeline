from prefect import flow, task
from pipelines.extract import extract_products
from pipelines.transform import normalize_products
from pipelines.load import to_parquet

@task
def extract_t():
    return extract_products()

@task
def transform_t(raw_path):
    return normalize_products(raw_path)

@task
def load_t(df):
    return to_parquet(df)

@flow(name="fake-store-etl")
def run_pipeline():
    raw_path = extract_t()
    df = transform_t(raw_path)
    pq = load_t(df)
    print(f"ETL Flow complete. Output: {pq}")   # <— no emoji

if __name__ == "__main__":
    run_pipeline()
