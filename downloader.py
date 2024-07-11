import yt_dlp
import os
import tkinter as tk
from tkinter import ttk, messagebox
from pydub import AudioSegment

# Función para descargar el audio desde YouTube
def download_audio(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'descargas/%(title)s.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            title = info_dict.get('title', None)
            filename = ydl.prepare_filename(info_dict)
        return filename, title
    except Exception as e:
        print("Ocurrió un error durante la descarga:", e)
        return None, None

# Función para convertir el archivo descargado a formato MP3 usando pydub
def convert_to_mp3(filename, title):
    try:
        # Cargar el archivo .webm usando pydub
        audio = AudioSegment.from_file(filename)

        # Crear el nombre de archivo para el archivo MP3 de salida
        mp3_filename = f"descargas/{title}.mp3"

        # Exportar el audio a formato MP3 usando pydub
        audio.export(mp3_filename, format="mp3")

        print(f"¡Conversión completada con éxito! Archivo guardado como {mp3_filename}")

        # Eliminar el archivo original si no se necesita
        os.remove(filename)

        return mp3_filename
    except Exception as e:
        print("Ocurrió un error durante la conversión:", e)
        return None

# Función para manejar el evento del botón de Descargar
def download_button_clicked():
    link = url_entry.get()
    if link:
        filename, title = download_audio(link)
        if filename and title:
            mp3_filename = convert_to_mp3(filename, title)
            if mp3_filename:
                messagebox.showinfo("Descarga Completada", f"¡Descarga completada!\nArchivo guardado como {mp3_filename}")
    else:
        messagebox.showwarning("Advertencia", "Por favor, introduce un enlace de YouTube")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Descargador de Audio de YouTube")
root.geometry("400x150")
root.resizable(False, False)
root.configure(bg="#f0f0f0")  # Color de fondo similar al estilo de Windows 11

# Etiqueta y campo de entrada para la URL del video
url_label = ttk.Label(root, text="URL del video de YouTube:")
url_label.pack(pady=(20, 5))
url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=5)

# Botón para iniciar la descarga
download_button = ttk.Button(root, text="Descargar", command=download_button_clicked)
download_button.pack(pady=(10, 20))

# Ejecutar la aplicación
root.mainloop()
