# CalculadoraEmisiones
import speech_recognition as sr
from tkinter import Tk, simpledialog, messagebox, END, Text, Label, Button, Frame

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
    cajaTexto1.insert(END, f"¡Bienvenido {nombre_usuario} a la calculadora de huella de carbono!\n")
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

ventanaPrincipal = Tk()
ventanaPrincipal.geometry("430x250")
ventanaPrincipal.title("Calculadora de emisiones")

frame1 = Frame(ventanaPrincipal)
frame1.grid(row=0, column=0)
etiqueta1 = Label(frame1, text="Calculadora de emisiones:")
etiqueta1.grid(row=0, column=0)

boton1 = Button(frame1, text="CALCULAR", command=lambda: obtener_datos_usuario(obtener_nombre_por_voz()))
boton1.grid(row=1, column=0)

frame2 = Frame(ventanaPrincipal)
frame2.grid(row=0, column=1)
cajaTexto1 = Text(frame2, height=15, width=80)
cajaTexto1.grid(row=0, column=0)

ventanaPrincipal.mainloop()
