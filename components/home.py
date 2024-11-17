import tkinter as tk

class HomeView(tk.Frame):
    def __init__(self, parent, db, player, app):
        super().__init__(parent, bg="#121212")
        self.db = db
        self.player = player
        self.app = app 

        self.header_label = tk.Label(self, text="Discover", bg="#121212", fg="white", font=("Arial", 24, "bold"))
        self.header_label.pack(anchor="w", padx=20, pady=20)

        self.display_artists()
        self.display_songs()
        self.display_genres()

    def display_artists(self):
        artists = self.db.get_artistas()
        artist_label = tk.Label(self, text="Popular Artists", bg="#121212", fg="#b3b3b3", font=("Arial", 16, "bold"))
        artist_label.pack(anchor="w", padx=20, pady=10)
        for artista in artists:
            btn = tk.Button(
                self, text=artista["nombre"], bg="#181818", fg="white", font=("Arial", 12), bd=0,
                activebackground="#1DB954", activeforeground="white",
                padx=10, pady=5, relief="flat",
                command=lambda a=artista: self.app.change_view("ArtistPage", a) 
            )
            btn.pack(anchor="w", padx=30, pady=2)

    def display_songs(self):
        songs = self.db.get_canciones()
        song_label = tk.Label(self, text="Trending Songs", bg="#121212", fg="#b3b3b3", font=("Arial", 16, "bold"))
        song_label.pack(anchor="w", padx=20, pady=10)
        for song in songs:
            btn = tk.Button(
                self, text=song["titulo"], bg="#181818", fg="white", font=("Arial", 12), bd=0,
                activebackground="#1DB954", activeforeground="white",
                padx=10, pady=5, relief="flat",
                command=lambda s=song: self.play_song(s["source"])
            )
            btn.pack(anchor="w", padx=30, pady=2)

    def display_genres(self):
        genres = self.db.get_genero()
        genre_label = tk.Label(self, text="Genres", bg="#121212", fg="#b3b3b3", font=("Arial", 16, "bold"))
        genre_label.pack(anchor="w", padx=20, pady=10)
        for genre in genres:
            btn = tk.Button(
                self, text=genre["nombre"], bg="#181818", fg="white", font=("Arial", 12), bd=0,
                activebackground="#1DB954", activeforeground="white",
                padx=10, pady=5, relief="flat",
                command=lambda g=genre: self.app.change_view("GenrePage", g)
            )
            btn.pack(anchor="w", padx=30, pady=2)

    def play_song(self, song_path):
        self.player.play_song(song_path)