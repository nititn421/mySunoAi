import streamlit as st

from voice import create_poetry_audio


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="MySunoAI Poetry Studio",
    page_icon="🎵",
    layout="centered"
)


st.title(
    "🎵 MySunoAI Poetry Studio"
)

st.markdown(
    "### 🎤 अपनी आवाज़ में Professional Poetry बनाइए"
)


# =========================================================
# POETRY
# =========================================================

lyrics = st.text_area(
    "✍️ Your Poetry",
    placeholder="यहाँ अपनी कविता लिखें...",
    height=180
)


# =========================================================
# MOOD
# =========================================================

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


# =========================================================
# VOICE PRESET
# =========================================================

preset = st.selectbox(
    "🎙️ Voice Enhancement Preset",
    [
        "Natural",
        "Warm",
        "Deep",
        "Studio",
        "Cinematic"
    ],
    index=3
)


st.markdown(
    "### 🎚️ Advanced Voice Controls"
)


# =========================================================
# PITCH
# =========================================================

pitch = st.slider(
    "🎚️ Pitch — मोटी ↔ पतली",
    -5,
    5,
    0,
    1
)


# =========================================================
# SPEED
# =========================================================

speed = st.slider(
    "⏩ Speed — Slow ↔ Fast",
    0.7,
    1.3,
    1.0,
    0.05
)


# =========================================================
# BASS
# =========================================================

bass = st.slider(
    "🔊 Bass",
    -5,
    8,
    0,
    1
)


# =========================================================
# TREBLE
# =========================================================

treble = st.slider(
    "✨ Treble / Clarity",
    -5,
    8,
    0,
    1
)


# =========================================================
# REVERB
# =========================================================

reverb = st.slider(
    "🌊 Reverb",
    0,
    30,
    0,
    1
)


# =========================================================
# MUSIC
# =========================================================

music_choices = [
    f"background{i}.mp3"
    for i in range(1, 13)
]


music_name = st.selectbox(
    "🎵 Select Background Music",
    music_choices
)


# =========================================================
# MUSIC VOLUME
# =========================================================

music_volume = st.slider(
    "🎵 Background Music Volume",
    -35,
    -15,
    -28,
    1
)


# =========================================================
# VOICE UPLOAD
# =========================================================

voice_file = st.file_uploader(
    "🎤 Upload Your Poetry Voice",
    type=[
        "wav",
        "mp3",
        "m4a",
        "ogg"
    ]
)


# =========================================================
# GENERATE
# =========================================================

if st.button(
    "🎵 Generate Professional Poetry",
    type="primary"
):

    if voice_file is None:

        st.error(
            "❌ Please upload your voice recording."
        )


    else:

        try:

            # Save upload

            input_voice = (
                "uploaded_voice.wav"
            )


            with open(
                input_voice,
                "wb"
            ) as f:

                f.write(
                    voice_file.getbuffer()
                )


            with st.spinner(
                "🎵 आपकी आवाज़ को enhance और music के साथ mix किया जा रहा है..."
            ):


                processed_voice, final_audio = (
                    create_poetry_audio(

                        voice_file=input_voice,

                        music_name=music_name,

                        mood=mood,

                        preset=preset,

                        pitch=pitch,

                        speed=speed,

                        bass=bass,

                        treble=treble,

                        reverb=reverb,

                        music_volume=music_volume

                    )
                )


            st.success(
                "✅ Professional Poetry Audio Generated!"
            )


            # =================================================
            # DETAILS
            # =================================================

            st.write(
                "### 📄 Processing Details"
            )


            st.write(
                f"""
😊 Mood: {mood}

🎙️ Preset: {preset}

🎚️ Pitch: {pitch}

⏩ Speed: {speed}x

🔊 Bass: {bass}

✨ Treble: {treble}

🌊 Reverb: {reverb}

🎵 Background Music: {music_name}

🎵 Music Volume: {music_volume} dB

🎧 Processing: Voice Enhancement + Compression + Automatic Music Mixing
"""
            )


            # =================================================
            # PROCESSED VOICE
            # =================================================

            st.write(
                "### 🎙️ Enhanced Voice"
            )


            st.audio(
                processed_voice
            )


            # =================================================
            # FINAL
            # =================================================

            st.write(
                "### 🎧 Final Poetry With Music"
            )


            st.audio(
                final_audio
            )


            # =================================================
            # DOWNLOAD
            # =================================================

            with open(
                final_audio,
                "rb"
            ) as f:

                st.download_button(

                    label="⬇️ Download Final Poetry",

                    data=f,

                    file_name=(
                        "MySunoAI_Professional_Poetry.mp3"
                    ),

                    mime="audio/mpeg"

                )


        except Exception as e:

            st.error(
                f"❌ ERROR: {str(e)}"
            )
