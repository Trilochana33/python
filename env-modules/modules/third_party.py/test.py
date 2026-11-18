import requests

city = input("Enter city name: ")

url = f"https://wttr.in/{city}?format=j1"

response = requests.get(url)

data = response.json()
current = data["current_condition"][0]
print(current)

print (current["temp_C"])

print(current["FeelsLikeF"])

print(current["humidity"])