import tkinter as tk
from tkinter import messagebox

class Create(tk.Frame):
    def __init__(self, parent, db, user):
        super().__init__(parent)
        self.user = user
        self.db = db

        self.create_window = tk.Toplevel(parent)
        self.create_window.title("Create Playlist")
        self.create_window.geometry("300x200")
        self.create_window.config(bg="#121212")

        self.label = tk.Label(self.create_window, text="Playlist title", bg="#121212", fg="white", font=("Arial", 14))
        self.label.pack(pady=10)

        self.title_entry = tk.Entry(self.create_window, font=("Arial", 12), width=25)
        self.title_entry.pack(pady=10)

        self.create_button = tk.Button(
            self.create_window, text="Create", font=("Arial", 12), bg="#1DB954",
            fg="white", activebackground="#1DB954", activeforeground="white",
            command=self.create_playlist
        )
        self.create_button.pack(pady=20)

    def create_playlist(self):
        title = self.title_entry.get().strip()

        if not title:
            messagebox.showwarning("Error", "Por favor ingrese un nombre para la playlist.")
            return

        playlist_id = self.db.crear_playlist(title, self.user)
        
        if playlist_id:
            messagebox.showinfo("Exiro", f"Playlist '{title}' creada!")
            self.create_window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear la playlist.")
