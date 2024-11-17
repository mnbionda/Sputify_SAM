import tkinter as tk
from components.manage import Manage

class Search(tk.Frame):
    def __init__(self, parent, db, player, app):
        super().__init__(parent, bg="#121212")
        self.db = db
        self.player = player
        self.app = app

        self.results_frame = tk.Frame(self, bg="#121212")
        self.results_frame.pack(fill="both", expand=True)

    def display_results(self, results):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        artist_label = tk.Label(self.results_frame, text="Artists", bg="#121212", fg="white", font=("Arial", 16))
        artist_label.pack(anchor="w", padx=10, pady=(10, 5))

        button_widgets = []

        for artist in results.get("artists", []):
            control_frame = tk.Frame(self.results_frame, bg="#282828")
            control_frame.pack(fill="x", padx=30, pady=2)

            artist_btn = tk.Button(
                control_frame, text=artist["nombre"], bg="#282828", fg="white", font=("Arial", 12), bd=0,
                activebackground="#1DB954", activeforeground="white",
                padx=30, pady=5, relief="flat", command=lambda a=artist: self.app.change_view("Artist", a)
            )
            artist_btn.pack(side="left", anchor="w")
            button_widgets.append(artist_btn)

        song_label = tk.Label(self.results_frame, text="Songs", bg="#121212", fg="white", font=("Arial", 16))
        song_label.pack(anchor="w", padx=10, pady=(10, 5))

        for song in results.get("songs", []):
            control_frame = tk.Frame(self.results_frame, bg="#282828")
            control_frame.pack(fill="x", padx=30, pady=2)

            song_btn = tk.Button(
                    control_frame, text=song["titulo"], bg="#282828", fg="white", font=("Arial", 12), bd=0,
                    activebackground="#1DB954", activeforeground="white",
                    padx=30, pady=5, relief="flat", command=lambda s=song: self.player.play_song(s)
                )
            song_btn.pack(side="left", anchor="w")
            button_widgets.append(song_btn)

            add_btn = tk.Button(control_frame, text="➕", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                                activebackground="#1DB954", activeforeground="white", command=lambda s=song: Manage(self, self.db, s))
            add_btn.pack(side="right", anchor="e", padx=(10, 0))
            button_widgets.append(add_btn)

        playlist_label = tk.Label(self.results_frame, text="Playlists", bg="#121212", fg="white", font=("Arial", 16))
        playlist_label.pack(anchor="w", padx=10, pady=(10, 5))

        for playlist in results.get("playlists", []):
            control_frame = tk.Frame(self.results_frame, bg="#282828")
            control_frame.pack(fill="x", padx=30, pady=2)

            artist_btn = tk.Button(
                control_frame, text=playlist["titulo"], bg="#282828", fg="white", font=("Arial", 12), bd=0,
                activebackground="#1DB954", activeforeground="white",
                padx=30, pady=5, relief="flat", command=lambda p=playlist: self.app.change_view("Playlist", p)
            )
            artist_btn.pack(side="left", anchor="w")
            button_widgets.append(artist_btn)

        for song_btn in button_widgets:
            song_btn.bind("<Enter>", lambda e, b=song_btn: b.config(bg="#1DB954"))
            song_btn.bind("<Leave>", lambda e, b=song_btn: b.config(bg="#282828"))