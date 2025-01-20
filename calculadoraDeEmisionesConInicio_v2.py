import speech_recognition as sr
import tkinter as tk
from tkinter import Tk, simpledialog, messagebox, END, Text, Label, Button, Frame, PhotoImage

def obtener_nombre_por_voz():
    # Inicializamos el reconocedor de voz
    recognizer = sr.Recognizer()

    # Usamos el micrófono como fuente de entrada
    with sr.Microphone() as source:
        # Pedimos al usuario que hable
        print("Por favor, di tu nombre...")  
        recognizer.adjust_for_ambient_noise(source)  # Ajustar el ruido ambiente
        audio = recognizer.listen(source)  # Escuchar el micrófono

    try:
        # Intentamos reconocer el audio
        nombre = recognizer.recognize_google(audio, language="es-ES")
        print("Has dicho: " + nombre)
        return nombre
    except sr.UnknownValueError:
        # En caso de no reconocer el audio
        print("No se pudo entender lo que dijiste.")
        return None
    except sr.RequestError:
        # En caso de un problema con la conexión a internet
        print("No se pudo conectar al servicio de reconocimiento de voz.")
        return None

def calcular_huella_carbono(transporte, electricidad, residuos):
    emisiones_transporte = {'coche': 0.120,  
                            'avion': 0.255,  
                            'bus': 0.045}    
    emisiones_electricidad = 0.233  
    emisiones_residuos = 0.8   

    huella_transporte = 0
    for modo, km in transporte.items():
        if modo in emisiones_transporte:
            huella_transporte += emisiones_transporte[modo] * km
    
    huella_electricidad = electricidad * emisiones_electricidad
    huella_residuos = residuos * emisiones_residuos
    
    huella_total = huella_transporte + huella_electricidad + huella_residuos
    return huella_total

def obtener_datos_usuario(nombre_usuario):
    cajaTexto1.insert(END, "¡Bienvenido {nombre_usuario} a la calculadora de huella de carbono!\n")
    cajaTexto1.insert(END, "Responde las siguientes preguntas para estimar tu huella de carbono.\n")
    
    transporte = {}

    def obtener_numero(a):
        while True:
            entrada = simpledialog.askstring("Input", a, parent=ventanaPrincipal)
            if entrada is None:  
                messagebox.showwarning("Warning", "No has puesto un valor")
                return None
            try:
                return float(entrada)
            except ValueError:
                messagebox.showwarning("Warning", "Por favor, ingresa un número válido.")
    
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
    mostrar_resultados(huella_total)

def mostrar_resultados(huella_total):
    cajaTexto1.delete("1.0", END)
    
    cajaTexto1.insert(END, "\nTu huella de carbono total al mes es de " + str(huella_total) + " kg CO2 equivalentes.\n")
    cajaTexto1.insert(END, "Sugerencias para reducir tu huella de carbono:\n")
    
    if huella_total > 90:
        cajaTexto1.insert(END, "- Considera usar más transporte público o bicicletas en lugar de coche.\n")
        cajaTexto1.insert(END, "- Revisa tu consumo energético y considera cambiar a electrodomésticos más eficientes.\n")
        cajaTexto1.insert(END, "- Intenta reducir los residuos generados, separando mejor los reciclables.\n")
        cajaTexto1.insert(END, "- Explora opciones de dietas más sostenibles, como la vegetariana o vegana.\n")
    else:
        cajaTexto1.insert(END, "- ¡Buen trabajo! Pero siempre hay espacio para mejorar, sigue reduciendo tu huella.\n")
    
    cajaTexto1.config(state="readonly") 

# Función para abrir la ventana principal
def abrir_ventana_principal():
    ventanaPrincipal = tk.Toplevel() #En tkinter, tk.Toplevel se utiliza para crear una nueva ventana separada de la ventana principa
    ventanaPrincipal.geometry("650x300")
    ventanaPrincipal.title("Calculadora de emisiones")
    ventanaPrincipal.configure(bg="#f0fff0")

    frame1 = tk.Frame(ventanaPrincipal, bg="#d0f0c0", padx=10, pady=10)
    frame1.grid(row=0, column=0, padx=10, pady=10)
    etiqueta1 = tk.Label(frame1, text="Calculadora de emisiones:", font=("Arial", 14, "bold"), fg="#006400", bg="#d0f0c0")
    etiqueta1.grid(row=0, column=0, pady=5)

    boton1 = tk.Button(frame1, text="CALCULAR", font=("Arial", 12), bg="#90EE90", fg="black", command=lambda: obtener_datos_usuario(obtener_nombre_por_voz()))
    boton1.grid(row=1, column=0, pady=10)

    frame2 = tk.Frame(ventanaPrincipal, bg="#f0fff0", padx=10, pady=10)
    frame2.grid(row=0, column=1, padx=10, pady=10)
    
    #El wrap="word" se utiliza para que al poner palabras en la caja de texto estas no se corten al llegar al final del widget
    cajaTexto1 = tk.Text(frame2, height=10, width=40, bg="#ffffff", fg="#006400", font=("Arial", 10), wrap="word", relief="solid", borderwidth=1)
    cajaTexto1.grid(row=0, column=0)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de Huella de Carbono")
ventana.geometry("800x600")
ventana.configure(bg="white")

# Título
titulo = tk.Label(ventana, text="Calculadora de Huella de Carbono", font=("Arial", 24, "bold"), fg="#228B22", bg="white")
titulo.pack(pady=20)

# creamos la imagen y la incluimos al pack
imagen_path = "huella.png"  
imagen = PhotoImage(file=imagen_path)
imagen = imagen.subsample(2, 2)  # Hacer la imagen 2 veces más grande
label_imagen = tk.Label(ventana, image=imagen, bg="white")
label_imagen.pack(pady=20)

# Botón de inicio que nos lleva a la calculadora
boton_inicio = tk.Button(ventana, text="Inicio", font=("Arial", 14), bg="#90EE90", fg="white", padx=20, pady=10, command=abrir_ventana_principal)
boton_inicio.pack(pady=20)

ventana.mainloop()

