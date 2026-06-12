import requests
from google.transit import gtfs_realtime_pb2

url = "https://bustime.ttc.ca/gtfsrt/vehicles"

feed = gtfs_realtime_pb2.FeedMessage()

response = requests.get(url)

feed.ParseFromString(response.content)

print("Entities:", len(feed.entity))

for entity in feed.entity[:5]:
    if entity.HasField("vehicle"):
        print(
            entity.vehicle.vehicle.id,
            entity.vehicle.position.latitude,
            entity.vehicle.position.longitude
        )