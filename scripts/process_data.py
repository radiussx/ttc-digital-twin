from pathlib import Path
import pandas as pd

files = list(Path("data/raw").glob("*.parquet"))

latest_file = max(files)

df = pd.read_parquet(latest_file)

processed = df[["id", "name", "email"]]

processed.to_parquet(
    "data/processed/users_processed.parquet"
)

print("Processed data saved!")