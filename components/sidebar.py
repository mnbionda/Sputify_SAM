import tkinter as tk

class Sidebar(tk.Frame):
    def __init__(self, parent, change_view_callback):
        super().__init__(parent, bg="#121212", width=250)
        self.change_view_callback = change_view_callback
        self.current_view_name = "Home"


        self.search_var = tk.StringVar() 

        self.buttons = [
            ("Home", "Home"),
            ("Library", "Library"),
            ("Liked Songs", "Liked Songs"),
            ("Create Playlist", "Create Playlist"),
            ("Search", "Search")
        ]
        
        self.button_widgets = []
        for text, view_name in self.buttons:
            btn = tk.Button(
                self,
                text=text,
                bg="#121212",
                fg="white",
                font=("Arial", 14, "bold"),
                bd=0,
                activebackground="#1DB954",
                activeforeground="white",
                command=lambda vn=view_name: self.handle_sidebar_click(vn)
            )
            btn.pack(fill="x", pady=8, padx=20, anchor="w")
            self.button_widgets.append(btn)

        self.search_entry = tk.Entry(
            self, textvariable=self.search_var, font=("Arial", 14),
            bg="#1DB954", fg="white", insertbackground="white", width=13
        )
        self.search_entry.bind("<KeyRelease>", self.perform_search)

        for btn in self.button_widgets:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1DB954"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#121212"))
            
    def handle_sidebar_click(self, view_name):
        if view_name == "Search":
            self.show_search_entry()
        else:
            self.change_view_callback(view_name)

    def show_search_entry(self):
        self.button_widgets[4].pack_forget()
        self.search_entry.pack(fill="x", pady=8, padx=20, anchor="w")
        self.search_entry.focus()

    def perform_search(self, event):
        query = self.search_var.get()
        if query.strip():
            self.change_view_callback("Search", query)
        else:
            self.change_view_callback("LastNonSearchView")
            
    def reset_search(self):
        self.search_var.set("")
        self.search_entry.pack_forget()
        self.button_widgets[4].pack(fill="x", pady=8, padx=20, anchor="w")