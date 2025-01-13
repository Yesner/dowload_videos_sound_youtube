import streamlit as st
from pytube import YouTube
from pytube.exceptions import PytubeError

# Título de la aplicación
st.title("YouTube Video Downloader")
st.subheader("Descarga tus videos o audios favoritos")

# Entrada de URL
url = st.text_input(label='Ingrese la URL del video de YouTube:')

# Verificar si se ha ingresado una URL
if url:
    try:
        # Obtener información del video
        yt = YouTube(url)
        st.image(yt.thumbnail_url, width=300)
        st.write(f"**Título:** {yt.title}")
        st.write(f"**Duración:** {yt.length} segundos")
        st.write(f"**Calificación:** {yt.rating}")

        # Obtener streams disponibles
        video_streams = yt.streams.filter(progressive=True, file_extension='mp4')
        audio_streams = yt.streams.filter(only_audio=True)

        # Mostrar opciones de descarga
        if video_streams or audio_streams:
            st.subheader("Opciones de descarga:")

            # Botones de descarga
            if st.button("Descargar Video"):
                try:
                    video = video_streams.get_lowest_resolution()
                    video.download()
                    st.success("Descarga de video completada")
                except Exception as e:
                    st.error(f"Error al descargar el video: {e}")

            if st.button("Descargar Solo Audio"):
                try:
                    audio = audio_streams.first()
                    audio.download()
                    st.success("Descarga de audio completada")
                except Exception as e:
                    st.error(f"Error al descargar el audio: {e}")
        else:
            st.warning("No se encontraron streams disponibles para descargar.")

    except PytubeError as e:
        st.error(f"Error al procesar la URL: {e}")
    except Exception as e:
        st.error(f"Se produjo un error inesperado: {e}")
