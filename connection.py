import mysql.connector
from mysql.connector import Error
from tkinter import messagebox


class DBConnection:
    def __init__(self):
        try:
            self.db_conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="Sputify"
            )
            self.cursor = self.db_conexion.cursor(dictionary=True)
        except Error as err:
            messagebox.showerror("DB Error", f"Error de conexion a base de datos: {err}")
            exit()

    def cerrar_conexion(self):
        self.cursor.close()
        self.db_conexion.close()

    def login(self, email, password):
        query = "SELECT * FROM usuario WHERE mail = %s AND pass = %s"
        self.cursor.execute(query, (email, password))
        return self.cursor.fetchone()

    def registrar_usuario(self, name, email, password):
        query = "INSERT INTO usuario (nombre, mail, pass) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (name, email, password))
        self.db_conexion.commit()
        return self.cursor.lastrowid

    def get_playlists_usuarios(self, user_id):
        query = "SELECT * FROM playlist WHERE id_usuario = %s"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def get_artistas(self):
        query = "SELECT * FROM artista"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def buscar_artistas(self, artist_name):
        query = "SELECT * FROM artista WHERE nombre LIKE %s"
        self.cursor.execute(query, (f"%{artist_name}%",))
        return self.cursor.fetchall()

    def get_albumes_artist(self, artist_id):
        query = "SELECT * FROM album WHERE artista_id = %s"
        self.cursor.execute(query, (artist_id,))
        return self.cursor.fetchall()

    def get_canciones(self):
        query = "SELECT * FROM cancion"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def buscar_canciones(self, song_title):
        query = "SELECT * FROM cancion WHERE titulo LIKE %s"
        self.cursor.execute(query, (f"%{song_title}%",))
        return self.cursor.fetchall()

    def get_canciones_album(self, album_id):
        query = "SELECT * FROM cancion WHERE album_id = %s"
        self.cursor.execute(query, (album_id,))
        return self.cursor.fetchall()

    def get_canciones_artista(self, artist_id):
        query = """
            SELECT c.* FROM cancion AS c
            JOIN cancion_pertenece_artista AS ca ON c.id_cancion = ca.id_cancion
            WHERE ca.artista_id = %s
        """
        self.cursor.execute(query, (artist_id,))
        return self.cursor.fetchall()

    def get_playlists(self):
        query = "SELECT * FROM playlist"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def buscar_playlists_title(self, title):
        query = "SELECT * FROM playlist WHERE titulo LIKE %s"
        self.cursor.execute(query, (f"%{title}%",))
        return self.cursor.fetchall()

    def get_canciones_playlist(self, playlist_id):
        query = """
            SELECT c.* FROM cancion AS c
            JOIN cancion_dentro_playlist AS cp ON c.id_cancion = cp.id_cancion
            WHERE cp.playlist_id = %s
        """
        self.cursor.execute(query, (playlist_id,))
        return self.cursor.fetchall()

    def add_cancion_playlist(self, playlist_id, song_id):
        query = "INSERT INTO cancion_dentro_playlist (playlist_id, id_cancion, fecha_agregada) VALUES (%s, %s, NOW())"
        self.cursor.execute(query, (playlist_id, song_id))
        self.db_conexion.commit()

    def get_canciones_favoritas(self, user_id):
        query = """
            SELECT c.* FROM cancion AS c
            JOIN cancion_dentro_playlist AS cp ON c.id_cancion = cp.id_cancion
            JOIN usuario AS u ON cp.playlist_id = u.favoritas_playlist_id
            WHERE u.id_usuario = %s
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def add_cancion_favoritos(self, user_id, song_id):
        query = "SELECT favoritas_playlist_id FROM usuario WHERE id_usuario = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        if result and result["favoritas_playlist_id"]:
            playlist_id = result["favoritas_playlist_id"]
            self.add_cancion_playlist(playlist_id, song_id)

    def get_genero(self):
        query = "SELECT * FROM genero"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_songs_genero(self, genre_id):
        query = "SELECT * FROM cancion WHERE genero_id = %s"
        self.cursor.execute(query, (genre_id,))
        return self.cursor.fetchall()

    def seguir_playlist(self, user_id, playlist_id):
        query = "INSERT INTO usuario_sigue_playlist (playlist_id, id_usuario, fecha_seguida) VALUES (%s, %s, NOW())"
        self.cursor.execute(query, (playlist_id, user_id))
        self.db_conexion.commit()

    def get_playlists_seguidas(self, user_id):
        query = """
            SELECT p.* FROM playlist AS p
            JOIN usuario_sigue_playlist AS usp ON p.playlist_id = usp.playlist_id
            WHERE usp.id_usuario = %s
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def buscar(self, busqueda):
        resultados = {
            "artists": self.buscar_artistas(busqueda),
            "songs": self.buscar_canciones(busqueda),
            "playlists": self.buscar_playlists_title(busqueda)
        }
        return resultados