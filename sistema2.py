import tkinter as tk  # Biblioteca para crear interfaces gráficas (ventanas, botones, etiquetas, etc.)
from tkinter import messagebox  # Módulo de tkinter para mostrar mensajes emergentes (message boxes)
from tkinter import ttk  # Submódulo de tkinter para widgets avanzados como la barra de progreso
import subprocess  # Permite ejecutar aplicaciones externas (como abrir Word, Excel, etc.)
import datetime  # Manejo de fechas y horas actuales
import time  # Biblioteca para controlar el tiempo (pausas, delays)
import pyttsx3  # Biblioteca para convertir texto a voz (speech synthesis)
import psutil  # Biblioteca para obtener información del sistema, como el estado de la batería
import sys  # Biblioteca del sistema, se usa aquí para cerrar la aplicación

# Inicializar el motor de voz
engine = pyttsx3.init()

# Configuración de voz en español
voices = engine.getProperty('voices')
for voice in voices:
    if "spanish" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Variable global para controlar el estado del asistente de voz
voice_assistant_enabled = True

# Función para hablar, solo si el asistente de voz está activado
def speak(text):
    if voice_assistant_enabled:
        engine.say(text)
        engine.runAndWait()

# Función para simular el arranque del sistema con una pantalla de carga
def loading_screen(root):
    speak("Bienvenido a OreonOS. Iniciando el sistema.")
    
    load_frame = tk.Frame(root, bg="#2e2e2e")
    load_frame.pack(fill="both", expand=True)

    # Título de la pantalla de carga
    title = tk.Label(load_frame, text="OreonOS", font=("Helvetica", 24, "bold"), bg="#2e2e2e", fg="white")
    title.pack(pady=100)

    # Barra de progreso
    progress = ttk.Progressbar(load_frame, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=50)

    def simulate_load():
        for i in range(101):
            progress['value'] = i
            root.update_idletasks()
            time.sleep(0.03)  # Simula la carga progresiva
        load_frame.pack_forget()  # Remueve la pantalla de carga
        show_profile_selection(root)  # Muestra la pantalla de selección de perfil

    root.after(1000, simulate_load)  # Inicia la simulación después de 1 segundo

# Función para cambiar el estado del asistente de voz
def toggle_voice_assistant():
    global voice_assistant_enabled
    voice_assistant_enabled = not voice_assistant_enabled
    status = "activado" if voice_assistant_enabled else "desactivado"
    speak(f"Asistente de voz {status}")
    voice_button.config(text=f"Asistente de Voz: {status.capitalize()}")

# Función para simular la configuración de volumen
def simulate_volume():
    speak("Abriendo configuración de volumen.")
    
    volume_window = tk.Toplevel()
    volume_window.title("Configuración de Volumen")
    volume_window.geometry("300x200")
    volume_window.configure(bg="#e0e4f3")
    
    title = tk.Label(volume_window, text="Configuración de Volumen", font=("Helvetica", 16), bg="#e0e4f3")
    title.pack(pady=10)
    
    volume_label = tk.Label(volume_window, text="Nivel de volumen:", font=("Helvetica", 12), bg="#e0e4f3")
    volume_label.pack(pady=10)
    
    # Barra de desplazamiento para simular el ajuste de volumen
    volume_scale = tk.Scale(volume_window, from_=0, to=100, orient="horizontal", bg="#e0e4f3")
    volume_scale.pack(pady=10)

    apply_button = tk.Button(volume_window, text="Aplicar", font=("Helvetica", 12), command=lambda: close_window_with_audio(volume_window, "Configuración de volumen cerrada."))
    apply_button.pack(pady=10)

def close_window_with_audio(window, message):
    speak(message)
    window.destroy()

# Función para simular la configuración de Wi-Fi
def simulate_wifi():
    speak("Abriendo configuración de Wi-Fi.")
    
    wifi_window = tk.Toplevel()
    wifi_window.title("Configuración de Wi-Fi")
    wifi_window.geometry("300x250")
    wifi_window.configure(bg="#e0e4f3")
    
    title = tk.Label(wifi_window, text="Configuración de Wi-Fi", font=("Helvetica", 16), bg="#e0e4f3")
    title.pack(pady=10)
    
    wifi_label = tk.Label(wifi_window, text="Redes disponibles:", font=("Helvetica", 12), bg="#e0e4f3")
    wifi_label.pack(pady=10)
    
    # Lista simulada de redes Wi-Fi
    wifi_listbox = tk.Listbox(wifi_window, height=5, font=("Helvetica", 12))
    wifi_listbox.insert(1, "Wi-Fi Casa")
    wifi_listbox.insert(2, "Wi-Fi Oficina")
    wifi_listbox.insert(3, "Wi-Fi Invitados")
    wifi_listbox.insert(4, "Wi-Fi Pública")
    wifi_listbox.pack(pady=10)

    connect_button = tk.Button(wifi_window, text="Conectar", font=("Helvetica", 12), command=lambda: close_window_with_audio(wifi_window, "Configuración de Wi-Fi cerrada."))
    connect_button.pack(pady=10)

# Función para mostrar la interfaz de selección de perfil
def show_profile_selection(root):
    speak("Por favor selecciona tu perfil.")

    profile_frame = tk.Frame(root, bg="#e0e4f3", width=500, height=400)
    profile_frame.pack_propagate(False)
    profile_frame.pack()

    title = tk.Label(profile_frame, text="Selecciona tu perfil", font=("Helvetica", 20), bg="#e0e4f3")
    title.pack(pady=50)

    def login(profile):
        profile_frame.pack_forget()
        speak(f"Perfil {profile} seleccionado.")
        show_desktop(root, profile)

    # Botones de perfiles
    profile1_button = tk.Button(profile_frame, text="Farley Martinez", font=("Helvetica", 14), command=lambda: login("Farley Martinez"))
    profile1_button.pack(pady=10)

    profile2_button = tk.Button(profile_frame, text="Yeisson Rodriguez", font=("Helvetica", 14), command=lambda: login("Yeisson Rodriguez"))
    profile2_button.pack(pady=10)

# Función para mostrar el escritorio
def show_desktop(root, profile):
    speak(f"Bienvenido al escritorio, {profile}.")

    desktop_frame = tk.Frame(root, bg="#e0e4f3")
    desktop_frame.pack(fill="both", expand=True)

    # Actualización de fecha, hora y batería
    def update_time():
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Obtener el estado real de la batería
        battery = psutil.sensors_battery()
        if battery:
            battery_level = f"{battery.percent}%"
            charging_status = "Cargando" if battery.power_plugged else "No está cargando"
        else:
            battery_level = "No disponible"
            charging_status = ""

        welcome_label.config(text=f"Bienvenido, perfil {profile}!\nFecha: {date_str}\nHora: {time_str}\nBatería: {battery_level} - {charging_status}")
        root.after(1000, update_time)  # Actualiza cada segundo

    # Mostrar información
    welcome_label = tk.Label(desktop_frame, font=("Helvetica", 14), bg="#e0e4f3", justify="center")
    welcome_label.pack(pady=20)
    update_time()  # Inicia la actualización de la hora

    # Función para decir la hora y fecha al hacer clic
    def say_datetime():
        now = datetime.datetime.now()
        speak(f"Hoy es {now.strftime('%Y-%m-%d')} y son las {now.strftime('%H:%M:%S')}")

    # Función para decir el estado de la batería
    def say_battery_status():
        battery = psutil.sensors_battery()
        if battery:
            level = battery.percent
            status = "cargando" if battery.power_plugged else "sin cargar"
            speak(f"La batería está al {level}% y está {status}.")
        else:
            speak("No se puede obtener información de la batería.")

    # Botón para abrir el menú de aplicaciones
    menu_button = tk.Button(desktop_frame, text="Abrir Menú de Aplicaciones", font=("Helvetica", 12),
                            command=lambda: show_app_menu(root))
    menu_button.pack(pady=20)

    # Botón para alternar el asistente de voz
    global voice_button
    voice_button = tk.Button(desktop_frame, text="Asistente de Voz: Activado", font=("Helvetica", 12),
                             command=toggle_voice_assistant)
    voice_button.pack(pady=20)

    # Botón para decir la fecha y hora
    datetime_button = tk.Button(desktop_frame, text="Decir Fecha y Hora", font=("Helvetica", 12), command=say_datetime)
    datetime_button.pack(pady=10)

    # Botón para decir el estado de la batería
    battery_button = tk.Button(desktop_frame, text="Estado de la Batería", font=("Helvetica", 12), command=say_battery_status)
    battery_button.pack(pady=10)

    # Botones de volumen y Wi-Fi
    volume_button = tk.Button(desktop_frame, text="Configuración de Volumen", font=("Helvetica", 12), command=simulate_volume)
    volume_button.pack(pady=10)

    wifi_button = tk.Button(desktop_frame, text="Configuración de Wi-Fi", font=("Helvetica", 12), command=simulate_wifi)
    wifi_button.pack(pady=10)

    # Botón para apagar el sistema
    shutdown_button = tk.Button(desktop_frame, text="Apagar Sistema", font=("Helvetica", 12), command=lambda: show_shutdown_screen(root))
    shutdown_button.pack(pady=10)

    # Mostrar la información del sistema (OS)
    os_info_label = tk.Label(desktop_frame, text="OreonOS - Sistema Operativo Accesible", font=("Helvetica", 12), bg="#e0e4f3")
    os_info_label.pack(pady=50)

# Función para mostrar el menú de aplicaciones
def show_app_menu(root):
    speak("Abriendo el menú de aplicaciones.")
    
    app_window = tk.Toplevel()
    app_window.title("Menú de Aplicaciones")
    app_window.geometry("300x400")
    app_window.configure(bg="#e0e4f3")

    title = tk.Label(app_window, text="Menú de Aplicaciones", font=("Helvetica", 16), bg="#e0e4f3")
    title.pack(pady=10)

    apps = {
        "Microsoft Word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "Microsoft Excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "Navegador": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        "Gestor de Archivos": "explorer.exe",
        "Ajustes del Sistema": "C:\\Windows\\System32\\control.exe"
    }

    def open_app(app_name):
        speak(f"Abriendo {app_name}.")
        subprocess.Popen(apps[app_name])

    # Mostrar aplicaciones como botones
    for app_name in apps:
        app_button = tk.Button(app_window, text=app_name, font=("Helvetica", 12), command=lambda app_name=app_name: open_app(app_name))
        app_button.pack(pady=10)

# Función para mostrar la pantalla de apagado con una barra de progreso
def show_shutdown_screen(root):
    speak("Cerrando sesión y apagando el sistema.")
    
    shutdown_frame = tk.Frame(root, bg="#2e2e2e")
    shutdown_frame.pack(fill="both", expand=True)

    title = tk.Label(shutdown_frame, text="Cerrando sesión...", font=("Helvetica", 24, "bold"), bg="#2e2e2e", fg="white")
    title.pack(pady=100)

    progress = ttk.Progressbar(shutdown_frame, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=50)

    def simulate_shutdown():
        for i in range(101):
            progress['value'] = i
            root.update_idletasks()
            time.sleep(0.03)  # Simula la carga progresiva
        shutdown_frame.pack_forget()  # Remueve la pantalla de carga
        final_shutdown_frame = tk.Frame(root, bg="#2e2e2e")
        final_shutdown_frame.pack(fill="both", expand=True)
        final_title = tk.Label(final_shutdown_frame, text="Sistema Apagado", font=("Helvetica", 24, "bold"), bg="#2e2e2e", fg="white")
        final_title.pack(pady=100)
        root.after(2000, sys.exit)  # Cierra la aplicación después de 2 segundos

    root.after(1000, simulate_shutdown)  # Inicia la simulación de apagado

# Función principal para iniciar la interfaz gráfica
def main():
    root = tk.Tk()
    root.title("OreonOS")
    root.geometry("800x600")
    root.configure(bg="#e0e4f3")
    
    # Pantalla de carga inicial
    loading_screen(root)
    
    root.mainloop()

# Ejecutar la función principal
if __name__ == "__main__":
    main()

