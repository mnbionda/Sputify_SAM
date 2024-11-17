import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import random

class HomeView(tk.Frame):
    def __init__(self, parent, db, player, app):
        super().__init__(parent, bg="#121212")
        self.db = db
        self.player = player
        self.app = app

        self.display_artists()
        self.display_songs()
        self.display_genres()

    def round_image(self, image_path, size=(150, 150), radius=10):
        img = Image.open(image_path).resize(size, Image.LANCZOS)
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + size, radius, fill=255)

        rounded_img = Image.new("RGBA", size)
        rounded_img.paste(img, (0, 0), mask)

        return ImageTk.PhotoImage(rounded_img)

    def display_artists(self):
        artists = self.db.get_artistas()
        section_label = tk.Label(self, text="Popular Artists", bg="#121212", fg="#b3b3b3", font=("Arial", 16, "bold"))
        section_label.pack(anchor="w", padx=20, pady=10)

        artist_frame = tk.Frame(self, bg="#121212")
        artist_frame.pack(anchor="w", padx=20)

        for artist in artists:
            artist_card = tk.Canvas(artist_frame, width=150, height=150, bg="#181818", highlightthickness=0)
            artist_card.pack(side="left", padx=10, pady=10)

            artist_image = self.round_image(artist["imagen"])
            artist_card.create_image(0, 0, anchor="nw", image=artist_image)
            artist_card.image = artist_image

            artist_card.create_text(75, 130, text=artist["nombre"], fill="black", font=("Arial", 12, "bold"), anchor="center")
            artist_card.bind("<Button-1>", lambda e, a=artist: self.app.change_view("ArtistPage", a))

    def display_songs(self):
        songs = self.db.get_canciones()
        section_label = tk.Label(self, text="Trending Songs", bg="#121212", fg="#b3b3b3", font=("Arial", 16, "bold"))
        section_label.pack(anchor="w", padx=20, pady=10)

        song_frame = tk.Frame(self, bg="#121212")
        song_frame.pack(anchor="w", padx=20)

        for song in songs:
            song_card = tk.Canvas(song_frame, width=150, height=150, bg="#181818", highlightthickness=0)
            song_card.pack(side="left", padx=10, pady=10)

            song_image = self.round_image(song["imagen"])
            song_card.create_image(0, 0, anchor="nw", image=song_image)
            song_card.image = song_image

            song_card.create_text(75, 130, text=song["titulo"], fill="black", font=("Arial", 12, "bold"), anchor="center")
            song_card.bind("<Button-1>", lambda e, s=song: self.player.play_song(s["source"]))

            
    def display_genres(self):
        genres = self.db.get_genero()
        section_label = tk.Label(self, text="Genres", bg="#121212", fg="#b3b3b3", font=("Arial", 16, "bold"))
        section_label.pack(anchor="w", padx=20, pady=10)

        genre_frame = tk.Frame(self, bg="#121212")
        genre_frame.pack(anchor="w", padx=20)

        colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A6", "#FFDB33", "#33FFDB"]

        for i, genre in enumerate(genres):
            color = random.choice(colors)
            genre_card = tk.Canvas(genre_frame, width=150, height=150, bg=color, highlightthickness=0)
            genre_card.pack(side="left", padx=10, pady=10)

            genre_card.create_text(75, 75, text=genre["nombre"], fill="black", font=("Arial", 12, "bold"), anchor="center")
            genre_card.bind("<Button-1>", lambda e, g=genre: self.app.change_view("GenrePage", g))