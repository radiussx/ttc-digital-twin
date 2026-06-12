import requests
import pandas as pd
from datetime import datetime

response = requests.get(
    "https://jsonplaceholder.typicode.com/users"
)

data = response.json()

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

df = pd.DataFrame(data)

filename = f"data/raw/users_{timestamp}.parquet"

df.to_parquet(filename)

print(f"Saved: {filename}")