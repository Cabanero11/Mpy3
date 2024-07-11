import yt_dlp
import os
import tkinter as tk
from tkinter import ttk, messagebox

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
        print("Ocurrió un error durante la descarga de audio:", e)
        return None, None

# Función para descargar el video desde YouTube
def download_video(link):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'descargas/%(title)s.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            title = info_dict.get('title', None)
            filename = ydl.prepare_filename(info_dict)
        return filename, title
    except Exception as e:
        print("Ocurrió un error durante la descarga de video:", e)
        return None, None

# Función para manejar el evento del botón de Toggle
def toggle_button_clicked():
    global download_function
    if toggle_var.get() == 1:
        download_function = download_audio
        messagebox.showinfo("Selección", "Se descargarán archivos de audio (.mp3)")
    else:
        download_function = download_video
        messagebox.showinfo("Selección", "Se descargarán archivos de video (.mp4)")

# Función para manejar el evento del botón de Descargar
def download_button_clicked():
    link = url_entry.get()
    if link:
        filename, title = download_function(link)
        if filename and title:
            messagebox.showinfo("Descarga Completada", f"¡Descarga completada!\nArchivo guardado como {filename}")
    else:
        messagebox.showwarning("Advertencia", "Por favor, introduce un enlace de YouTube")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Descargador de YouTube")
root.geometry("400x200")
root.resizable(False, False)
root.configure(bg="#f0f0f0")  # Color de fondo similar al estilo de Windows 11

# Etiqueta y campo de entrada para la URL del video
url_label = ttk.Label(root, text="URL del video de YouTube:")
url_label.pack(pady=(20, 5))
url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=5)

# Botón de Toggle para elegir entre descargar audio o video
toggle_var = tk.IntVar(value=1)  # Inicia con la opción de descargar audio (.mp3)
toggle_button = ttk.Checkbutton(root, text="Descargar como audio (.mp3)", variable=toggle_var, onvalue=1, offvalue=0, command=toggle_button_clicked)
toggle_button.pack(pady=10)

# Botón para iniciar la descarga
download_button = ttk.Button(root, text="Descargar", command=download_button_clicked)
download_button.pack(pady=(10, 20))

# Ejecutar la aplicación
root.mainloop()
