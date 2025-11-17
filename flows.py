from prefect import flow, task
from pipelines.extract import extract_products
from pipelines.transform import normalize_products
from pipelines.load import to_parquet_and_csv  # ⬅ use new function


@task
def extract_t():
    return extract_products()

@task
def transform_t(raw_path):
    return normalize_products(raw_path)

@task
def load_t(df):
    return to_parquet_and_csv(df)


@flow(name="fake-store-etl")
def run_pipeline():
    raw_path = extract_t()
    df = transform_t(raw_path)
    parquet_path, csv_path = load_t(df)
    print(f"ETL complete → {parquet_path} and {csv_path}")


if __name__ == "__main__":
    run_pipeline()
