import tkinter as tk

class Playlist(tk.Frame):
    def __init__(self, parent, playlist, db, player, app):
        super().__init__(parent, bg="#121212")
        self.playlist = playlist
        self.db = db
        self.player = player
        self.app = app

        playlist_label = tk.Label(self, text=f"{playlist['titulo']}", bg="#121212", fg="white", font=("Arial", 24, "bold"))
        playlist_label.pack(pady=20)

        self.display_songs()

    def display_songs(self):
        songs = self.db.get_canciones_playlist(self.playlist["playlist_id"])
        for song in songs:
            song_label = tk.Label(self, text=song["titulo"], bg="#121212", fg="#b3b3b3", font=("Arial", 16))
            song_label.pack(anchor="w", padx=20, pady=5)