from pathlib import Path
import pandas as pd

latest_file = max(
    Path("data/raw").glob("ttc_vehicles_*.parquet")
)

df = pd.read_parquet(latest_file)

df = df[df["route_id"] != ""]

route_counts = (
    df.groupby("route_id")
      .size()
      .reset_index(name="vehicle_count")
      .sort_values(
          "vehicle_count",
          ascending=False
      )
)

print(route_counts.head(20))