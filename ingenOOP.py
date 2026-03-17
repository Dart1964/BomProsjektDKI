import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator


class OMDbClient:
    """Klasse som håndterer all kommunikasjon med OMDb API"""

    def __init__(self, api_key):
        self.api_key = api_key

    def search_movie(self, title):
        url = f"http://www.omdbapi.com/?s={title}&type=movie&apikey={self.api_key}"
        return requests.get(url).json()

    def search_series(self, title):
        url = f"http://www.omdbapi.com/?s={title}&type=series&apikey={self.api_key}"
        return requests.get(url).json()

    def get_by_id(self, imdb_id):
        url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={self.api_key}"
        return requests.get(url).json()

    def get_season(self, imdb_id, season):
        url = f"http://www.omdbapi.com/?i={imdb_id}&Season={season}&apikey={self.api_key}"
        return requests.get(url).json()


class GraphGenerator:
    """Klasse som lager grafer"""

    def create_episode_graph(self, title, episode_numbers, ratings):

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9))

        ax1.plot(
            episode_numbers,
            ratings,
            marker="o",
            markersize=3,
            linewidth=1
        )
        ax1.set_xlabel("Episode Number")
        ax1.set_ylabel("IMDb Rating")
        ax1.set_title(f"{title} - Line Plot")
        ax1.set_ylim(0, 10)
        ax1.set_yticks(range(0, 11, 1))
        ax1.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))

        ax2.bar(episode_numbers, ratings, color="skyblue")
        ax2.set_xlabel("Episode Number")
        ax2.set_ylabel("IMDb Rating")
        ax2.set_title(f"{title} - Bar Chart")
        ax2.set_ylim(0, 10)
        ax2.set_yticks(range(0, 11, 1))
        ax2.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))

        fig.subplots_adjust(hspace=0.35)

        return fig


class MovieApp:
    """Hovedklassen som styrer GUI og programlogikken"""

    def __init__(self, root):

        self.root = root
        self.root.title("Movie / Series Rating Viewer")

        self.api = OMDbClient("f95c9411")
        self.graph = GraphGenerator()

        self.create_gui()

    def create_gui(self):

        title = tk.Label(
            self.root,
            text="Enter Movie or Series Name",
            font=("Arial", 14)
        )
        title.pack(pady=10)

        self.entry = tk.Entry(self.root, width=30)
        self.entry.pack(pady=5)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        movie_button = tk.Button(
            button_frame,
            text="Movie Ratings",
            command=self.show_movie
        )
        movie_button.grid(row=0, column=0, padx=10)

        series_button = tk.Button(
            button_frame,
            text="Series Graph",
            command=self.show_series
        )
        series_button.grid(row=0, column=1, padx=10)

        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    def clear_output(self):
        for widget in self.output_frame.winfo_children():
            widget.destroy()

    def show_cast(self, data):

        tk.Label(
            self.output_frame,
            text="Director: " + data.get("Director", "N/A"),
            font=("Arial", 11, "italic"),
            fg="#444"
        ).pack(anchor="w", padx=10)

        tk.Label(
            self.output_frame,
            text="Writer: " + data.get("Writer", "N/A"),
            font=("Arial", 11, "italic"),
            fg="#444"
        ).pack(anchor="w", padx=10)

        tk.Label(
            self.output_frame,
            text="Actors:",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=10, pady=(8, 2))

        for actor in data.get("Actors", "N/A").split(", "):
            tk.Label(
                self.output_frame,
                text=f"  • {actor}",
                font=("Arial", 11)
            ).pack(anchor="w", padx=20)

    def show_movie(self):

        self.clear_output()

        movie = self.entry.get().strip()

        if not movie:
            messagebox.showerror("Error", "Write a movie name")
            return

        data = self.api.search_movie(movie)

        if data.get("Response") == "False":
            messagebox.showerror("Error", data.get("Error"))
            return

        results = data["Search"]

        if len(results) == 1:
            self.show_movie_by_id(results[0]["imdbID"])
        else:
            self.choose_title(results, self.show_movie_by_id)

    def show_movie_by_id(self, imdb_id):

        self.clear_output()

        data = self.api.get_by_id(imdb_id)

        if data.get("Response") == "False":
            messagebox.showerror("Error", data.get("Error"))
            return

        tk.Label(
            self.output_frame,
            text=f"Title: {data['Title']} ({data.get('Year', 'N/A')})",
            font=("Arial", 12, "bold")
        ).pack()

        tk.Label(
            self.output_frame,
            text=f"Type: {data.get('Type', 'N/A')}",
            font=("Arial", 11)
        ).pack()

        tk.Label(
            self.output_frame,
            text="Ratings:",
            font=("Arial", 12, "bold")
        ).pack(pady=(8, 2))

        if "Ratings" in data and data["Ratings"]:
            for rating in data["Ratings"]:
                text = f"{rating['Source']} : {rating['Value']}"
                tk.Label(self.output_frame, text=text).pack()
        else:
            tk.Label(self.output_frame, text="No ratings available").pack()

        self.show_cast(data)

    def show_series(self):

        self.clear_output()

        series = self.entry.get().strip()

        if not series:
            messagebox.showerror("Error", "Write a series name")
            return

        data = self.api.search_series(series)

        if data.get("Response") == "False":
            messagebox.showerror("Error", data.get("Error"))
            return

        results = data["Search"]

        if len(results) == 1:
            self.show_series_by_id(results[0]["imdbID"])
        else:
            self.choose_title(results, self.show_series_by_id)

    def show_series_by_id(self, imdb_id):

        self.clear_output()

        data = self.api.get_by_id(imdb_id)

        if data.get("Response") == "False":
            messagebox.showerror("Error", data.get("Error"))
            return

        if "totalSeasons" not in data:
            messagebox.showerror("Error", "Not a series")
            return

        self.show_cast(data)

        total_seasons = int(data["totalSeasons"])

        episode_numbers = []
        ratings = []
        episode_counter = 1

        for season in range(1, total_seasons + 1):

            season_data = self.api.get_season(imdb_id, season)

            if "Episodes" not in season_data:
                continue

            for ep in season_data["Episodes"]:

                rating = ep["imdbRating"]

                if rating != "N/A":
                    episode_numbers.append(episode_counter)
                    ratings.append(float(rating))

                episode_counter += 1

        if not ratings:
            messagebox.showerror("Error", "No ratings found")
            return

        fig = self.graph.create_episode_graph(
            data["Title"],
            episode_numbers,
            ratings
        )

        canvas = FigureCanvasTkAgg(fig, master=self.output_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def choose_title(self, results, callback):

        select_window = tk.Toplevel(self.root)
        select_window.title("Choose Title")
        select_window.geometry("500x350")

        tk.Label(
            select_window,
            text="Choose the correct title",
            font=("Arial", 11, "bold")
        ).pack(pady=8)

        listbox = tk.Listbox(select_window, width=65, height=12)
        listbox.pack(padx=10, pady=10)

        for item in results:

            title = item.get("Title", "Unknown")
            year = item.get("Year", "")
            item_type = item.get("Type", "")

            listbox.insert(
                tk.END,
                f"{title} ({year}) - {item_type}"
            )

        def select_item():

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


root = tk.Tk()

app = MovieApp(root)

root.mainloop()