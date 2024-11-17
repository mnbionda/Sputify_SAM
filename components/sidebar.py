import tkinter as tk

class Sidebar(tk.Frame):
    def __init__(self, parent, change_view_callback):
        super().__init__(parent, bg="#121212", width=250)
        self.change_view_callback = change_view_callback

        buttons = [
            ("Home", "Home"),
            ("Search", "Search"),
            ("Library", "Library"),
            ("Create Playlist", "Create Playlist"),
            ("Liked Songs", "Liked Songs")
        ]

        for text, view_name in buttons:
            btn = tk.Button(
                self,
                text=text,
                bg="#121212",
                fg="white",
                font=("Arial", 14, "bold"),
                bd=0,
                activebackground="#1DB954",
                activeforeground="white",
                command=lambda vn=view_name: self.change_view(vn)
            )
            btn.pack(fill="x", pady=8, padx=20, anchor="w")

            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1DB954"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#121212"))

    def change_view(self, view_name):
        self.change_view_callback(view_name)