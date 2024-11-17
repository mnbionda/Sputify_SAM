import tkinter as tk

class Library(tk.Frame):
    def __init__(self, parent, db, player, app, user):
        super().__init__(parent, bg="#121212")
        self.db = db
        self.player = player
        self.app = app
        self.user = user
        self.playlists = self.db.get_playlists_usuarios(self.user) + self.db.get_playlists_seguidas(self.user)

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

        header_frame = tk.Frame(self.scrollable_frame, bg="#121212")
        header_frame.pack(fill="x", padx=20, pady=(20, 12))

        playlist_label = tk.Label(header_frame, text="Playlists", bg="#121212", fg="white",
                                  font=("Arial", 24, "bold"))
        playlist_label.pack(side="left")

        self.display_playlists()

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

    def display_playlists(self):
        button_widgets = []
        for playlist in self.playlists:
            control_frame = tk.Frame(self.scrollable_frame, bg="#282828")
            control_frame.pack(fill="x", padx=30, pady=2)
            
            btn = tk.Button(
                control_frame, text=playlist["titulo"], bg="#282828", fg="white", font=("Arial", 12), bd=0,
                activebackground="#1DB954", activeforeground="white", anchor="w",
                padx=10, pady=5, relief="flat", command=lambda p=playlist: self.app.change_view("Playlist", p)
            )
            btn.pack(side="left", anchor="w", fill="x", expand=True)
            button_widgets.append(btn)

            if self.user == playlist["id_usuario"]:
                remove_btn = tk.Button(
                    control_frame, text="➖", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                    activebackground="#1DB954", activeforeground="white",
                    command=lambda p=playlist: self.remove_playlist(p)
                )
                remove_btn.pack(side="right", anchor="e", padx=(10, 0))
                button_widgets.append(remove_btn)
        
        for song_btn in button_widgets:
            song_btn.bind("<Enter>", lambda e, b=song_btn: b.config(bg="#1DB954"))
            song_btn.bind("<Leave>", lambda e, b=song_btn: b.config(bg="#282828"))

    def remove_playlist(self, playlist):
        self.db.eliminar_playlist(playlist["playlist_id"])
        self.app.change_view("Library")