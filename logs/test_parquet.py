import pandas as pd

df = pd.read_parquet("data/curated/products.parquet")
print(df.head())
print("\nRows:", len(df))
