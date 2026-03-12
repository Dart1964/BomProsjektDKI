import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt

API_KEY = "f95c9411"


def clear_output():
    for widget in output_frame.winfo_children():
        widget.destroy()


def show_movie():
    clear_output()

    movie = entry.get()

    url = f"http://www.omdbapi.com/?t={movie}&apikey={API_KEY}"
    data = requests.get(url).json()

    if data.get("Response") == "False":
        messagebox.showerror("Error", data.get("Error"))
        return

    tk.Label(output_frame, text=f"Title: {data['Title']}", font=("Arial", 12)).pack()

    tk.Label(output_frame, text="Ratings:", font=("Arial", 12, "bold")).pack()

    if "Ratings" in data:
        for rating in data["Ratings"]:
            text = f"{rating['Source']} : {rating['Value']}"
            tk.Label(output_frame, text=text).pack()
    else:
        tk.Label(output_frame, text="No ratings available").pack()


def show_series():
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

    episode_numbers = []
    ratings = []

    episode_counter = 1

    for season in range(1, total_seasons + 1):
        season_url = f"http://www.omdbapi.com/?t={series}&Season={season}&apikey={API_KEY}"
        season_data = requests.get(season_url).json()

        for ep in season_data["Episodes"]:
            rating = ep["imdbRating"]
            if rating != "N/A":
                episode_numbers.append(episode_counter)
                ratings.append(float(rating))
            episode_counter += 1

    if not ratings:
        messagebox.showerror("Error", "No ratings found")
        return

    # --- Create figure with 2 subplots ---
    plt.figure(figsize=(10,9))

    # Line plot
    plt.subplot(2,1,1)
    plt.plot(episode_numbers, ratings, marker='o', linestyle='-')
    plt.xlabel("Episode Number")
    plt.ylabel("IMDb Rating")
    plt.title(f"{series} - Line Plot")
    plt.ylim(0, 10.1)
    plt.yticks([i*0.5 for i in range(21)])
    step = max(1, len(episode_numbers)//20)
    plt.xticks(range(1, len(episode_numbers)+1, step), rotation=45)

    # Bar plot
    plt.subplot(2,1,2)
    plt.bar(episode_numbers, ratings, color='skyblue')
    plt.xlabel("Episode Number")
    plt.ylabel("IMDb Rating")
    plt.title(f"{series} - Bar Chart")
    plt.ylim(0, 10.1)
    plt.yticks([i*0.5 for i in range(21)])
    plt.xticks(range(1, len(episode_numbers)+1, step), rotation=45)

    plt.tight_layout()
    plt.show()


# GUI
root = tk.Tk()
root.title("Movie / Series Rating Viewer")
root.geometry("500x400")

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
output_frame.pack(pady=20)

root.mainloop()