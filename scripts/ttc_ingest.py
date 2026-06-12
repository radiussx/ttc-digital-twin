import requests
import pandas as pd
from datetime import datetime
from google.transit import gtfs_realtime_pb2

url = "https://bustime.ttc.ca/gtfsrt/vehicles"

feed = gtfs_realtime_pb2.FeedMessage()

response = requests.get(url)

feed.ParseFromString(response.content)

rows = []

for entity in feed.entity:
    if entity.HasField("vehicle"):
        vehicle = entity.vehicle
        rows.append({
           "vehicle_id": vehicle.vehicle.id,
    "route_id": vehicle.trip.route_id,
    "trip_id": vehicle.trip.trip_id,
    "latitude": vehicle.position.latitude,
    "longitude": vehicle.position.longitude,
    "timestamp": datetime.now()
        })

df = pd.DataFrame(rows)

filename = (
    f"data/raw/ttc_vehicles_"
    f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
)

df.to_parquet(filename)

print(df.head())
print(f"\nSaved {len(df)} vehicles")