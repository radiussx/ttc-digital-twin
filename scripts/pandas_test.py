import json
import pandas as pd

with open("data/users.json", "r") as file:
    users = json.load(file)

df = pd.DataFrame(users)

df.to_parquet("data/users.parquet")

print("Parquet saved!")