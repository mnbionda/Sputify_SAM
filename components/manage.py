import tkinter as tk
from tkinter import messagebox

class Manage(tk.Frame):
    def __init__(self, parent, db, song, user):
        super().__init__(parent)
        self.song = song
        self.db = db
        self.user = user

        self.add_song_window = tk.Toplevel(parent)
        self.add_song_window.title("Add Song to Playlist")
        self.add_song_window.geometry("300x400")
        self.add_song_window.config(bg="#121212")

        self.label = tk.Label(self.add_song_window, text="Select a Playlist", bg="#121212", fg="white", font=("Arial", 16))
        self.label.pack(pady=10)

        self.playlists = self.db.get_playlists_usuarios(user)

        for playlist in self.playlists:
            playlist_button = tk.Button(
                self.add_song_window, text=playlist["titulo"], bg="#181818", fg="white", font=("Arial", 12),
                activebackground="#1DB954", activeforeground="white", padx=10, pady=5, relief="flat",
                command=lambda p=playlist: self.add_to_playlist(p, self.add_song_window)
            )
            playlist_button.pack(fill="x", padx=20, pady=5)

    def add_to_playlist(self, playlist, window):
        if self.db.cancion_en_playlist(playlist["playlist_id"], self.song['id_cancion']):
            window.destroy()
        else:
            try:
                self.db.add_cancion_playlist(playlist["playlist_id"], self.song['id_cancion'])
                messagebox.showinfo("Exito", f"Cancion añadida a la playlist '{playlist['titulo']}'!")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No pudo agregarse la cancion: {e}")
