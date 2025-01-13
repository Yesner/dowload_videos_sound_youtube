import streamlit as st
import yt_dlp

st.title("YouTube Video Downloader")
st.subheader("Descarga tus videos o audios favoritos")

url = st.text_input("Ingrese la URL del video de YouTube:")

if url:
    try:
        # Opciones de descarga para yt-dlp
        ydl_opts_video = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True
        }

        ydl_opts_audio = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': '/ruta/a/ffmpeg'  # Cambia esta ruta si FFmpeg no está en el PATH
        }

        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            st.image(info.get('thumbnail'), width=300)
            st.write(f"**Título:** {info.get('title')}")
            st.write(f"**Duración:** {info.get('duration')} segundos")

        if st.button("Descargar Video"):
            try:
                with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
                    ydl.download([url])
                st.success("Descarga de video completada")
            except Exception as e:
                st.error(f"Error al descargar el video: {e}")

        if st.button("Descargar Solo Audio"):
            try:
                with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
                    ydl.download([url])
                st.success("Descarga de audio completada")
            except Exception as e:
                st.error(f"Error al descargar el audio: {e}")

    except Exception as e:
        st.error(f"Error al procesar la URL: {e}")
