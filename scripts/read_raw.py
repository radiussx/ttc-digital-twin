from pathlib import Path
import pandas as pd

files = list(Path("data/raw").glob("*.parquet"))

latest_file = max(files)

print("Reading:", latest_file)

df = pd.read_parquet(latest_file)

print(df[["name", "email"]])