import tkinter as tk
# tkinter brukes til å lage vinduer, knapper og tekstfelt

from tkinter import messagebox
# messagebox brukes til å vise feilmeldinger i små popup-vinduer

import requests
# requests brukes til å hente data fra internett (API)

import matplotlib.pyplot as plt
# matplotlib brukes til å lage grafer

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# gjør at matplotlib-grafer kan vises inni tkinter-vinduet

from matplotlib.ticker import MaxNLocator
# lager pene og jevnt fordelte tall på aksene i grafen


API_KEY = "f95c9411"
# nøkkel som gir tilgang til OMDb film-databasen


def clear_output():
    # sletter alt som vises i resultatområdet
    for widget in output_frame.winfo_children():
        # finner alle elementer inni rammen
        widget.destroy()
        # fjerner elementet fra skjermen


def show_cast(data):
    # viser regissør og manusforfatter

    tk.Label(
        output_frame,
        text="Director: " + data.get("Director", "N/A"),
        font=("Arial", 11, "italic"),
        fg="#444"
    ).pack(anchor="w", padx=10)

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

    actors_text = data.get("Actors", "N/A")

    # deler opp skuespillerlisten
    for actor in actors_text.split(", "):
        tk.Label(
            output_frame,
            text=f"  • {actor}",
            font=("Arial", 11)
        ).pack(anchor="w", padx=20)


def show_movie_by_id(imdb_id):
    # viser en bestemt film ved hjelp av imdb id

    clear_output()

    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={API_KEY}"
    data = requests.get(url).json()

    # hvis filmen ikke finnes
    if data.get("Response") == "False":
        messagebox.showerror("Error", data.get("Error"))
        return

    # viser tittel
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

    # overskrift for vurderinger
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

    show_cast(data)


def choose_title(results, callback):
    # åpner et lite vindu der brukeren kan velge riktig film/serie

    select_window = tk.Toplevel(root)
    select_window.title("Choose Title")
    select_window.geometry("500x350")

    tk.Label(
        select_window,
        text="Choose the correct title",
        font=("Arial", 11, "bold")
    ).pack(pady=8)

    listbox = tk.Listbox(select_window, width=65, height=12)
    listbox.pack(padx=10, pady=10)

    # legger filmer inn i listen
    for item in results:
        title = item.get("Title", "Unknown")
        year = item.get("Year", "")
        item_type = item.get("Type", "")

        listbox.insert(tk.END, f"{title} ({year}) - {item_type}")

    def select_item():
        # kjøres når brukeren trykker "Select"

        selected = listbox.curselection()

        if not selected:
            messagebox.showerror("Error", "Choose a title")
            return

        imdb_id = results[selected[0]]["imdbID"]

        select_window.destroy()

        callback(imdb_id)

    tk.Button(
        select_window,
        text="Select",
        command=select_item
    ).pack(pady=8)


def show_movie():
    # søker etter filmer med dette navnet

    clear_output()

    movie = entry.get().strip()

    if not movie:
        messagebox.showerror("Error", "Write a movie name")
        return

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
        choose_title(results, show_movie_by_id)


def show_series():
    # søker etter serier

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


def show_series_by_id(imdb_id):
    # lager grafer for alle episoder i en serie

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

        # går gjennom episodene
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

    # lager figur (graf-vindu)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9))
    # fig = hele graf-området
    # ax1 og ax2 = grafene inni figuren

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
    # lager mer plass mellom grafene

    # viser grafen i tkinter
    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# -------- GUI --------

root = tk.Tk()
# lager hovedvinduet

root.title("Movie / Series Rating Viewer")

title = tk.Label(
    root,
    text="Enter Movie or Series Name",
    font=("Arial", 14)
)
title.pack(pady=10)

entry = tk.Entry(root, width=30)
# tekstfelt der brukeren skriver navn

entry.pack(pady=5)

button_frame = tk.Frame(root)
# ramme som holder knappene

button_frame.pack(pady=10)

movie_button = tk.Button(
    button_frame,
    text="Movie Ratings",
    command=show_movie
)
movie_button.grid(row=0, column=0, padx=10)

series_button = tk.Button(
    button_frame,
    text="Series Graph",
    command=show_series
)
series_button.grid(row=0, column=1, padx=10)

output_frame = tk.Frame(root)
# område der resultater og grafer vises

output_frame.pack(pady=20, fill=tk.BOTH, expand=True)

root.mainloop()
# holder programmet i gang
# programmet stopper når vinduet lukkesss