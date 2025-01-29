import sqlite3
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk, PhotoImage, simpledialog, messagebox, END


# Variables globales
EMISIONES_TRANSPORTE = {'coche': 0.120, 'avion': 0.255, 'bus': 0.045}
EMISIONES_ELECTRICIDAD = 0.233
EMISIONES_RESIDUOS = 0.8

# Configurar la base de datos SQLite
base = sqlite3.connect('huella_carbono3.0.db')
cursor = base.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    gasto_transporte REAL,
    gasto_electricidad REAL,
    gasto_residuos REAL,
    huella_total REAL NOT NULL
)
''')
base.commit()

def obtener_nombre_por_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Por favor, di tu nombre...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        nombre = recognizer.recognize_google(audio, language="es-ES")
        print("Has dicho: " + nombre)
        return nombre
    except sr.UnknownValueError:
        print("No se pudo entender lo que dijiste.")
        return None
    except sr.RequestError:
        print("No se pudo conectar al servicio de reconocimiento de voz.")
        return None

def calcular_huella_carbono(transporte, electricidad, residuos):
    huella_transporte = sum(EMISIONES_TRANSPORTE[modo] * km for modo, km in transporte.items() if modo in EMISIONES_TRANSPORTE)
    huella_electricidad = electricidad * EMISIONES_ELECTRICIDAD
    huella_residuos = residuos * EMISIONES_RESIDUOS

    return huella_transporte, huella_electricidad, huella_residuos

def obtener_datos_usuario():
    nombre_usuario = obtener_nombre_por_voz()
    if not nombre_usuario:
        messagebox.showwarning("Advertencia", "No se obtuvo un nombre válido.")
        return

    transporte = {}

    def obtener_numero(prompt):
        while True:
            entrada = simpledialog.askstring("Input", prompt)
            if entrada is None:
                messagebox.showwarning("Advertencia", "No has puesto un valor.")
                return None
            try:
                return float(entrada)
            except ValueError:
                messagebox.showwarning("Advertencia", "Por favor, ingresa un número válido.")

    transporte['coche'] = obtener_numero("¿Cuántos km viajas en coche al mes?")
    if transporte['coche'] is None: return

    transporte['avion'] = obtener_numero("¿Cuántos km viajas en avión al mes?")
    if transporte['avion'] is None: return

    transporte['bus'] = obtener_numero("¿Cuántos km viajas en bus al mes?")
    if transporte['bus'] is None: return

    electricidad = obtener_numero("¿Cuántos kWh gastas al mes?")
    if electricidad is None: return

    residuos = obtener_numero("¿Cuántos kg generas de basura al mes?")
    if residuos is None: return

    huella_transporte, huella_electricidad, huella_residuos = calcular_huella_carbono(transporte, electricidad, residuos)
    huella_total = huella_transporte + huella_electricidad + huella_residuos

    registrar_usuario(nombre_usuario, huella_transporte, huella_electricidad, huella_residuos, huella_total)
    mostrar_resultados(huella_total, nombre_usuario)

def mostrar_resultados(huella_total, nombre_usuario):
    cajaTexto1.config(state="normal")  # Habilitar la caja de texto para mostrar resultados
    cajaTexto1.delete("1.0", END)
    cajaTexto1.insert(END, f"\nHola {nombre_usuario}, tu huella de carbono total al mes es de {huella_total:.2f} kg CO2 equivalentes.\n")
    cajaTexto1.insert(END, "Sugerencias para reducir tu huella de carbono:\n")
    if huella_total > 90:
        cajaTexto1.insert(END, "- Considera usar más transporte público o bicicleta.\n")
        cajaTexto1.insert(END, "- Reduce tu consumo energético y revisa tus electrodomésticos.\n")
        cajaTexto1.insert(END, "- Separa mejor los residuos reciclables.\n")
    else:
        cajaTexto1.insert(END, "- ¡Buen trabajo! Sigue reduciendo tu huella.\n")
    cajaTexto1.config(state="disabled")  # Volver a deshabilitar la caja después de mostrar los resultados

def abrir_ventana_principal():
    global cajaTexto1, tabla
    
    ventanaPrincipal = tk.Toplevel()
    ventanaPrincipal.geometry("925x600")
    ventanaPrincipal.title("Calculadora de emisiones")
    ventanaPrincipal.configure(bg="#f0fff0")

    frame1 = tk.Frame(ventanaPrincipal, bg="#d0f0c0", padx=10, pady=10)
    frame1.grid(row=0, column=0, padx=10, pady=10)

    etiqueta1 = tk.Label(frame1, text="Calculadora de emisiones:", font=("Arial", 14, "bold"), fg="#006400", bg="#d0f0c0")
    etiqueta1.grid(row=0, column=0, pady=5)

    boton1 = tk.Button(frame1, text="CALCULAR", font=("Arial", 12), bg="#90EE90", fg="black", command=obtener_datos_usuario)
    boton1.grid(row=1, column=0, pady=10)

    frame2 = tk.Frame(ventanaPrincipal, bg="#f0fff0", padx=10, pady=10)
    frame2.grid(row=0, column=1, padx=10, pady=10, sticky="n")
    
    cajaTexto1 = tk.Text(frame2, height=10, width=40, bg="#ffffff", fg="#006400", font=("Arial", 10), wrap="word", relief="solid", borderwidth=1)
    cajaTexto1.grid(row=0, column=0)
    cajaTexto1.config(state="disabled")  # Establecer la caja como no editable al principio

    frame_tabla = tk.Frame(ventanaPrincipal, bg="#f0fff0", padx=10, pady=10)
    frame_tabla.grid(row=1, column=0, columnspan=2, pady=10)

    tabla = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Transporte", "Electricidad", "Residuos", "Huella Total"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Transporte", text="Gasto Transporte")
    tabla.heading("Electricidad", text="Gasto Electricidad")
    tabla.heading("Residuos", text="Gasto Residuos")
    tabla.heading("Huella Total", text="Huella Total")

    for col in ("ID", "Nombre", "Transporte", "Electricidad", "Residuos", "Huella Total"):
        tabla.column(col, width=150, anchor="center")
        
    tabla.grid(row=0, column=0)
    
    cargar_usuarios_en_tabla()

    frame_botones = tk.Frame(ventanaPrincipal, bg="#f0fff0", padx=10, pady=10)
    frame_botones.grid(row=2, column=0, columnspan=2, pady=10)

    boton_borrar = tk.Button(frame_botones, text="BORRAR", font=("Arial", 12), bg="#FF4500", fg="white", command=borrar_usuario_seleccionado)
    boton_borrar.grid(row=0, column=0, padx=10)

def registrar_usuario(nombre, huella_transporte, huella_electricidad, huella_residuos, huella_total):
    cursor.execute('''
    INSERT INTO usuarios (nombre, gasto_transporte, gasto_electricidad, gasto_residuos, huella_total)
    VALUES (?, ?, ?, ?, ?)
    ''', (nombre, huella_transporte, huella_electricidad, huella_residuos, huella_total))
    base.commit()
    cargar_usuarios_en_tabla()

def cargar_usuarios_en_tabla():
    for item in tabla.get_children():
        tabla.delete(item)
    cursor.execute('SELECT * FROM usuarios')
    for fila in cursor.fetchall():
        tabla.insert("", "end", values=fila)

def borrar_usuario_seleccionado():
    selected_item = tabla.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un usuario para borrar.")
        return

    valores = tabla.item(selected_item, "values")
    usuario_id = valores[0]
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (usuario_id,))
    base.commit()

    cargar_usuarios_en_tabla()

ventana = tk.Tk()
ventana.title("Calculadora pantalla de inicio")
ventana.geometry("800x600")
ventana.configure(bg="white")

titulo = tk.Label(ventana, text="Calculadora de Huella de Carbono", font=("Arial", 24, "bold"), fg="#228B22", bg="white")
titulo.pack(pady=20)

imagen_path = "huella.png"
imagen = PhotoImage(file=imagen_path)
imagen = imagen.subsample(2, 2)
label_imagen = tk.Label(ventana, image=imagen, bg="white")
label_imagen.pack(pady=20)

boton_inicio = tk.Button(ventana, text="Inicio", font=("Arial", 14), bg="#90EE90", fg="black", padx=20, pady=10, command=abrir_ventana_principal)
boton_inicio.pack(pady=20)

ventana.mainloop()
