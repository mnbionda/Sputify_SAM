import tkinter as tk
from tkinter import messagebox
from connection import registrar_usuario

def registrar():
    name = entry_name.get()
    email = entry_email.get()
    password = entry_password.get()

    if not name or not email or not password:
        messagebox.showwarning("Campos Vacíos", "Por favor, completa todos los espacios.")
        return

    # Registro del nuevo usuario
    try:
        user_id = registrar_usuario(name, email, password)
        messagebox.showinfo("Registro Exitoso", f"Usuario registrado!") 
        # Limpia los campos después del registro
        entry_name.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")

# Configuración de la ventana de registro
root = tk.Tk()
root.title("Registro")
root.geometry("400x400") 
root.configure(bg="black")

# Estilo
label_name = tk.Label(root, text="Nombre:", bg="black", fg="#1DB954", font=("Arial", 14))
label_name.pack(pady=(20, 5))

entry_name = tk.Entry(root, width=30, font=("Arial", 14))
entry_name.pack(pady=5)

label_email = tk.Label(root, text="Email:", bg="black", fg="#1DB954", font=("Arial", 14))
label_email.pack(pady=5)

entry_email = tk.Entry(root, width=30, font=("Arial", 14))
entry_email.pack(pady=5)

label_password = tk.Label(root, text="Contraseña:", bg="black", fg="#1DB954", font=("Arial", 14))
label_password.pack(pady=5)

entry_password = tk.Entry(root, show="*", width=30, font=("Arial", 14))
entry_password.pack(pady=5)

button_register = tk.Button(root, text="Registrar", command=registrar, bg="#1DB954", fg="black", font=("Arial", 14))
button_register.pack(pady=(20, 0))

root.mainloop()
