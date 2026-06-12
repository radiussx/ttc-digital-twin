from pathlib import Path
import pandas as pd

latest_file = max(
    Path("data/raw").glob("ttc_vehicles_*.parquet")
)

df = pd.read_parquet(latest_file)

print(df.head())

print("\nUnique Routes:", df["route_id"].nunique())