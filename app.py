import streamlit as st
import yt_dlp
import os

st.title("YouTube Video Downloader")
st.subheader("Descarga videos o audios de YouTube")

url = st.text_input("Ingrese la URL del video de YouTube:")

# Directorio temporal para guardar los archivos
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

if url:
    try:
        # Mostrar detalles del video
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            st.image(info.get('thumbnail'), width=300)
            st.write(f"**Título:** {info.get('title')}")
            st.write(f"**Duración:** {info.get('duration')} segundos")

        # Opciones para video y audio
        ydl_opts_video = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
            'quiet': True,
        }
        ydl_opts_audio = {
            'format': 'bestaudio/best',
            'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': '/ruta/a/ffmpeg'  # Cambia esta ruta si FFmpeg no está en el PATH
        }

        # Botones para descargar video o audio
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
