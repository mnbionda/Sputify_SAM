import tkinter as tk
from components.manage import Manage

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
        button_widgets = []
        songs = self.db.get_canciones_playlist(self.playlist["playlist_id"])
        for song in songs:
            control_frame = tk.Frame(self, bg="#282828")
            control_frame.pack(fill="x", padx=30, pady=2)

            song_btn = tk.Button(
                    control_frame, text=song["titulo"], bg="#282828", fg="white", font=("Arial", 12), bd=0,
                    activebackground="#1DB954", activeforeground="white",
                    padx=30, pady=5, relief="flat", command=lambda s=song: self.player.play_song(s)
                )
            song_btn.pack(side="left", anchor="w")
            button_widgets.append(song_btn)

            remove_btn = tk.Button(control_frame, text="➖", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                                activebackground="#1DB954", activeforeground="white", 
                                command=lambda s=song: self.remove_song_from_playlist(s))
            remove_btn.pack(side="right", anchor="e", padx=(10, 0))
            button_widgets.append(remove_btn)

            add_btn = tk.Button(control_frame, text="➕", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                                activebackground="#1DB954", activeforeground="white", command=lambda s=song: Manage(self, self.db, s))
            add_btn.pack(side="right", anchor="e", padx=(10, 0))
            button_widgets.append(add_btn)

        for song_btn in button_widgets:
            song_btn.bind("<Enter>", lambda e, b=song_btn: b.config(bg="#1DB954"))
            song_btn.bind("<Leave>", lambda e, b=song_btn: b.config(bg="#282828"))

    def remove_song_from_playlist(self, song):
        self.db.sacar_cancion_playlist(self.playlist["playlist_id"], song["id_cancion"])

        self.app.change_view("Playlist", self.playlist)