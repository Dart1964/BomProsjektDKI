import tkinter as tk          # tkinter er Pythons innebygde bibliotek for å lage vinduer
from tkinter import messagebox  # messagebox brukes til å vise feilmeldinger i pop-up vinduer
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

API_KEY = "f95c9411"


def clear_output():
    # Fjerner alle widgets som vises i output_frame
    for widget in output_frame.winfo_children():  # hent alle barn-widgets i rammen
        widget.destroy()  # slett widgeten fra skjermen

def show_cast(data):
    tk.Label(output_frame, text="Director: " + data.get("Director", "N/A"), font=("Arial", 11, "italic"), fg="#444").pack(anchor="w", padx=10)
    tk.Label(output_frame, text="Writer: " + data.get("Writer", "N/A"), font=("Arial", 11, "italic"), fg="#444").pack(anchor="w", padx=10)

    tk.Label(output_frame, text="Actors:", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(8, 2))
    for actor in data.get("Actors", "N/A").split(", "):
        tk.Label(output_frame, text=f"  • {actor}", font=("Arial", 11)).pack(anchor="w", padx=20)


def show_movie():
    # Henter filmdata fra OMDB og viser tittel + vurderinger
    clear_output()

    movie = entry.get()  # les teksten brukeren har skrevet inn

    url = f"http://www.omdbapi.com/?t={movie}&apikey={API_KEY}"
    data = requests.get(url).json()

    if data.get("Response") == "False":
        messagebox.showerror("Error", data.get("Error"))  # vis feilmelding i pop-up
        return

    # tk.Label viser tekst på skjermen
    # .pack() plasserer widgeten i vinduet, stablet ovenfra og ned
    tk.Label(output_frame, text=f"Title: {data['Title']}", font=("Arial", 12)).pack()
    tk.Label(output_frame, text="Ratings:", font=("Arial", 12, "bold")).pack()

    if "Ratings" in data:
        for rating in data["Ratings"]:
            text = f"{rating['Source']} : {rating['Value']}"
            tk.Label(output_frame, text=text).pack()
    else:
        tk.Label(output_frame, text="No ratings available").pack()
    show_cast(data)


def show_series():
    # Henter vurderinger for alle episoder i en serie og viser dem som graf
    clear_output()

    series = entry.get()

    url = f"http://www.omdbapi.com/?t={series}&apikey={API_KEY}"
    data = requests.get(url).json()

    if data.get("Response") == "False":
        messagebox.showerror("Error", data.get("Error"))
        return

    if "totalSeasons" not in data:
        messagebox.showerror("Error", "Not a series")
        return

    show_cast(data)

    total_seasons = int(data["totalSeasons"])
    episode_numbers = []  # episodenummer på x-aksen
    ratings = []          # vurderinger på y-aksen

    episode_counter = 1   # teller episoder på tvers av sesonger

    for season in range(1, total_seasons + 1):
        season_url = f"http://www.omdbapi.com/?t={series}&Season={season}&apikey={API_KEY}"
        season_data = requests.get(season_url).json()

        for ep in season_data["Episodes"]:
            rating = ep["imdbRating"]
            if rating != "N/A":  # hopp over episoder uten vurdering
                episode_numbers.append(episode_counter)
                ratings.append(float(rating))
            episode_counter += 1

    if not ratings:
        messagebox.showerror("Error", "No ratings found")
        return


    root.geometry("800x900")
    # figsize=(bredde, høyde) i tommer — bestemmer størrelsen på grafvinduet
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

    step = max(1, len(episode_numbers) // 20)

    ax1.plot(episode_numbers, ratings, marker='o', linestyle='-')
    ax1.set_xlabel("Episode Number")
    ax1.set_ylabel("IMDb Rating")
    ax1.set_title(f"{series} - Line Plot")
    ax1.set_ylim(0, 10.1)
    ax1.set_yticks([i * 0.5 for i in range(21)])
    ax1.set_xticks(range(1, len(episode_numbers) + 1, step))
    ax1.tick_params(axis='x', rotation=45)

    ax2.bar(episode_numbers, ratings, color='skyblue')
    ax2.set_xlabel("Episode Number")
    ax2.set_ylabel("IMDb Rating")
    ax2.set_title(f"{series} - Bar Chart")
    ax2.set_ylim(0, 10.1)
    ax2.set_yticks([i * 0.5 for i in range(21)])
    ax2.set_xticks(range(1, len(episode_numbers) + 1, step))
    ax2.tick_params(axis='x', rotation=45)

    fig.tight_layout()

    # Embed the figure into the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# ── Oppsett av GUI ────────────────────────────────────────────────────────────

root = tk.Tk()                              # lag hovedvinduet
root.title("Movie / Series Rating Viewer")  # tekst i tittelbaren

title = tk.Label(root, text="Enter Movie or Series Name", font=("Arial", 14))
title.pack(pady=10)  # pady legger til vertikal luft rundt widgeten

entry = tk.Entry(root, width=30)  # tekstfelt der brukeren skriver inn navn
entry.pack(pady=5)

# Frame er en usynlig boks som brukes til å gruppere widgets
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# command= er funksjonen som kjøres når knappen trykkes
movie_button = tk.Button(button_frame, text="Movie Ratings", command=show_movie)
movie_button.grid(row=0, column=0, padx=10)  # grid() plasserer widgets i rader og kolonner

series_button = tk.Button(button_frame, text="Series Graph", command=show_series)
series_button.grid(row=0, column=1, padx=10)

output_frame = tk.Frame(root)  # tom ramme som fylles med resultater når brukeren søker
output_frame.pack(pady=20)

# mainloop() holder vinduet åpent og lytter etter klikk og tastetrykk
root.mainloop()