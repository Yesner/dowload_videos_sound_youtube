import streamlit as st
from pytube import YouTube
from pytube.exceptions import PytubeError

st.title("Youtube Video Downloader")
st.subheader("Enter the URL:")
url = st.text_input(label='URL')

if url != '':
    try:
        yt = YouTube(url)
        st.image(yt.thumbnail_url, width=300)
        try:
            st.subheader('''
            {}
            ## Length: {} seconds
            ## Rating: {} 
            '''.format(yt.title, yt.length, yt.rating))
        except PytubeError as e:
            st.error(f"An error occurred while accessing video details: {e}")
        
        video_streams = yt.streams.filter(progressive=True, file_extension='mp4')
        audio_streams = yt.streams.filter(only_audio=True)
        
        if video_streams or audio_streams:
            download_video = st.button("Download Video")
            download_audio = st.button("Download Audio Only")
            
            if download_video:
                try:
                    video_streams.get_lowest_resolution().download()
                    st.subheader("Video Download Complete")
                except PytubeError as e:
                    st.error(f"An error occurred while downloading the video: {e}")
            
            if download_audio:
                try:
                    audio_streams.first().download()
                    st.subheader("Audio Download Complete")
                except PytubeError as e:
                    st.error(f"An error occurred while downloading the audio: {e}")
        else:
            st.subheader("Sorry, this video cannot be downloaded")
    except PytubeError as e:
        st.error(f"An error occurred: {e}")