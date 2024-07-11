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
        toggle_button.config(image=audio_on_img)
        toggle_text.set("Audio (.mp3)")
    else:
        download_function = download_video
        toggle_button.config(image=video_on_img)
        toggle_text.set("Video (.mp4)")

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
audio_on_img = tk.PhotoImage(file="audio_on.png")
video_on_img = tk.PhotoImage(file="video_on.png")

toggle_text = tk.StringVar(value="Audio (.mp3)")

# Botón de Toggle para elegir entre descargar audio o video
toggle_var = tk.IntVar(value=1)  # Inicia con la opción de descargar audio (.mp3)
toggle_button = ttk.Checkbutton(root, textvariable=toggle_text, variable=toggle_var, onvalue=1, offvalue=0, command=toggle_button_clicked, image=audio_on_img, compound="right")
toggle_button.pack(pady=10)

# Botón para iniciar la descarga
download_button = ttk.Button(root, text="Descargar", command=download_button_clicked, style='my.TButton')
download_button.pack(pady=(10, 10))

# Ejecutar la aplicación
root.mainloop()
