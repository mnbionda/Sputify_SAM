import tkinter as tk
from tkinter import messagebox

class Login:
    def __init__(self, root, cambiar_a_registro, logged, db):
        self.root = root
        self.root.geometry("500x400")
        self.cambiar_a_registro = cambiar_a_registro
        self.logged = logged
        self.db = db

        self.crear_interfaz_login()

    def crear_interfaz_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Bienvenido a Sputify", bg="#121212", fg="#1DB954", font=("Arial", 24, "bold")).pack(pady=(20, 10))

        tk.Label(self.root, text="Email:", bg="#121212", fg="#FFFFFF", font=("Arial", 14)).pack(pady=(20, 5))
        self.entry_email = tk.Entry(self.root, width=35, font=("Arial", 14), bg="#FFFFFF", fg="#000000", bd=0, insertbackground="#808080")
        self.entry_email.pack(pady=5, ipady=5)

        tk.Label(self.root, text="Contraseña:", bg="#121212", fg="#FFFFFF", font=("Arial", 14)).pack(pady=5)
        self.entry_password = tk.Entry(self.root, show="*", width=35, font=("Arial", 14), bg="#FFFFFF", fg="#000000", bd=0, insertbackground="#808080")
        self.entry_password.pack(pady=5, ipady=5)

        tk.Button(self.root, text="Iniciar Sesión", command=self.iniciar_sesion, bg="#1DB954", fg="#FFFFFF", font=("Arial", 14), bd=0, padx=10, pady=5).pack(pady=(20, 5))
        
        tk.Button(self.root, text="¿No tienes cuenta? Regístrate", command=self.cambiar_a_registro, bg="#121212", fg="#1DB954", font=("Arial", 12), bd=0).pack(pady=(10, 5))

    def iniciar_sesion(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        
        if not email or not password:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
            return

        user = self.db.login(email, password)
        if user:
            self.logged(user)
        else:
            messagebox.showerror("Error", "Email o contraseña incorrectos")