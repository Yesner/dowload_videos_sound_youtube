import streamlit as st
import yt_dlp
import os

# Título de la aplicación
st.title("YouTube Video Downloader")
st.subheader("Descarga videos o audios directamente desde YouTube")

# Entrada de la URL del video
url = st.text_input("Ingrese la URL del video de YouTube:")

# Crear directorio para guardar descargas
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

# Ruta del ejecutable de FFmpeg
ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "ffmpeg.exe")

# Verificar si FFmpeg existe
if not os.path.isfile(ffmpeg_path):
    st.error("FFmpeg no encontrado. Asegúrate de que FFmpeg esté en la carpeta 'ffmpeg'.")

# Función para procesar la URL y descargar el contenido
if url:
    try:
        # Obtener información del video
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            st.image(info.get('thumbnail'), width=300)
            st.write(f"**Título:** {info.get('title')}")
            st.write(f"**Duración:** {info.get('duration')} segundos")

        # Opciones para descargar video
        ydl_opts_video = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
            'quiet': True,
            'ffmpeg_location': ffmpeg_path  # Ruta a FFmpeg
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
            'ffmpeg_location': ffmpeg_path  # Ruta a FFmpeg
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