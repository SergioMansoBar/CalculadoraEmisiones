import speech_recognition as sr
import tkinter as tk
from tkinter import PhotoImage, simpledialog, messagebox, END

def obtener_nombre_por_voz():
    # Inicializamos el reconocedor de voz
    recognizer = sr.Recognizer()

    # Usamos el micrófono como fuente de entrada
    with sr.Microphone() as source:
        print("Por favor, di tu nombre...")  
        recognizer.adjust_for_ambient_noise(source)  # Ajustar el ruido ambiente
        audio = recognizer.listen(source)  # Escuchar el micrófono

    try:
        # Intentamos reconocer el audio
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
    emisiones_transporte = {'coche': 0.120, 'avion': 0.255, 'bus': 0.045}
    emisiones_electricidad = 0.233
    emisiones_residuos = 0.8

    huella_transporte = sum(emisiones_transporte[modo] * km for modo, km in transporte.items() if modo in emisiones_transporte)
    huella_electricidad = electricidad * emisiones_electricidad
    huella_residuos = residuos * emisiones_residuos

    return huella_transporte + huella_electricidad + huella_residuos

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

    huella_total = calcular_huella_carbono(transporte, electricidad, residuos)
    mostrar_resultados(huella_total, nombre_usuario)

def mostrar_resultados(huella_total, nombre_usuario):
    cajaTexto1.config(state="normal")
    cajaTexto1.delete("1.0", END)
    cajaTexto1.insert(END, f"\nHola {nombre_usuario}, tu huella de carbono total al mes es de {huella_total:.2f} kg CO2 equivalentes.\n")
    cajaTexto1.insert(END, "Sugerencias para reducir tu huella de carbono:\n")
    if huella_total > 90:
        cajaTexto1.insert(END, "- Considera usar más transporte público o bicicleta.\n")
        cajaTexto1.insert(END, "- Reduce tu consumo energético y revisa tus electrodomésticos.\n")
        cajaTexto1.insert(END, "- Separa mejor los residuos reciclables.\n")
    else:
        cajaTexto1.insert(END, "- ¡Buen trabajo! Sigue reduciendo tu huella.\n")
    cajaTexto1.config(state="disabled")

# Función para abrir la ventana principal
def abrir_ventana_principal():
    global cajaTexto1 #definimos cajaTexto1 como variable global para que pueda ser usada fuera

    #En tkinter, tk.Toplevel se utiliza para crear una nueva ventana separada de la ventana principal
    ventanaPrincipal = tk.Toplevel()
    ventanaPrincipal.geometry("650x300")
    ventanaPrincipal.title("Calculadora de emisiones")
    ventanaPrincipal.configure(bg="#f0fff0")

    frame1 = tk.Frame(ventanaPrincipal, bg="#d0f0c0", padx=10, pady=10)
    frame1.grid(row=0, column=0, padx=10, pady=10)

    etiqueta1 = tk.Label(frame1, text="Calculadora de emisiones:", font=("Arial", 14, "bold"), fg="#006400", bg="#d0f0c0")
    etiqueta1.grid(row=0, column=0, pady=5)

    boton1 = tk.Button(frame1, text="CALCULAR", font=("Arial", 12), bg="#90EE90", fg="black", command=obtener_datos_usuario)
    boton1.grid(row=1, column=0, pady=10)

    frame2 = tk.Frame(ventanaPrincipal, bg="#f0fff0", padx=10, pady=10)
    frame2.grid(row=0, column=1, padx=10, pady=10)
    
    #El wrap="word" se utiliza para que al poner palabras en la caja de texto estas no se corten al llegar al final del widget
    cajaTexto1 = tk.Text(frame2, height=10, width=40, bg="#ffffff", fg="#006400", font=("Arial", 10), wrap="word", relief="solid", borderwidth=1)
    cajaTexto1.grid(row=0, column=0)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Calculadora pantalla de inicio")
ventana.geometry("800x600")
ventana.configure(bg="white")

titulo = tk.Label(ventana, text="Calculadora de Huella de Carbono", font=("Arial", 24, "bold"), fg="#228B22", bg="white")
titulo.pack(pady=20)

# creamos la imagen y la incluimos al pack
imagen_path = "huella.png"
imagen = PhotoImage(file=imagen_path)
imagen = imagen.subsample(2, 2)
label_imagen = tk.Label(ventana, image=imagen, bg="white")
label_imagen.pack(pady=20)

# Botón de inicio que nos lleva a la calculadora
boton_inicio = tk.Button(ventana, text="Inicio", font=("Arial", 14), bg="#90EE90", fg="black", padx=20, pady=10, command=abrir_ventana_principal)
boton_inicio.pack(pady=20)

ventana.mainloop()
