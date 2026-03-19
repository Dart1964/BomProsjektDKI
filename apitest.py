import requests
import json

API_KEY = "f95c9411"


def search_movie(title):
    url = f"http://www.omdbapi.com/?s={title}&type=movie&apikey={API_KEY}"
    return requests.get(url).json()


def get_by_id(imdb_id):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={API_KEY}"
    return requests.get(url).json()


def get_season(imdb_id, season):
    url = f"http://www.omdbapi.com/?i={imdb_id}&Season={season}&apikey={API_KEY}"
    return requests.get(url).json()


# 1. Søk etter en film
search_data = search_movie("Inception")
print("=== SEARCH DATA ===")
print(json.dumps(search_data, indent=4))

# 2. Hent detaljer for første treff
if search_data.get("Response") == "True":
    first_id = search_data["Search"][0]["imdbID"]

    detail_data = get_by_id(first_id)
    print("\n=== DETAIL DATA ===")
    print(json.dumps(detail_data, indent=4))

# 3. Test serie + sesongdata
series_search = search_movie("Breaking Bad")

if series_search.get("Response") == "True":
    series_id = series_search["Search"][0]["imdbID"]

    season_data = get_season(series_id, 1)
    print("\n=== SEASON DATA ===")
    print(json.dumps(season_data, indent=4))