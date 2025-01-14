import streamlit as st
import yt_dlp
import os
import subprocess
import sys
import zipfile

# Función para descargar y descomprimir FFmpeg
def download_ffmpeg():
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    ffmpeg_zip = "ffmpeg.zip"
    ffmpeg_dir = "ffmpeg"

    # Descargar FFmpeg
    subprocess.run(["curl", "-L", ffmpeg_url, "-o", ffmpeg_zip], check=True)

    # Descomprimir FFmpeg
    with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
        zip_ref.extractall(ffmpeg_dir)

    # Mover el ejecutable a la carpeta correcta
    for root, dirs, files in os.walk(ffmpeg_dir):
        for file in files:
            if file == "ffmpeg.exe":
                os.rename(os.path.join(root, file), os.path.join(ffmpeg_dir, "ffmpeg.exe"))
                break

# Verificar si FFmpeg existe y descargarlo si no está presente
ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "ffmpeg.exe")
if not os.path.isfile(ffmpeg_path):
    st.warning("FFmpeg no encontrado. Descargando FFmpeg...")
    download_ffmpeg()
    if not os.path.isfile(ffmpeg_path):
        st.error("No se pudo descargar FFmpeg. Asegúrate de que FFmpeg esté en la carpeta 'ffmpeg'.")
        sys.exit(1)

# Título de la aplicación
st.title("YouTube Video Downloader")
st.subheader("Descarga videos o audios directamente desde YouTube")

# Entrada de la URL del video
url = st.text_input("Ingrese la URL del video de YouTube:")

# Crear directorio para guardar descargas
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

# Función para procesar la URL y descargar el contenido
if url:
    try:
        # Obtener información del video
        ydl_opts_info = {
            'quiet': True,
            'ffmpeg_location': ffmpeg_path,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            st.image(info.get('thumbnail'), width=300)
            st.write(f"**Título:** {info.get('title')}")
            st.write(f"**Duración:** {info.get('duration')} segundos")

        # Opciones para descargar video
        ydl_opts_video = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
            'quiet': True,
            'ffmpeg_location': ffmpeg_path,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }

        # Opciones para descargar solo audio
        ydl_opts_audio = {
            'format': 'bestaudio/best',
            'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': ffmpeg_path,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }

        # Botones de descarga
        if st.button("Descargar Video"):
            try:
                with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
                    ydl.download([url])
                video_path = os.path.join(download_dir, f"{info.get('title')}.mp4")
                st.success("Descarga de video completada")
                with open(video_path, "rb") as file:
                    st.download_button(
                        label="Descargar Video",
                        data=file,
                        file_name=f"{info.get('title')}.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"Error al descargar el video: {e}")

        if st.button("Descargar Solo Audio"):
            try:
                with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
                    ydl.download([url])
                audio_path = os.path.join(download_dir, f"{info.get('title')}.mp3")
                st.success("Descarga de audio completada")
                with open(audio_path, "rb") as file:
                    st.download_button(
                        label="Descargar Audio",
                        data=file,
                        file_name=f"{info.get('title')}.mp3",
                        mime="audio/mpeg"
                    )
            except Exception as e:
                st.error(f"Error al descargar el audio: {e}")

    except Exception as e:
        st.error(f"Error al procesar la URL: {e}")