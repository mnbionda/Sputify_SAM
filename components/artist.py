import tkinter as tk

class Artist(tk.Frame):
    def __init__(self, parent, artist, db, player, app):
        super().__init__(parent, bg="#121212")
        self.artist = artist
        self.db = db
        self.player = player
        self.app = app

        artist_label = tk.Label(self, text=f"{artist['nombre']}", bg="#121212", fg="white", font=("Arial", 24, "bold"))
        artist_label.pack(pady=20)

        self.display_albums()

    def display_albums(self):
        albums = self.db.get_albumes_artist(self.artist["artista_id"])
        for album in albums:
            album_label = tk.Label(self, text=album["titulo"], bg="#121212", fg="#b3b3b3", font=("Arial", 16))
            album_label.pack(anchor="w", padx=20, pady=5)
            
            songs = self.db.get_canciones_album(album["album_id"])
            for song in songs:
                song_btn = tk.Button(
                    self, text=song["titulo"], bg="#181818", fg="white", font=("Arial", 12), bd=0,
                    activebackground="#1DB954", activeforeground="white",
                    padx=10, pady=5, relief="flat", command=lambda s=song: self.player.play_song(s)
                )
                song_btn.pack(anchor="w", padx=40, pady=2)