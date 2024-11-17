import tkinter as tk
from components.manage import Manage

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
        button_widgets = []
        albums = self.db.get_albumes_artist(self.artist["artista_id"])
        for album in albums:
            album_frame = tk.Frame(self, bg="#121212")
            album_frame.pack(anchor="w", fill="x", pady=5)

            album_label = tk.Label(album_frame, text=album["titulo"], bg="#121212", fg="#b3b3b3", font=("Arial", 16))
            album_label.pack(anchor="w", padx=30)

            songs = self.db.get_canciones_album(album["album_id"])
            for song in songs:
                control_frame = tk.Frame(album_frame, bg="#282828")
                control_frame.pack(fill="x", padx=30, pady=2)
                
                song_btn = tk.Button(
                    control_frame, text=song["titulo"], bg="#282828", fg="white", font=("Arial", 12), bd=0,
                    activebackground="#1DB954", activeforeground="white",
                    padx=30, pady=5, relief="flat", command=lambda s=song: self.player.play_song(s, songs)
                )
                song_btn.pack(side="left", anchor="w")
                button_widgets.append(song_btn)

                add_btn = tk.Button(control_frame, text="➕", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                                    activebackground="#1DB954", activeforeground="white", command=lambda s=song: Manage(self, self.db, s))
                add_btn.pack(side="right", anchor="e", padx=(10, 0))
                button_widgets.append(add_btn)

        for song_btn in button_widgets:
            song_btn.bind("<Enter>", lambda e, b=song_btn: b.config(bg="#1DB954"))
            song_btn.bind("<Leave>", lambda e, b=song_btn: b.config(bg="#282828"))