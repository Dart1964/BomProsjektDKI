# tkinter brukes til å lage grafiske programmer
# (vinduer, knapper, tekstfelt osv.)
import tkinter as tk

# messagebox brukes til å vise popup-feilmeldinger
from tkinter import messagebox

# requests brukes til å hente data fra internett (API)
import requests

# matplotlib brukes til å lage grafer
import matplotlib.pyplot as plt

# gjør at matplotlib-grafer kan vises inni tkinter-vinduet
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# lager pene og jevnt fordelte tall på graf-aksene
from matplotlib.ticker import MaxNLocator

# API-nøkkel for OMDb (Open Movie Database)
API_KEY = "f95c9411"

# Denne funksjonen sletter alt som vises i resultatområdet
def clear_output():
    # finner alle elementene inni output_frame
    for widget in output_frame.winfo_children():
        # sletter elementet fra skjermen
        widget.destroy()

# Denne funksjonen viser regissør, manusforfatter og skuespillere
def show_cast(data):
    # viser regissør
    tk.Label(
        output_frame,
        text="Director: " + data.get("Director", "N/A"),
        font=("Arial", 11, "italic"),
        fg="#444"
    ).pack(anchor="w", padx=10)

    # viser manusforfatter
    tk.Label(
        output_frame,
        text="Writer: " + data.get("Writer", "N/A"),
        font=("Arial", 11, "italic"),
        fg="#444"
    ).pack(anchor="w", padx=10)

    # overskrift for skuespillere
    tk.Label(
        output_frame,
        text="Actors:",
        font=("Arial", 11, "bold")
    ).pack(anchor="w", padx=10, pady=(8, 2))

    # henter listen med skuespillere
    actors_text = data.get("Actors", "N/A")

    # split deler opp teksten ved hvert komma
    for actor in actors_text.split(", "):
        # viser en skuespiller per linje
        tk.Label(
            output_frame,
            text=f"  • {actor}",
            font=("Arial", 11)
        ).pack(anchor="w", padx=20)

# Denne funksjonen viser en bestemt film ved hjelp av imdb id
def show_movie_by_id(imdb_id):
    # fjerner gamle resultater
    clear_output()

    # lager URL til API-et
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={API_KEY}"

    # henter data fra API
    data = requests.get(url).json()

    # hvis filmen ikke finnes
    if data.get("Response") == "False":
        messagebox.showerror("Error", data.get("Error"))
        return

    # viser tittel og år
    tk.Label(
        output_frame,
        text=f"Title: {data['Title']} ({data.get('Year', 'N/A')})",
        font=("Arial", 12, "bold")
    ).pack()

    # viser type (movie eller series)
    tk.Label(
        output_frame,
        text=f"Type: {data.get('Type', 'N/A')}",
        font=("Arial", 11)
    ).pack()

    # overskrift for ratings
    tk.Label(
        output_frame,
        text="Ratings:",
        font=("Arial", 12, "bold")
    ).pack(pady=(8, 2))

    # viser alle ratings
    if "Ratings" in data and data["Ratings"]:
        for rating in data["Ratings"]:
            text = f"{rating['Source']} : {rating['Value']}"
            tk.Label(output_frame, text=text).pack()
    else:
        tk.Label(output_frame, text="No ratings available").pack()

    # viser regissør og skuespillere
    show_cast(data)

# Denne funksjonen åpner et nytt vindu der brukeren kan velge riktig film
def choose_title(results, callback):
    # lager nytt vindu
    select_window = tk.Toplevel(root)
    select_window.title("Choose Title")
    select_window.geometry("500x350")

    # tekst øverst i vinduet
    tk.Label(
        select_window,
        text="Choose the correct title",
        font=("Arial", 11, "bold")
    ).pack(pady=8)

    # liste som brukeren kan velge fra
    listbox = tk.Listbox(select_window, width=65, height=12)
    listbox.pack(padx=10, pady=10)

    # legger filmer inn i listen
    for item in results:
        title = item.get("Title", "Unknown")
        year = item.get("Year", "")
        item_type = item.get("Type", "")
        listbox.insert(tk.END, f"{title} ({year}) - {item_type}")

    # funksjon som kjøres når brukeren trykker Select
    def select_item():
        selected = listbox.curselection()

        if not selected:
            messagebox.showerror("Error", "Choose a title")
            return

        imdb_id = results[selected[0]]["imdbID"]
        select_window.destroy()

        # callback betyr at vi kjører funksjonen som ble sendt inn
        callback(imdb_id)

    # knapp for å velge film
    tk.Button(
        select_window,
        text="Select",
        command=select_item
    ).pack(pady=8)

# denne funksjonen søker etter filmer
def show_movie():
    # fjerner gamle resultater
    clear_output()

    # henter teksten brukeren skrev
    movie = entry.get().strip()

    if not movie:
        messagebox.showerror("Error", "Write a movie name")
        return

    # søker etter filmer i API
    url = f"http://www.omdbapi.com/?s={movie}&type=movie&apikey={API_KEY}"
    data = requests.get(url).json()

    if data.get("Response") == "False":
        messagebox.showerror("Error", data.get("Error"))
        return

    results = data["Search"]

    # hvis bare én film finnes
    if len(results) == 1:
        show_movie_by_id(results[0]["imdbID"])
    else:
        # ellers må brukeren velge riktig film
        choose_title(results, show_movie_by_id)

# denne funksjonen søker etter serier
def show_series():
    clear_output()
    series = entry.get().strip()

    if not series:
        messagebox.showerror("Error", "Write a series name")
        return

    url = f"http://www.omdbapi.com/?s={series}&type=series&apikey={API_KEY}"
    data = requests.get(url).json()

    if data.get("Response") == "False":
        messagebox.showerror("Error", data.get("Error"))
        return

    results = data["Search"]

    if len(results) == 1:
        show_series_by_id(results[0]["imdbID"])
    else:
        choose_title(results, show_series_by_id)

# denne funksjonen lager grafer for alle episoder i en serie
def show_series_by_id(imdb_id):
    clear_output()
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={API_KEY}"
    data = requests.get(url).json()

    if data.get("Response") == "False":
        messagebox.showerror("Error", data.get("Error"))
        return

    if "totalSeasons" not in data:
        messagebox.showerror("Error", "Not a series")
        return

    show_cast(data)
    total_seasons = int(data["totalSeasons"])
    episode_numbers = []
    ratings = []
    episode_counter = 1

    # går gjennom alle sesonger
    for season in range(1, total_seasons + 1):
        season_url = f"http://www.omdbapi.com/?i={imdb_id}&Season={season}&apikey={API_KEY}"
        season_data = requests.get(season_url).json()

        if "Episodes" not in season_data:
            continue

        # går gjennom alle episodene
        for ep in season_data["Episodes"]:
            rating = ep["imdbRating"]

            if rating != "N/A":
                episode_numbers.append(episode_counter)
                ratings.append(float(rating))

            episode_counter += 1

    if not ratings:
        messagebox.showerror("Error", "No ratings found")
        return

    root.geometry("950x1000")

    # fig er hele grafområdet
    # ax1 og ax2 er to grafer inni figuren
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9))

    # linjegraf
    ax1.plot(
        episode_numbers,
        ratings,
        marker="o",
        markersize=3,
        linewidth=1
    )
    ax1.set_xlabel("Episode Number")
    ax1.set_ylabel("IMDb Rating")
    ax1.set_title(f"{data['Title']} - Line Plot")
    ax1.set_ylim(0, 10)
    ax1.set_yticks(range(0, 11, 1))
    ax1.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))

    # stolpediagram
    ax2.bar(episode_numbers, ratings, color="skyblue")
    ax2.set_xlabel("Episode Number")
    ax2.set_ylabel("IMDb Rating")
    ax2.set_title(f"{data['Title']} - Bar Chart")
    ax2.set_ylim(0, 10)
    ax2.set_yticks(range(0, 11, 1))
    ax2.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))

    fig.subplots_adjust(hspace=0.35)

    # viser grafen i tkinter
    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# lager hovedvinduet
root = tk.Tk()
root.title("Movie / Series Rating Viewer")

# overskrift
title = tk.Label(
    root,
    text="Enter Movie or Series Name",
    font=("Arial", 14)
)
title.pack(pady=10)

# tekstfelt der brukeren skriver navn
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# ramme for knappene
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# knapp for film
movie_button = tk.Button(
    button_frame,
    text="Movie Ratings",
    command=show_movie
)
movie_button.grid(row=0, column=0, padx=10)

# knapp for serie
series_button = tk.Button(
    button_frame,
    text="Series Graph",
    command=show_series
)
series_button.grid(row=0, column=1, padx=10)

# område der resultater vises
output_frame = tk.Frame(root)
output_frame.pack(pady=20, fill=tk.BOTH, expand=True)

# starter programmet
root.mainloop()