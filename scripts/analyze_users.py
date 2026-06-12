import pandas as pd

df = pd.read_parquet(
    "data/processed/users_processed.parquet"
)

print("\nRows:", len(df))
print("\nColumns:")
print(df.columns)

print("\nFirst 5 rows:")
print(df.head())