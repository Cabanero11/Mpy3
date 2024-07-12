import yt_dlp
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Función de hook para actualizar el progreso
def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d['_percent_str'].strip()
        percent = percent.replace('[0;94m', '').replace('[0m', '')  # Limpiar códigos de color
        status_label.config(text=f"[{percent}] descargado")
        root.update_idletasks()  # Actualizar la interfaz gráfica

# Función para descargar el audio desde YouTube
def download_audio(link, audio_quality):
    ydl_opts = {
        'format': f'bestaudio[abr<={audio_quality}]/bestaudio/best',
        'outtmpl': 'descargas/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': audio_quality,
        }],
        'progress_hooks': [progress_hook],  # Agregar hook de progreso
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            title = info_dict.get('title', None)
            filename = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')
        return filename, title
    except Exception as e:
        print("Ocurrió un error durante la descarga de audio:", e)
        return None, None

# Función para descargar el video desde YouTube
def download_video(link, video_quality):
    ydl_opts = {
        'format': f'bestvideo[height<={video_quality}]+bestaudio[ext=m4a]/best[height<={video_quality}]',
        'outtmpl': 'descargas/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],  # Agregar hook de progreso
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            title = info_dict.get('title', None)
            filename = ydl.prepare_filename(info_dict).replace('.webm', '.mp4')
        return filename, title
    except Exception as e:
        print("Ocurrió un error durante la descarga de video:", e)
        return None, None

def resource_path(relative_path):
    """ Conseguir el path, bien para cuando se haga el .exe """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Función para manejar el evento del botón de Toggle
def toggle_button_clicked():
    global download_function
    if toggle_var.get() == 1:
        download_function = download_audio
        toggle_button.config(image=audio_on_img)
        toggle_text.set("Audio (.mp3)")
        quality_combobox.config(values=audio_qualities)
        quality_combobox.set(audio_qualities[0])
    else:
        download_function = download_video
        toggle_button.config(image=video_on_img)
        toggle_text.set("Video (.mp4)")
        quality_combobox.config(values=video_qualities)
        quality_combobox.set(video_qualities[0])

# Función para manejar el evento del botón de Descargar
def download_button_clicked():
    link = url_entry.get()
    quality = quality_combobox.get().replace(' kbps', '').replace('p', '')
    if link:
        filename, title = download_function(link, quality)
        if filename and title:
            messagebox.showinfo("Descarga Completada", f"¡Descarga completada!\nArchivo guardado como {filename}")
            status_label.config(text="")  # Limpiar etiqueta de estado al finalizar
    else:
        messagebox.showwarning("Advertencia", "Por favor, introduce un enlace de YouTube")

def abrir_carpeta_descargas():
    try:
        # Directorio actual donde se ejecuta el script
        directorio_actual = os.getcwd()
        
        # Combinar el directorio actual con 'descargas/'
        carpeta_descargas = os.path.join(directorio_actual, 'descargas')
        
        # Abrir la carpeta en el explorador de archivos del sistema operativo
        os.startfile(carpeta_descargas)
        
    except Exception as e:
        print(f"Bruh donde esta la carpeta: {e}")


# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Descargador de YouTube")
root.geometry("400x360")
root.resizable(False, False)
root.configure(bg="#f0f0f0")  # Color de fondo similar al estilo de Windows 11
# Se pone audio default, sino da error el 'download_function'
download_function = download_audio

# Configuración para centrar la ventana en la pantalla
window_width = 400
window_height = 360

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))

root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

estilo = ttk.Style()
estilo.configure('BW.TLabel', font=('Helvetica', 14))

estilo_boton = ttk.Style()
estilo_boton.configure('my.TButton', font=('Helvetica', 12))

# Etiqueta y campo de entrada para la URL del video
url_label = ttk.Label(root, text="URL del video de YouTube:", style='BW.TLabel')
url_label.pack(pady=(20, 5))
url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=5)
url_entry.focus()

# Imágenes para el botón de toggle
audio_on_img = tk.PhotoImage(file=resource_path('audio_on.png'))
video_on_img = tk.PhotoImage(file=resource_path('video_on.png'))

toggle_text = tk.StringVar(value="Audio (.mp3)")

# Botón de Toggle para elegir entre descargar audio o video
toggle_var = tk.IntVar(value=1)  # Inicia con la opción de descargar audio (.mp3)
toggle_button = ttk.Checkbutton(root, textvariable=toggle_text, variable=toggle_var, onvalue=1, offvalue=0, command=toggle_button_clicked, image=audio_on_img, compound="right")
toggle_button.pack(pady=10)

# Opciones de calidad
audio_qualities = ['128 kbps', '192 kbps', '256 kbps']
video_qualities = ['360p', '480p', '720p', '1080p']

# Combobox para seleccionar la calidad
quality_label = ttk.Label(root, text="Selecciona la calidad:", style='BW.TLabel')
quality_label.pack(pady=(10, 5))
quality_combobox = ttk.Combobox(root, values=audio_qualities, state="readonly")
quality_combobox.set(audio_qualities[0])
quality_combobox.pack(pady=5)

# Botón para iniciar la descarga
download_button = ttk.Button(root, text="Descargar", command=download_button_clicked, style='my.TButton')
download_button.pack(pady=(10, 10))

# Botón para iniciar la descarga
download_button = ttk.Button(root, text="Abrir Carpeta", command=abrir_carpeta_descargas, style='my.TButton')
download_button.pack(pady=(10, 10))

# Etiqueta para mostrar el progreso
status_label = ttk.Label(root, text="", style='BW.TLabel')
status_label.pack(pady=(5, 5))

# Ejecutar la aplicación
root.mainloop()
