import json

with open("data/users.json", "r") as file:
    users = json.load(file)

for user in users:
    print(user["name"])