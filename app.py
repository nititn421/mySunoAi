import streamlit as st
from voice import create_poetry_audio


st.set_page_config(
    page_title="MySunoAI Poetry Studio",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 MySunoAI Poetry Studio")
st.markdown("### 🎤 अपनी आवाज़ में Poetry बनाइए")


# Poetry
lyrics = st.text_area(
    "✍️ Your Poetry",
    placeholder="यहाँ अपनी कविता लिखें...",
    height=200
)


# Mood
mood = st.selectbox(
    "😊 Poetry Mood",
    [
        "Emotional",
        "Sad",
        "Romantic",
        "Deep",
        "Calm",
        "Motivational",
        "Spiritual"
    ]
)


# Voice Tone
voice_tone = st.selectbox(
    "🎙️ Voice Tone",
    [
        "Emotional",
        "Deep",
        "Soft",
        "Warm",
        "Clear"
    ]
)


# Music
music_choices = [
    "background1.mp3",
    "background2.mp3",
    "background3.mp3",
    "background4.mp3",
    "background5.mp3",
    "background6.mp3",
    "background7.mp3",
    "background8.mp3",
    "background9.mp3",
    "background10.mp3",
    "background11.mp3",
    "background12.mp3"
]

music_name = st.selectbox(
    "🎵 Select Background Music",
    music_choices
)


# Voice upload
voice_file = st.file_uploader(
    "🎤 Upload Your Poetry Voice",
    type=["wav", "mp3", "m4a", "ogg"]
)


# Generate
if st.button("🎵 Generate Poetry", type="primary"):

    if voice_file is None:

        st.error("❌ Please upload your voice recording.")

    else:

        try:

            # Save uploaded voice temporarily
            input_voice = "uploaded_voice.wav"

            with open(input_voice, "wb") as f:
                f.write(voice_file.getbuffer())


            st.info("🎵 Processing your voice... Please wait.")

            processed_voice, final_audio = create_poetry_audio(

                voice_file=input_voice,

                music_name=music_name,

                mood=mood,

                voice_tone=voice_tone

            )


            st.success(
                "✅ Poetry Audio Generated Successfully!"
            )


            st.write("### 📄 Processing Details")

            st.write(
                f"""
                😊 Mood: {mood}

                🎙️ Voice Tone: {voice_tone}

                🎵 Background Music: {music_name}

                🎤 Voice: Your Uploaded Voice

                🎧 Processing: Voice Enhancement + Automatic Music Mixing
                """
            )


            st.write("### 🎙️ Processed Voice")

            st.audio(
                processed_voice
            )


            st.write("### 🎧 Final Poetry With Music")

            st.audio(
                final_audio
            )


            # Download button
            with open(final_audio, "rb") as f:

                st.download_button(
                    label="⬇️ Download Final Poetry",
                    data=f,
                    file_name="MySunoAI_Poetry.mp3",
                    mime="audio/mpeg"
                )


        except Exception as e:

            st.error(
                f"❌ ERROR: {str(e)}"
            )
