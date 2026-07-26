import streamlit as st
from voice import create_poetry_audio

st.set_page_config(
    page_title="MySunoAI Poetry Studio",
    page_icon="🎵"
)

st.title("🎵 MySunoAI Poetry Studio")

st.write("MySunoAI is running successfully!")

if st.button("Test Voice Module"):
    st.success("Voice module loaded successfully!")
