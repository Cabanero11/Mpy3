import yt_dlp
from moviepy.editor import AudioFileClip
import os

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

def convert_to_mp3(filename, title):
    try:
        audio_clip = AudioFileClip(filename)
        mp3_filename = f"descargas/{title}.mp3"
        audio_clip.write_audiofile(mp3_filename)
        print(f"¡Conversión completada con éxito! Archivo guardado como {mp3_filename}")
        audio_clip.close()
        # Elimina el archivo original si no lo necesitas
        os.remove(filename)
    except Exception as e:
        print("Ocurrió un error durante la conversión:", e)

link = input("Introduce el LINK del audio de YouTube: ")
filename, title = download_audio(link)

if filename and title:
    convert_to_mp3(filename, title)
