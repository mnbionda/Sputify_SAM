import tkinter as tk
from tkinter import messagebox

class Registro:
    def __init__(self, root, cambiar_a_login, db):
        self.root = root
        self.root.geometry("500x450")
        self.cambiar_a_login = cambiar_a_login
        self.db = db

        self.crear_interfaz_registro()

    def crear_interfaz_registro(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Crea tu cuenta de Sputify", bg="#121212", fg="#1DB954", font=("Arial", 24, "bold")).pack(pady=(20, 10))

        tk.Label(self.root, text="Nombre:", bg="#121212", fg="#FFFFFF", font=("Arial", 14)).pack(pady=(20, 5))
        self.entry_nombre = tk.Entry(self.root, width=35, font=("Arial", 14), bg="#FFFFFF", fg="#000000", bd=0, insertbackground="#808080")
        self.entry_nombre.pack(pady=5, ipady=5)

        tk.Label(self.root, text="Email:", bg="#121212", fg="#FFFFFF", font=("Arial", 14)).pack(pady=5)
        self.entry_email = tk.Entry(self.root, width=35, font=("Arial", 14), bg="#FFFFFF", fg="#000000", bd=0, insertbackground="#808080")
        self.entry_email.pack(pady=5, ipady=5)

        tk.Label(self.root, text="Contraseña:", bg="#121212", fg="#FFFFFF", font=("Arial", 14)).pack(pady=5)
        self.entry_password = tk.Entry(self.root, show="*", width=35, font=("Arial", 14), bg="#FFFFFF", fg="#000000", bd=0, insertbackground="#808080")
        self.entry_password.pack(pady=5, ipady=5)

        tk.Button(self.root, text="Registrar", command=self.registrar_usuario, bg="#1DB954", fg="#FFFFFF", font=("Arial", 14), bd=0, padx=10, pady=5).pack(pady=(20, 5))

        tk.Button(self.root, text="¿Ya tienes cuenta? Inicia Sesión", command=self.cambiar_a_login, bg="#121212", fg="#1DB954", font=("Arial", 12), bd=0).pack(pady=(10, 5))

    def registrar_usuario(self):
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        
        if not nombre or not email or not password:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
            return

        try:
            self.db.registrar_usuario(nombre, email, password)
            self.cambiar_a_login()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")
