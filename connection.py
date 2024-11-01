import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

try:
    db_conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Sputify"
    )
    cursor = db_conexion.cursor(dictionary=True)
except Error as err:
    messagebox.showerror("DB Error", f"Error de conexion a base de datos: {err}")
    exit()

def cerrar_conexion():
    cursor.close()
    db_conexion.close()


def login(email, password):
    query = "SELECT * FROM usuario WHERE mail = %s AND pass = %s"
    cursor.execute(query, (email, password))
    return cursor.fetchone()

def registrar_usuario(name, email, password):
    query = "INSERT INTO usuario (nombre, mail, pass) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, password))
    db_conexion.commit()
    return cursor.lastrowid

def get_playlists_usuarios(user_id):
    query = "SELECT * FROM playlist WHERE id_usuario = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


def get_artistas():
    query = "SELECT * FROM artista"
    cursor.execute(query)
    return cursor.fetchall()

def buscar_artistas(artist_name):
    query = "SELECT * FROM artista WHERE nombre LIKE %s"
    cursor.execute(query, (f"%{artist_name}%",))
    return cursor.fetchall()

def get_albumes_artist(artist_id):
    query = "SELECT * FROM album WHERE artista_id = %s"
    cursor.execute(query, (artist_id,))
    return cursor.fetchall()


def get_canciones():
    query = "SELECT * FROM cancion"
    cursor.execute(query)
    return cursor.fetchall()

def buscar_canciones(song_title):
    query = "SELECT * FROM cancion WHERE titulo LIKE %s"
    cursor.execute(query, (f"%{song_title}%",))
    return cursor.fetchall()

def get_canciones_album(album_id):
    query = "SELECT * FROM cancion WHERE album_id = %s"
    cursor.execute(query, (album_id,))
    return cursor.fetchall()

def get_canciones_artista(artist_id):
    query = """
        SELECT c.* FROM cancion AS c
        JOIN cancion_pertenece_artista AS ca ON c.id_cancion = ca.id_cancion
        WHERE ca.artista_id = %s
    """
    cursor.execute(query, (artist_id,))
    return cursor.fetchall()


def get_playlists():
    query = "SELECT * FROM playlist"
    cursor.execute(query)
    return cursor.fetchall()

def buscar_playlists_title(title):
    query = "SELECT * FROM playlist WHERE titulo LIKE %s"
    cursor.execute(query, (f"%{title}%",))
    return cursor.fetchall()

def get_canciones_playlist(playlist_id):
    query = """
        SELECT c.* FROM cancion AS c
        JOIN cancion_dentro_playlist AS cp ON c.id_cancion = cp.id_cancion
        WHERE cp.playlist_id = %s
    """
    cursor.execute(query, (playlist_id,))
    return cursor.fetchall()

def add_cancion_playlist(playlist_id, song_id):
    query = "INSERT INTO cancion_dentro_playlist (playlist_id, id_cancion, fecha_agregada) VALUES (%s, %s, NOW())"
    cursor.execute(query, (playlist_id, song_id))
    db_conexion.commit()


def get_canciones_favoritas(user_id):
    query = """
        SELECT c.* FROM cancion AS c
        JOIN cancion_dentro_playlist AS cp ON c.id_cancion = cp.id_cancion
        JOIN usuario AS u ON cp.playlist_id = u.favoritas_playlist_id
        WHERE u.id_usuario = %s
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

def add_cancion_favoritos(user_id, song_id):
    query = "SELECT favoritas_playlist_id FROM usuario WHERE id_usuario = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if result and result["favoritas_playlist_id"]:
        playlist_id = result["favoritas_playlist_id"]
        add_cancion_playlist(playlist_id, song_id)


def get_genero():
    query = "SELECT * FROM genero"
    cursor.execute(query)
    return cursor.fetchall()

def get_songs_genero(genre_id):
    query = "SELECT * FROM cancion WHERE genero_id = %s"
    cursor.execute(query, (genre_id,))
    return cursor.fetchall()



def seguir_playlist(user_id, playlist_id):
    query = "INSERT INTO usuario_sigue_playlist (playlist_id, id_usuario, fecha_seguida) VALUES (%s, %s, NOW())"
    cursor.execute(query, (playlist_id, user_id))
    db_conexion.commit()

def get_playlists_seguidas(user_id):
    query = """
        SELECT p.* FROM playlist AS p
        JOIN usuario_sigue_playlist AS usp ON p.playlist_id = usp.playlist_id
        WHERE usp.id_usuario = %s
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


def buscar(busqueda):
    resultados = {
        "artists": buscar_artistas(busqueda),
        "songs": buscar_canciones(busqueda),
        "playlists": buscar_playlists_title(busqueda)
    }
    return resultados