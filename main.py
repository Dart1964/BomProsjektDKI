import tkinter as tk          # tkinter brukes til å lage grafiske vinduer (GUI)
from tkinter import messagebox  # brukes til å vise feilmeldinger i popup-vinduer
import requests               # brukes til å hente data fra internett (API)
import matplotlib.pyplot as plt  # brukes til å lage grafer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # gjør at grafen kan vises i tkinter

API_KEY = "f95c9411"  # API-nøkkel for OMDb (film-database på nett)


def clear_output():
    # Fjerner alt som vises i output_frame før nye resultater vises
    for widget in output_frame.winfo_children():  # finner alle widgets i rammen
        widget.destroy()  # sletter widgeten fra vinduet


def show_cast(data):
    # Viser regissør og manusforfatter
    tk.Label(output_frame, text="Director: " + data.get("Director", "N/A"),
             font=("Arial", 11, "italic"), fg="#444").pack(anchor="w", padx=10)

    tk.Label(output_frame, text="Writer: " + data.get("Writer", "N/A"),
             font=("Arial", 11, "italic"), fg="#444").pack(anchor="w", padx=10)

    # Overskrift for skuespillere
    tk.Label(output_frame, text="Actors:", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(8, 2))

    # Deler opp skuespillerlisten og viser én per linje
    for actor in data.get("Actors", "N/A").split(", "):
        tk.Label(output_frame, text=f"  • {actor}", font=("Arial", 11)).pack(anchor="w", padx=20)


def show_movie():
    # Henter informasjon om en film og viser vurderinger
    clear_output()  # fjerner tidligere resultater

    movie = entry.get()  # leser teksten brukeren skrev inn

    # Lager URL til OMDb API
    url = f"http://www.omdbapi.com/?t={movie}&apikey={API_KEY}"

    # Sender forespørsel til API og gjør svaret om til en dictionary
    data = requests.get(url).json()

    # Hvis filmen ikke finnes
    if data.get("Response") == "False":
        messagebox.showerror("Error", data.get("Error"))
        return

    # Viser filmens tittel
    tk.Label(output_frame, text=f"Title: {data['Title']}", font=("Arial", 12)).pack()

    # Overskrift for vurderinger
    tk.Label(output_frame, text="Ratings:", font=("Arial", 12, "bold")).pack()

    # Viser alle vurderingene
    if "Ratings" in data:
        for rating in data["Ratings"]:
            text = f"{rating['Source']} : {rating['Value']}"
            tk.Label(output_frame, text=text).pack()
    else:
        tk.Label(output_frame, text="No ratings available").pack()

    # Viser regissør, writer og skuespillere
    show_cast(data)


def show_series():
    # Henter rating for alle episoder i en serie og lager grafer
    clear_output()

    series = entry.get()  # serien brukeren skrev inn

    # Henter grunnleggende info om serien
    url = f"http://www.omdbapi.com/?t={series}&apikey={API_KEY}"
    data = requests.get(url).json()

    # Feil hvis serien ikke finnes
    if data.get("Response") == "False":
        messagebox.showerror("Error", data.get("Error"))
        return

    # Feil hvis resultatet ikke er en serie
    if "totalSeasons" not in data:
        messagebox.showerror("Error", "Not a series")
        return

    show_cast(data)  # viser regissør og skuespillere

    total_seasons = int(data["totalSeasons"])  # hvor mange sesonger serien har

    episode_numbers = []  # episodenummer til x-aksen
    ratings = []          # rating til y-aksen

    episode_counter = 1   # teller episoder gjennom alle sesonger

    # Går gjennom hver sesong
    for season in range(1, total_seasons + 1):

        # Henter episoder fra denne sesongen
        season_url = f"http://www.omdbapi.com/?t={series}&Season={season}&apikey={API_KEY}"
        season_data = requests.get(season_url).json()

        # Går gjennom alle episodene
        for ep in season_data["Episodes"]:

            rating = ep["imdbRating"]

            # Hopper over episoder uten rating
            if rating != "N/A":
                episode_numbers.append(episode_counter)
                ratings.append(float(rating))

            episode_counter += 1

    # Hvis ingen rating ble funnet
    if not ratings:
        messagebox.showerror("Error", "No ratings found")
        return

    root.geometry("800x900")  # gjør vinduet større så grafene får plass

    # Lager to grafer (linjegraf og stolpediagram)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

    step = max(1, len(episode_numbers) // 20)  # bestemmer hvor mange x-verdier som vises

    # -------- Linjegraf --------
    ax1.plot(episode_numbers, ratings, marker='o', linestyle='-')
    ax1.set_xlabel("Episode Number")
    ax1.set_ylabel("IMDb Rating")
    ax1.set_title(f"{series} - Line Plot")
    ax1.set_ylim(0, 10.1)
    ax1.set_yticks([i * 0.5 for i in range(21)])  # y-akse fra 0 til 10
    ax1.set_xticks(range(1, len(episode_numbers) + 1, step))
    ax1.tick_params(axis='x', rotation=45)

    # -------- Stolpediagram --------
    ax2.bar(episode_numbers, ratings, color='skyblue')
    ax2.set_xlabel("Episode Number")
    ax2.set_ylabel("IMDb Rating")
    ax2.set_title(f"{series} - Bar Chart")
    ax2.set_ylim(0, 10.1)
    ax2.set_yticks([i * 0.5 for i in range(21)])
    ax2.set_xticks(range(1, len(episode_numbers) + 1, step))
    ax2.tick_params(axis='x', rotation=45)

    fig.tight_layout()  # justerer avstanden mellom grafene

    # Legger grafen inn i tkinter-vinduet
    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# -------- GUI OPPSETT --------

root = tk.Tk()  # lager hovedvinduet
root.title("Movie / Series Rating Viewer")  # tekst øverst i vinduet

# Overskrift i vinduet
title = tk.Label(root, text="Enter Movie or Series Name", font=("Arial", 14))
title.pack(pady=10)

# Tekstfelt der brukeren skriver film eller serie
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Frame brukes til å gruppere knappene
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Knapp som viser filmratings
movie_button = tk.Button(button_frame, text="Movie Ratings", command=show_movie)
movie_button.grid(row=0, column=0, padx=10)

# Knapp som lager graf for serier
series_button = tk.Button(button_frame, text="Series Graph", command=show_series)
series_button.grid(row=0, column=1, padx=10)

# Område der resultater og grafer vises
output_frame = tk.Frame(root)
output_frame.pack(pady=20)

# Holder programmet i gang og venter på brukerinteraksjon
root.mainloop()