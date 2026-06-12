from pathlib import Path

files = Path("data/raw").glob("*.parquet")

for file in files:
    print(file)