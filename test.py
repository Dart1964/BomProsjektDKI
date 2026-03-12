import tkinter as tk          # tkinter er Pythons innebygde bibliotek for å lage vinduer
from tkinter import messagebox  # messagebox brukes til å vise feilmeldinger i pop-up vinduer
import requests
import matplotlib.pyplot as plt

API_KEY = "f95c9411"


def clear_output():
    # Fjerner alle widgets som vises i output_frame
    for widget in output_frame.winfo_children():  # hent alle barn-widgets i rammen
        widget.destroy()  # slett widgeten fra skjermen


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

    # figsize=(bredde, høyde) i tommer — bestemmer størrelsen på grafvinduet
    plt.figure(figsize=(10, 9))

    # subplot(rader, kolonner, indeks) — deler figuren i et rutenett
    plt.subplot(2, 1, 1)  # øverste graf
    plt.plot(episode_numbers, ratings, marker='o', linestyle='-')
    plt.xlabel("Episode Number")
    plt.ylabel("IMDb Rating")
    plt.title(f"{series} - Line Plot")
    plt.ylim(0, 10.1)
    plt.yticks([i * 0.5 for i in range(21)])
    step = max(1, len(episode_numbers) // 20)  # maks ~20 labels på x-aksen
    plt.xticks(range(1, len(episode_numbers) + 1, step), rotation=45)

    plt.subplot(2, 1, 2)  # nederste graf
    plt.bar(episode_numbers, ratings, color='skyblue')
    plt.xlabel("Episode Number")
    plt.ylabel("IMDb Rating")
    plt.title(f"{series} - Bar Chart")
    plt.ylim(0, 10.1)
    plt.yticks([i * 0.5 for i in range(21)])
    plt.xticks(range(1, len(episode_numbers) + 1, step), rotation=45)

    plt.tight_layout()  # juster mellomrom så grafene ikke overlapper
    plt.show()          # åpne grafvinduet


# ── Oppsett av GUI ────────────────────────────────────────────────────────────

root = tk.Tk()                              # lag hovedvinduet
root.title("Movie / Series Rating Viewer")  # tekst i tittelbaren
root.geometry("500x400")                    # størrelse på vinduet i piksler (bredde x høyde)

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