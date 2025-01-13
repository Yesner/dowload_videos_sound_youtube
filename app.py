import streamlit as st
import yt_dlp

# Título de la aplicación
st.title("YouTube Video Downloader")
st.subheader("Descarga tus videos o audios favoritos")

# Entrada de URL
url = st.text_input("Ingrese la URL del video de YouTube:")

# Verificar si se ha ingresado una URL
if url:
    try:
        # Opciones de descarga para yt-dlp
        ydl_opts_video = {
            'format': 'bestvideo+bestaudio/best',  # Descargar video con audio
            'outtmpl': '%(title)s.%(ext)s',  # Nombre del archivo basado en el título del video
            'quiet': True  # Modo silencioso
        }

        ydl_opts_audio = {
            'format': 'bestaudio/best',  # Descargar solo el audio
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Convertir audio a formato MP3
                'preferredquality': '192',  # Calidad del audio
            }]
        }

        # Mostrar información del video
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            st.image(info.get('thumbnail'), width=300)
            st.write(f"**Título:** {info.get('title')}")
            st.write(f"**Duración:** {info.get('duration')} segundos")
            st.write(f"**Subido por:** {info.get('uploader')}")

        # Botones para descarga
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
