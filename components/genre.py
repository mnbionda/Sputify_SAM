import tkinter as tk
from components.manage import Manage

class Genre(tk.Frame):
    def __init__(self, parent, genre, db, player, app, user):
        super().__init__(parent, bg="#121212")
        self.genre = genre
        self.player = player
        self.db = db
        self.app = app
        self.user = user

        self.album_frame = tk.Frame(self, bg="#121212")
        self.album_frame.pack(anchor="w", fill="x", pady=5)

        genre_label = tk.Label(self.album_frame, text=f"{genre['nombre']}", bg="#121212", fg="white", font=("Arial", 24, "bold"))
        genre_label.pack(pady=20)

        self.display_songs()

    def display_songs(self):
        button_widgets = []
        songs = self.db.get_songs_genero(self.genre["genero_id"])
        for song in songs:
            control_frame = tk.Frame(self.album_frame, bg="#282828")
            control_frame.pack(fill="x", padx=30, pady=2)
            
            song_btn = tk.Button(
                control_frame, text=song["titulo"], bg="#282828", fg="white", font=("Arial", 12), bd=0,
                activebackground="#1DB954", activeforeground="white",
                padx=30, pady=5, relief="flat", command=lambda s=song: self.player.play_song(s, songs)
            )
            song_btn.pack(side="left", anchor="w")
            button_widgets.append(song_btn)

            add_btn = tk.Button(control_frame, text="➕", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                                activebackground="#1DB954", activeforeground="white", command=lambda s=song: Manage(self, self.db, s, self.user))
            add_btn.pack(side="right", anchor="e", padx=(10, 0))
            button_widgets.append(add_btn)

        for song_btn in button_widgets:
            song_btn.bind("<Enter>", lambda e, b=song_btn: b.config(bg="#1DB954"))
            song_btn.bind("<Leave>", lambda e, b=song_btn: b.config(bg="#282828"))