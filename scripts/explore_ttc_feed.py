import requests
from google.transit import gtfs_realtime_pb2

url = "https://bustime.ttc.ca/gtfsrt/vehicles"

feed = gtfs_realtime_pb2.FeedMessage()

response = requests.get(url)

feed.ParseFromString(response.content)

count = 0

for entity in feed.entity:
    if entity.HasField("vehicle"):

        vehicle = entity.vehicle

        print("\nVehicle ID:", vehicle.vehicle.id)

        if vehicle.trip.route_id:
            print("Route ID:", vehicle.trip.route_id)

        if vehicle.trip.trip_id:
            print("Trip ID:", vehicle.trip.trip_id)

        count += 1

        if count >= 10:
            break