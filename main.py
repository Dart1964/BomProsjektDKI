import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator

API_KEY = "f95c9411"


def clear_output():
    # Fjerner alt som vises i output-feltet
    for widget in output_frame.winfo_children():
        widget.destroy()


def show_cast(data):
    # Viser regissør og manusforfatter
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

    # Overskrift for skuespillere
    tk.Label(
        output_frame,
        text="Actors:",
        font=("Arial", 11, "bold")
    ).pack(anchor="w", padx=10, pady=(8, 2))

    # Viser hver skuespiller på egen linje
    for actor in data.get("Actors", "N/A").split(", "):
        tk.Label(
            output_frame,
            text=f"  • {actor}",
            font=("Arial", 11)
        ).pack(anchor="w", padx=20)


def show_movie():
    # Henter informasjon om en film
    clear_output()

    movie = entry.get().strip()

    if not movie:
        messagebox.showerror("Error", "Please enter a movie or series name")
        return

    url = f"http://www.omdbapi.com/?t={movie}&apikey={API_KEY}"
    data = requests.get(url).json()

    # Hvis filmen ikke finnes
    if data.get("Response") == "False":
        messagebox.showerror("Error", data.get("Error"))
        return

    # Viser tittel
    tk.Label(
        output_frame,
        text=f"Title: {data['Title']}",
        font=("Arial", 12)
    ).pack()

    # Overskrift for ratings
    tk.Label(
        output_frame,
        text="Ratings:",
        font=("Arial", 12, "bold")
    ).pack()

    # Viser alle ratings som finnes
    if "Ratings" in data and data["Ratings"]:
        for rating in data["Ratings"]:
            text = f"{rating['Source']} : {rating['Value']}"
            tk.Label(output_frame, text=text).pack()
    else:
        tk.Label(output_frame, text="No ratings available").pack()

    # Viser regissør, writer og skuespillere
    show_cast(data)


def show_series():
    # Henter rating for alle episoder i en serie og viser grafer
    clear_output()

    series = entry.get().strip()

    if not series:
        messagebox.showerror("Error", "Please enter a movie or series name")
        return

    url = f"http://www.omdbapi.com/?t={series}&apikey={API_KEY}"
    data = requests.get(url).json()

    # Hvis serien ikke finnes
    if data.get("Response") == "False":
        messagebox.showerror("Error", data.get("Error"))
        return

    # Sjekker at det faktisk er en serie
    if "totalSeasons" not in data:
        messagebox.showerror("Error", "Not a series")
        return

    # Viser info om serien
    show_cast(data)

    total_seasons = int(data["totalSeasons"])
    episode_numbers = []   # x-akse
    ratings = []           # y-akse
    episode_counter = 1    # teller episoder fortløpende

    # Går gjennom alle sesonger
    for season in range(1, total_seasons + 1):
        season_url = f"http://www.omdbapi.com/?t={series}&Season={season}&apikey={API_KEY}"
        season_data = requests.get(season_url).json()

        # Hopper over hvis sesongen ikke har episoder
        if "Episodes" not in season_data:
            continue

        # Går gjennom alle episodene i sesongen
        for ep in season_data["Episodes"]:
            rating = ep["imdbRating"]

            # Tar bare med episoder som har rating
            if rating != "N/A":
                episode_numbers.append(episode_counter)
                ratings.append(float(rating))

            episode_counter += 1

    # Hvis ingen ratings ble funnet
    if not ratings:
        messagebox.showerror("Error", "No ratings found")
        return

    root.geometry("950x1000")  # større vindu så grafene får bedre plass

    # Lager to grafer under hverandre
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9))

    total_episodes = len(episode_numbers)

    num_ticks = 10
    step = max(1, total_episodes // num_ticks)
    x_ticks = list(range(1, total_episodes + 1, step))

    if x_ticks[-1] != total_episodes:
        x_ticks.append(total_episodes)

    # -------- Linjegraf --------
    ax1.plot(episode_numbers, ratings, marker="o", linestyle="-")
    ax1.set_xlabel("Episode Number", labelpad=10)
    ax1.set_ylabel("IMDb Rating")
    ax1.set_title(f"{series} - Line Plot", pad=12)
    ax1.set_ylim(0, 10)
    ax1.set_yticks(range(0, 11, 1))  # bare hele tall fra 0 til 10
    ax1.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))
    ax1.tick_params(axis="x", rotation=0)

    # -------- Stolpediagram --------
    ax2.bar(episode_numbers, ratings, color="skyblue")
    ax2.set_xlabel("Episode Number", labelpad=10)
    ax2.set_ylabel("IMDb Rating")
    ax2.set_title(f"{series} - Bar Chart", pad=12)
    ax2.set_ylim(0, 10)
    ax2.set_yticks(range(0, 11, 1))  # bare hele tall fra 0 til 10
    ax2.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))
    ax2.tick_params(axis="x", rotation=0)

    # Mer luft mellom grafene
    fig.subplots_adjust(hspace=0.35)

    # Viser grafen inne i tkinter-vinduet
    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# ---------------- GUI ----------------

root = tk.Tk()
root.title("Movie / Series Rating Viewer")

title = tk.Label(root, text="Enter Movie or Series Name", font=("Arial", 14))
title.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

movie_button = tk.Button(button_frame, text="Movie Ratings", command=show_movie)
movie_button.grid(row=0, column=0, padx=10)

series_button = tk.Button(button_frame, text="Series Graph", command=show_series)
series_button.grid(row=0, column=1, padx=10)

output_frame = tk.Frame(root)
output_frame.pack(pady=20, fill=tk.BOTH, expand=True)

root.mainloop()