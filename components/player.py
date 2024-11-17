import tkinter as tk
from components.manage import Manage
from PIL import Image, ImageTk
import pygame
import os

class Player(tk.Frame):
    def __init__(self, parent, db, user):
        super().__init__(parent, bg="#282828", height=100)
        pygame.mixer.init()

        self.is_playing = False
        self.current_song_path = None
        self.song_length = 0
        self.current_time = 0
        self.image_label = None
        self.current_song = None
        self.db = db
        self.user = user
        self.songs = []
        self.current_song_index = 0

        self.album_cover = tk.Label(self, bg="#282828")
        self.album_cover.pack(side="left", padx=(10, 20))

        self.song_info = tk.Label(self, text="", bg="#282828", fg="white", font=("Arial", 14, "bold"))
        self.song_info.pack(side="left", padx=10)

        control_frame = tk.Frame(self, bg="#282828")
        control_frame.pack(side="left", padx=20)
        
        self.prev_btn = tk.Button(control_frame, text="⏮", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                                  activebackground="#1DB954", activeforeground="white", command=self.prev_song)
        self.prev_btn.pack(side="left", padx=10)
        
        self.play_pause_btn = tk.Button(control_frame, text="▶", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                                        activebackground="#1DB954", activeforeground="white", command=self.toggle_play_pause)
        self.play_pause_btn.pack(side="left", padx=10)
        
        self.next_btn = tk.Button(control_frame, text="⏭", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                                  activebackground="#1DB954", activeforeground="white", command=self.next_song)
        self.next_btn.pack(side="left", padx=10)

        self.add_btn = tk.Button(control_frame, text="➕", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                                  activebackground="#1DB954", activeforeground="white", command=self.add_song)
        self.add_btn.pack(side="left", padx=10)

        self.volume_slider = tk.Scale(self, from_=0, to=100, orient="horizontal", bg="#282828", fg="white",
                                      troughcolor="#1DB954", highlightthickness=0, command=self.set_volume, length=100)
        self.volume_slider.set(50)
        self.volume_slider.pack(side="right", padx=20, pady=(0, 19))

        self.progress_frame = tk.Frame(self, bg="#282828")
        self.progress_frame.pack(side="right", padx=20)
        
        self.current_time_label = tk.Label(self.progress_frame, text="0:00", bg="#282828", fg="white", font=("Arial", 10))
        self.current_time_label.pack(side="left", pady=(19, 19))

        self.progress = tk.Scale(self.progress_frame, from_=0, to=100, orient="horizontal", length=500, bg="#282828",
                                 troughcolor="#1DB954", highlightthickness=0, command=self.seek_song, fg="#282828")
        self.progress.pack(side="left", padx=5, pady=(0, 19))
        
        self.song_length_label = tk.Label(self.progress_frame, text="0:00", bg="#282828", fg="white", font=("Arial", 10))
        self.song_length_label.pack(side="left", padx=(0, 50), pady=(19, 19))

    def play_song(self, song, songs):
        self.current_song = song
        self.songs = songs
        self.current_song_index = songs.index(song)

        if os.path.exists(song["source"]):
            self.current_song_path = song["source"]
            pygame.mixer.music.load(song["source"])
            pygame.mixer.music.play()

            song_title = os.path.basename(song["titulo"])
            self.song_info.config(text=song_title)

            self.song_length = pygame.mixer.Sound(song["source"]).get_length()
            self.song_length_label.config(text=self.format_time(self.song_length))
            self.current_time = 0
            self.is_playing = True
            self.play_pause_btn.config(text="⏸")
            self.update_progress()

            if "imagen" in song and os.path.exists(song["imagen"]):
                self.load_album_cover(song["imagen"])
            else:
                self.clear_album_cover()

    def load_album_cover(self, image_path):
        img = Image.open(image_path)
        img = img.resize((50, 50), Image.LANCZOS)
        self.album_cover_img = ImageTk.PhotoImage(img)
        self.album_cover.config(image=self.album_cover_img)

    def clear_album_cover(self):
        self.album_cover.config(image='')

    def toggle_play_pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_pause_btn.config(text="▶")
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.play_pause_btn.config(text="⏸")

    def update_progress(self):
        if self.is_playing and self.current_song_path:
            self.current_time += 1
            if self.current_time <= self.song_length:
                self.progress.set((self.current_time / self.song_length) * 100)
                self.current_time_label.config(text=self.format_time(self.current_time))
                self.after(1000, self.update_progress)
            else:
                self.is_playing = False
                self.play_pause_btn.config(text="▶")
                self.progress.set(0)
                self.current_time_label.config(text="0:00")
                self.next_song()

    def seek_song(self, position):
        if self.current_song_path and self.song_length > 0:
            new_time = int((self.progress.get() / 100) * self.song_length)
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(new_time)
            self.current_time = new_time
            self.current_time_label.config(text=self.format_time(new_time))

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume) / 100)

    def prev_song(self):
        if self.songs:
            self.current_song_index = (self.current_song_index - 1) % len(self.songs)
            self.play_song(self.songs[self.current_song_index], self.songs)

    def next_song(self):
        if self.songs:
            self.current_song_index = (self.current_song_index + 1) % len(self.songs)
            self.play_song(self.songs[self.current_song_index], self.songs)

    def add_song(self):
        if not self.current_song_path:
            return
        
        Manage(self, self.db, self.current_song, self.user["id_usuario"])

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02}"