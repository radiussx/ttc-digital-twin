import requests
import json

response = requests.get(
    "https://jsonplaceholder.typicode.com/users"
)

data = response.json()

with open("data/users.json", "w") as file:
    json.dump(data, file, indent=4)

print("Data saved successfully!")