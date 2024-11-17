import tkinter as tk

class Search(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#121212")

        self.results_frame = tk.Frame(self, bg="#121212")
        self.results_frame.pack(fill="both", expand=True)

    def display_results(self, results):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        artist_label = tk.Label(self.results_frame, text="Artists", bg="#121212", fg="white", font=("Arial", 16))
        artist_label.pack(anchor="w", padx=10, pady=(10, 5))
        for artist in results.get("artists", []):
            tk.Label(self.results_frame, text=artist["nombre"], bg="#121212", fg="white").pack(anchor="w", padx=20)

        song_label = tk.Label(self.results_frame, text="Songs", bg="#121212", fg="white", font=("Arial", 16))
        song_label.pack(anchor="w", padx=10, pady=(10, 5))
        for song in results.get("songs", []):
            tk.Label(self.results_frame, text=song["titulo"], bg="#121212", fg="white").pack(anchor="w", padx=20)

        playlist_label = tk.Label(self.results_frame, text="Playlists", bg="#121212", fg="white", font=("Arial", 16))
        playlist_label.pack(anchor="w", padx=10, pady=(10, 5))
        for playlist in results.get("playlists", []):
            tk.Label(self.results_frame, text=playlist["titulo"], bg="#121212", fg="white").pack(anchor="w", padx=20)