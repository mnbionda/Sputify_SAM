import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from components.manage import Manage

class Artist(tk.Frame):
    def __init__(self, parent, artist, db, player, app, user):
        super().__init__(parent, bg="#121212")
        self.artist = artist
        self.db = db
        self.player = player
        self.app = app
        self.user = user

        self.create_artist_header()

        self.display_albums()

    def create_artist_header(self):
        header_frame = tk.Frame(self, bg="#121212")
        header_frame.pack(fill="x", pady=20, padx=10)

        img = Image.open(self.artist['imagen'])
        img = img.resize((120, 120), Image.LANCZOS)
        
        mask = Image.new("L", (120, 120), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + (120, 120), 10, fill=255)
        rounded_img = Image.new("RGBA", (120, 120))
        rounded_img.paste(img, (0, 0), mask)

        artist_image = ImageTk.PhotoImage(rounded_img)

        if artist_image:
            image_label = tk.Label(header_frame, image=artist_image, bg="#121212")
            image_label.image = artist_image
            image_label.pack(side="left", padx=20)

        artist_label = tk.Label(header_frame, text=f"{self.artist['nombre']}", bg="#121212", fg="white", font=("Arial", 24, "bold"))
        artist_label.pack(side="left", padx=10)

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
                    padx=30, pady=5, relief="flat", command=lambda s=song, album_songs=songs: self.player.play_song(s, album_songs)
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