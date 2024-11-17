import tkinter as tk
from components.login import Login
from components.register import Registro
from components.sidebar import Sidebar
from components.player import Player
from components.home import Home
from components.search import Search
from components.library import Library
from components.artist import Artist
from components.genre import Genre
from components.playlist import Playlist
from connection import DBConnection


class SputifyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sputify")
        self.configure(bg="#121212")

        self.db = DBConnection()
        self.user = None

        self.show_login()

    def show_login(self):
        Login(self, self.show_register, self.on_login, self.db)

    def show_register(self):
        Registro(self, self.show_login, self.db)

    def on_login(self, user):
        self.user = user

        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("1280x700")
        self.show_main_app()

    def show_main_app(self):
        self.player = Player(self, self.db, self.user)
        self.player.pack(side="bottom", fill="x")

        self.sidebar = Sidebar(self, self.change_view, self.db, self.user)
        self.sidebar.pack(side="left", fill="y")

        self.content_frame = tk.Frame(self, bg="#121212")
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.current_view = None
        self.last_view_name = "Home"
        self.last_view_data = None

        self.change_view("Home")

    def change_view(self, view_name, data=None):
        if view_name == "LastNonSearchView":
            view_name = self.last_view_name
            data = self.last_view_data
        elif view_name != "Search":
            self.last_view_name = view_name
            self.last_view_data = data

        if self.current_view:
            self.current_view.destroy()

        if view_name == "Home":
            self.current_view = Home(self.content_frame, self.db, self.player, self)
        elif view_name == "Search":
            self.current_view = Search(self.content_frame, self.db, self.player, self, self.user["id_usuario"])
            self.current_view.display_results(self.db.buscar(data))
        elif view_name == "Library":
            self.current_view = Library(self.content_frame, self.db, self.player, self, self.user["id_usuario"])
        elif view_name == "Artist":
            self.current_view = Artist(self.content_frame, data, self.db, self.player, self, self.user["id_usuario"])
        elif view_name == "Genre":
            self.current_view = Genre(self.content_frame, data, self.db, self.player, self, self.user["id_usuario"])
        elif view_name == "Playlist":
            self.current_view = Playlist(self.content_frame, data, self.db, self.player, self, self.user["id_usuario"])
        elif view_name == "Liked Songs":
            self.current_view = Playlist(self.content_frame, self.db.get_favorita_usuario(self.user["id_usuario"]),
                                         self.db, self.player, self, self.user["id_usuario"])

        self.current_view.pack(fill="both", expand=True)

        if view_name != "Search":
            self.sidebar.reset_search()


if __name__ == "__main__":
    app = SputifyApp()
    app.mainloop()
