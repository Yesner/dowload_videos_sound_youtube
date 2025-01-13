import streamlit as st
from pytube import YouTube
from pytube.exceptions import PytubeError

st.title("YouTube Video Downloader")
st.subheader("Descarga tus videos o audios favoritos")

url = st.text_input("Ingrese la URL del video de YouTube:")

if url:
    try:
        # Intentar cargar la información del video
        yt = YouTube(url)
        st.image(yt.thumbnail_url, width=300)
        st.write(f"**Título:** {yt.title}")
        st.write(f"**Duración:** {yt.length} segundos")
        st.write(f"**Calificación:** {yt.rating}")
        
        # Streams disponibles
        video_streams = yt.streams.filter(progressive=True, file_extension='mp4')
        audio_streams = yt.streams.filter(only_audio=True)

        if video_streams or audio_streams:
            st.subheader("Opciones de descarga:")
            if st.button("Descargar Video"):
                try:
                    video_streams.get_lowest_resolution().download()
                    st.success("Descarga de video completada")
                except Exception as e:
                    st.error(f"Error al descargar el video: {e}")
            if st.button("Descargar Solo Audio"):
                try:
                    audio_streams.first().download()
                    st.success("Descarga de audio completada")
                except Exception as e:
                    st.error(f"Error al descargar el audio: {e}")
        else:
            st.warning("No se encontraron streams disponibles.")
    except PytubeError as e:
        st.error(f"Error de Pytube: {e}")
    except KeyError as e:
        st.error("El video no pudo ser procesado. Es posible que Pytube necesite una actualización.")
    except Exception as e:
        st.error(f"Se produjo un error inesperado: {e}")
