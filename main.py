import requests

API_KEY = "f95c9411"

movie = input("Enter movie name: ")

url = f"http://www.omdbapi.com/?t={movie}&apikey={API_KEY}"

response = requests.get(url)
data = response.json()

print("Title:", data["Title"])
print("Year:", data["Year"])
print("IMDb rating:", data["imdbRating"])

print("\nOther ratings:")
for rating in data["Ratings"]:
    print(rating["Source"], "-", rating["Value"])