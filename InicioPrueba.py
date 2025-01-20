import tkinter as tk
from tkinter import PhotoImage

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de Huella de Carbono")
ventana.geometry("800x600")
ventana.configure(bg="white")

# Título
titulo = tk.Label(ventana, text="Calculadora de Huella de Carbono", font=("Arial", 24, "bold"), fg="#228B22", bg="white")
titulo.pack(pady=20)

# Imagen
imagen_path = "huella.png"  # Cambia la imagen a formato PNG
try:
    imagen = PhotoImage(file=imagen_path)
    imagen = imagen.subsample(2, 2)  # Hacer la imagen 5 veces más grande
    label_imagen = tk.Label(ventana, image=imagen, bg="white")
    label_imagen.pack(pady=20)
except Exception as e:
    label_error = tk.Label(ventana, text=f"Error al cargar la imagen: {e}", fg="red", bg="white")
    label_error.pack(pady=20)

# Botón de inicio
boton_inicio = tk.Button(ventana, text="INICIO", font=("Arial", 14), bg="#90EE90", fg="white", padx=20, pady=10)
boton_inicio.pack(pady=20)

# Ejecutar ventana
ventana.mainloop()
