import tkinter as tk

class Library(tk.Frame):
    def __init__(self, parent, db, player, app, user):
        super().__init__(parent, bg="#121212")
        self.db = db
        self.player = player
        self.app = app
        self.user = user
        self.playlists = self.db.get_playlists_usuarios(self.user) + self.db.get_playlists_seguidas(self.user)

        header_frame = tk.Frame(self, bg="#121212")
        header_frame.pack(fill="x", padx=20, pady=(20, 12))

        playlist_label = tk.Label(header_frame, text="Playlists", bg="#121212", fg="white",
                                  font=("Arial", 24, "bold"))
        playlist_label.pack(side="left")

        self.display_playlists()

    def display_playlists(self):
        for playlist in self.playlists:
            btn = tk.Button(
                self, text=playlist["titulo"], bg="#181818", fg="white", font=("Arial", 12), bd=0,
                activebackground="#1DB954", activeforeground="white",
                padx=10, pady=5, relief="flat", command=lambda p=playlist: self.app.change_view("Playlist", p)
            )
            btn.pack(anchor="w", padx=20, pady=2)

    def show_playlist(self, playlist):
        print(f"Showing playlist: {playlist['titulo']}")
