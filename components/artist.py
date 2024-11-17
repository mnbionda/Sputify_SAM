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

        self.canvas = tk.Canvas(self, bg="#121212", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#121212")

        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", tags="scrollable_frame")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind("<Configure>", self.resize_canvas)

        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.create_artist_header()
        self.display_albums()

    def update_scroll_region(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        scrollable_height = self.canvas.bbox("all")[3]
        visible_height = self.canvas.winfo_height()

        if scrollable_height <= visible_height:
            self.canvas.unbind_all("<MouseWheel>")
            self.scrollbar.pack_forget()
        else:
            self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
            self.scrollbar.pack(side="right", fill="y")

    def resize_canvas(self, event=None):
        canvas_width = event.width
        self.canvas.itemconfig("scrollable_frame", width=canvas_width)

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def create_artist_header(self):
        header_frame = tk.Frame(self.scrollable_frame, bg="#121212")
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
            album_frame = tk.Frame(self.scrollable_frame, bg="#121212")
            album_frame.pack(anchor="w", fill="x", pady=5)

            album_label = tk.Label(album_frame, text=album["titulo"], bg="#121212", fg="#b3b3b3", font=("Arial", 16))
            album_label.pack(anchor="w", padx=30)

            songs = self.db.get_canciones_album(album["album_id"])
            for song in songs:
                control_frame = tk.Frame(album_frame, bg="#282828")
                control_frame.pack(fill="x", padx=30, pady=2)

                song_btn = tk.Button(
                    control_frame, text=song["titulo"], bg="#282828", fg="white", font=("Arial", 12), bd=0,
                    activebackground="#1DB954", activeforeground="white", anchor="w",
                    padx=30, pady=5, relief="flat", command=lambda s=song, album_songs=songs: self.player.play_song(s, album_songs)
                )
                song_btn.pack(side="left", anchor="w", fill="x", expand=True)
                button_widgets.append(song_btn)

                add_btn = tk.Button(control_frame, text="➕", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                                    activebackground="#1DB954", activeforeground="white", command=lambda s=song: Manage(self, self.db, s, self.user))
                add_btn.pack(side="right", anchor="e", padx=(10, 0))
                button_widgets.append(add_btn)

        for song_btn in button_widgets:
            song_btn.bind("<Enter>", lambda e, b=song_btn: b.config(bg="#1DB954"))
            song_btn.bind("<Leave>", lambda e, b=song_btn: b.config(bg="#282828"))
