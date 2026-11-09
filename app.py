import tkinter as tk
import serial
import time

# Agrupamos las variables en un diccionario (sin la 't')
estado = {
    'x': 'N',
    'y': 'N',
    'vel': 150
}
try:
# Conexión al puerto
    try:
        arduino = serial.Serial('COM7', 9600, timeout=1)
        time.sleep(3)
        conexion = True
    except Exception as e:
        print(f"Error al conectar con Arduino: {e}")
        conexion = False
except KeyboardInterrupt:
    print("Programa interrumpido por el usuario.")
    if conexion and arduino.is_open:
        arduino.close()
    exit()
def enviar_vector():
    if conexion:
        # Crea la cadena "X, Y, Velocidad\n"
        mensaje = f"{estado['x']}, {estado['y']}, {estado['vel']}\n"
        arduino.write(mensaje.encode('utf-8'))
        print(f"Enviado: {mensaje.strip()}") 

def actualizar_velocidad(event):
    estado['vel'] = slider_vel.get()
    enviar_vector()

def presionar_tecla(event):
    tecla = event.keysym
    cambio = False
    
    if tecla == 'Up' and estado['y'] != 'F':
        estado['y'] = 'F'
        interfaz_flechas['Up'].config(bg="green")
        cambio = True
    elif tecla == 'Down' and estado['y'] != 'B':
        estado['y'] = 'B'
        interfaz_flechas['Down'].config(bg="green")
        cambio = True
    elif tecla == 'Left' and estado['x'] != 'L':
        estado['x'] = 'L'
        interfaz_flechas['Left'].config(bg="green")
        cambio = True
    elif tecla == 'Right' and estado['x'] != 'R':
        estado['x'] = 'R'
        interfaz_flechas['Right'].config(bg="green")
        cambio = True
        
    if cambio:
        enviar_vector()

def soltar_tecla(event):
    tecla = event.keysym
    cambio = False
    
    if tecla == 'Up' and estado['y'] == 'F':
        estado['y'] = 'N'
        interfaz_flechas['Up'].config(bg="red")
        cambio = True
    elif tecla == 'Down' and estado['y'] == 'B':
        estado['y'] = 'N'
        interfaz_flechas['Down'].config(bg="red")
        cambio = True
    elif tecla == 'Left' and estado['x'] == 'L':
        estado['x'] = 'N'
        interfaz_flechas['Left'].config(bg="red")
        cambio = True
    elif tecla == 'Right' and estado['x'] == 'R':
        estado['x'] = 'N'
        interfaz_flechas['Right'].config(bg="red")
        cambio = True
        
    if cambio:
        enviar_vector()

def al_cerrar():
    if conexion and arduino.is_open:
        arduino.close()
    ventana.destroy()
    ventana.quit()

# --- Interfaz Gráfica ---
ventana = tk.Tk()
ventana.title("Control Vectorial")
ventana.geometry("350x400") # Altura reducida al sacar el deslizador
ventana.configure(bg="#2b2b2b")
ventana.protocol("WM_DELETE_WINDOW", al_cerrar)

# Deslizador de Velocidad
slider_vel = tk.Scale(ventana, from_=0, to=255, orient='horizontal', 
                      label="Velocidad (PWM)", bg="#2b2b2b", fg="white", 
                      highlightthickness=0)
slider_vel.set(estado['vel'])
slider_vel.pack(pady=10, fill='x', padx=20)
slider_vel.bind("<ButtonRelease-1>", actualizar_velocidad)

# Cruz Direccional
frame = tk.Frame(ventana, bg="#2b2b2b")
frame.pack(expand=True, pady=10)

estilo = {"bg": "red", "fg": "white", "width": 6, "height": 3, "font": ("Arial", 12, "bold")}
interfaz_flechas = {
    'Up': tk.Label(frame, text="▲\n(F)", **estilo),
    'Left': tk.Label(frame, text="◄\n(L)", **estilo),
    'Down': tk.Label(frame, text="▼\n(B)", **estilo),
    'Right': tk.Label(frame, text="►\n(R)", **estilo)
}

interfaz_flechas['Up'].grid(row=0, column=1, padx=5, pady=5)
interfaz_flechas['Left'].grid(row=1, column=0, padx=5, pady=5)
interfaz_flechas['Down'].grid(row=1, column=1, padx=5, pady=5)
interfaz_flechas['Right'].grid(row=1, column=2, padx=5, pady=5)

ventana.bind('<KeyPress>', presionar_tecla)
ventana.bind('<KeyRelease>', soltar_tecla)

try:
    ventana.mainloop()
except KeyboardInterrupt:
    print("Programa interrumpido por el usuario.")
    al_cerrar()
