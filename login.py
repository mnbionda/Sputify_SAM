import tkinter as tk
from tkinter import messagebox
from connection import login

def iniciar_sesion():
    email = entry_email.get()
    password = entry_password.get()
   
    if not email or not password:
        messagebox.showwarning("Campos Vacíos", "Por favor, completa todos los espacios.")
        return
    
    user = login(email, password)
    
    if user:
        messagebox.showinfo("Inicio de sesión", f"Bienvenido, {user['nombre']}!")
    else:
        messagebox.showerror("Error", "Email o contraseña incorrectos")

# Configuración de la ventana de inicio de sesión
root = tk.Tk()
root.title("Login")
root.geometry("400x300") 
root.configure(bg="black")

# Estilo
label_email = tk.Label(root, text="Email:", bg="black", fg="#1DB954", font=("Arial", 14))
label_email.pack(pady=(20, 5))

entry_email = tk.Entry(root, width=30, font=("Arial", 14))
entry_email.pack(pady=5)

label_password = tk.Label(root, text="Contraseña:", bg="black", fg="#1DB954", font=("Arial", 14))
label_password.pack(pady=5)

entry_password = tk.Entry(root, show="*", width=30, font=("Arial", 14))
entry_password.pack(pady=5)

button_login = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion, bg="#1DB954", fg="black", font=("Arial", 14))
button_login.pack(pady=(20, 0))

root.mainloop()
