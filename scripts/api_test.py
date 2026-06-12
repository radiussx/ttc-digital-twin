import requests

response = requests.get(
    "https://jsonplaceholder.typicode.com/users"
)

print("Status Code:", response.status_code)

print("\nData:")

print(response.json())