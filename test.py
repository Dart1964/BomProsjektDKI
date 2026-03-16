# Denne filen tester noen viktige deler av programmet
# Den bruker print for å vise om testene fungerer

import requests

# samme API-nøkkel som i hovedprogrammet
API_KEY = "f95c9411"


print("STARTER SYSTEMTESTER") 


# TEST 1
# Tester om OMDb API svarer
print("\nTEST 1: Tester API-tilkobling")

url = f"http://www.omdbapi.com/?t=Batman&apikey={API_KEY}"

data = requests.get(url).json()

if data.get("Response") == "True":
    print("OK: API fungerer")
else:
    print("FEIL: API svarer ikke")


# TEST 2
# Tester filmsøk
print("\nTEST 2: Tester filmsøk")

url = f"http://www.omdbapi.com/?s=Batman&type=movie&apikey={API_KEY}"

data = requests.get(url).json()

if data.get("Response") == "True":
    results = data["Search"]
    print("OK: Fant", len(results), "filmer")
else:
    print("FEIL: Filmsøk fungerer ikke")


# TEST 3
# Tester at en bestemt film kan hentes
print("\nTEST 3: Tester henting av filmdata")

url = f"http://www.omdbapi.com/?t=Inception&apikey={API_KEY}"

data = requests.get(url).json()

if data.get("Title"):
    print("OK: Film hentet:", data["Title"])
else:
    print("FEIL: Kunne ikke hente film")


# TEST 4
# Tester henting av serieepisoder
print("\nTEST 4: Tester serieepisoder")

url = f"http://www.omdbapi.com/?t=Breaking Bad&Season=1&apikey={API_KEY}"

data = requests.get(url).json()

if "Episodes" in data:
    print("OK: Fant", len(data["Episodes"]), "episoder i sesong 1")
else:
    print("FEIL: Episoder ble ikke hentet")


print("\n------ SYSTEMTESTER FERDIG ------")