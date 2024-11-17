import tkinter as tk
from tkinter import ttk
import pygame
import os

class Player(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#282828", height=100)
        pygame.mixer.init()

        self.is_playing = False
        self.current_song_path = None
        self.song_length = 0
        self.current_time = 0

        self.song_info = tk.Label(self, text="", bg="#282828", fg="white", font=("Arial", 14, "bold"))
        self.song_info.pack(side="left", padx=10)

        control_frame = tk.Frame(self, bg="#282828")
        control_frame.pack(side="left", padx=40)
        
        self.prev_btn = tk.Button(control_frame, text="⏮", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                                  activebackground="#1DB954", activeforeground="white", command=self.prev_song)
        self.prev_btn.pack(side="left", padx=10)
        
        self.play_pause_btn = tk.Button(control_frame, text="▶", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                                        activebackground="#1DB954", activeforeground="white", command=self.toggle_play_pause)
        self.play_pause_btn.pack(side="left", padx=10)
        
        self.next_btn = tk.Button(control_frame, text="⏭", font=("Arial", 14), bg="#282828", fg="white", bd=0,
                                  activebackground="#1DB954", activeforeground="white", command=self.next_song)
        self.next_btn.pack(side="left", padx=10)

        self.volume_slider = tk.Scale(self, from_=0, to=100, orient="horizontal", bg="#282828", fg="white",
                                      troughcolor="#1DB954", highlightthickness=0, command=self.set_volume, length=100)
        self.volume_slider.set(50)  # Default volume
        self.volume_slider.pack(side="right", padx=20)

        self.progress_frame = tk.Frame(self, bg="#282828")
        self.progress_frame.pack(side="right", padx=20)
        
        self.current_time_label = tk.Label(self.progress_frame, text="0:00", bg="#282828", fg="white", font=("Arial", 10))
        self.current_time_label.pack(side="left")

        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(side="left", padx=5)
        
        self.song_length_label = tk.Label(self.progress_frame, text="0:00", bg="#282828", fg="white", font=("Arial", 10))
        self.song_length_label.pack(side="left")

    def play_song(self, song):
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
                self.progress["value"] = (self.current_time / self.song_length) * 100
                self.current_time_label.config(text=self.format_time(self.current_time))
                self.after(1000, self.update_progress)
            else:
                self.is_playing = False
                self.play_pause_btn.config(text="▶")
                self.progress["value"] = 0
                self.current_time_label.config(text="0:00")

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume) / 100)

    def prev_song(self):
        print("Previous song")

    def next_song(self):
        print("Next song")

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02}"