import streamlit as st

from voice import create_poetry_audio


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MySunoAI Poetry Studio",
    page_icon="🎵",
    layout="centered"
)


# =========================================================
# TITLE
# =========================================================

st.title("🎵 MySunoAI Poetry Studio")

st.markdown(
    "### ✍️ अपनी कविता लिखिए और उसे Hindi AI Voice में सुनिए"
)


# =========================================================
# POETRY INPUT
# =========================================================

lyrics = st.text_area(
    "✍️ अपनी कविता लिखें",
    placeholder=(
        "यहाँ अपनी कविता लिखें...\n\n"
        "उदाहरण:\n"
        "वह चाँद के बगल का तारा ऐसे मुस्कुराता है..."
    ),
    height=250
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
    ],
    index=0
)


# =========================================================
# VOICE STYLE
# =========================================================

voice_style = st.selectbox(
    "🎙️ Voice Style",
    [
        "Natural",
        "Soft",
        "Deep",
        "Warm",
        "Clear"
    ],
    index=0
)


# =========================================================
# PITCH
# =========================================================

pitch = st.slider(
    "🎚️ Voice Pitch",
    min_value=-5,
    max_value=5,
    value=0,
    step=1
)


# =========================================================
# SPEED
# =========================================================

speed = st.slider(
    "⏩ Voice Speed",
    min_value=0.7,
    max_value=1.3,
    value=1.0,
    step=0.05
)


# =========================================================
# BASS
# =========================================================

bass = st.slider(
    "🔊 Bass",
    min_value=-5,
    max_value=8,
    value=0,
    step=1
)


# =========================================================
# TREBLE
# =========================================================

treble = st.slider(
    "✨ Voice Clarity / Treble",
    min_value=-5,
    max_value=8,
    value=0,
    step=1
)


# =========================================================
# REVERB
# =========================================================

reverb = st.slider(
    "🌊 Reverb",
    min_value=0,
    max_value=30,
    value=0,
    step=1
)


# =========================================================
# BACKGROUND MUSIC
# =========================================================

music_choices = [
    f"background{i}.mp3"
    for i in range(1, 13)
]


music_name = st.selectbox(
    "🎵 Background Music",
    music_choices,
    index=0
)


# =========================================================
# MUSIC VOLUME
# =========================================================

music_volume = st.slider(
    "🎵 Background Music Volume",
    min_value=-35,
    max_value=-15,
    value=-28,
    step=1
)


# =========================================================
# GENERATE BUTTON
# =========================================================

generate_button = st.button(
    "🎵 Generate Poetry Audio",
    type="primary",
    use_container_width=True
)


# =========================================================
# GENERATE AUDIO
# =========================================================

if generate_button:

    # -----------------------------------------------------
    # CHECK POETRY
    # -----------------------------------------------------

    if not lyrics.strip():

        st.error(
            "❌ पहले अपनी कविता लिखिए।"
        )

        st.stop()


    # -----------------------------------------------------
    # PROCESS
    # -----------------------------------------------------

    try:

        with st.spinner(
            "🎙️ आपकी कविता को Hindi AI Voice में बदला जा रहा है..."
        ):

            processed_voice, final_audio = (
                create_poetry_audio(

                    lyrics=lyrics,

                    music_name=music_name,

                    mood=mood,

                    voice_style=voice_style,

                    pitch=pitch,

                    speed=speed,

                    bass=bass,

                    treble=treble,

                    reverb=reverb,

                    music_volume=music_volume

                )
            )


        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        st.success(
            "✅ आपकी Poetry Audio तैयार है!"
        )


        # -------------------------------------------------
        # DETAILS
        # -------------------------------------------------

        st.write(
            "### 📄 Processing Details"
        )

        st.info(
            f"""
😊 Poetry Mood: {mood}

🎙️ Voice Style: {voice_style}

🎚️ Pitch: {pitch}

⏩ Speed: {speed}x

🔊 Bass: {bass}

✨ Treble: {treble}

🌊 Reverb: {reverb}

🎵 Background Music: {music_name}

🎵 Music Volume: {music_volume} dB
"""
        )


        # -------------------------------------------------
        # AI VOICE
        # -------------------------------------------------

        st.write(
            "### 🎙️ Hindi AI Voice"
        )

        st.audio(
            processed_voice,
            format="audio/mp3"
        )


        # -------------------------------------------------
        # FINAL AUDIO
        # -------------------------------------------------

        st.write(
            "### 🎧 Final Poetry With Music"
        )

        st.audio(
            final_audio,
            format="audio/mp3"
        )


        # -------------------------------------------------
        # DOWNLOAD
        # -------------------------------------------------

        with open(
            final_audio,
            "rb"
        ) as audio_file:

            st.download_button(

                label="⬇️ Download Final Poetry",

                data=audio_file,

                file_name="MySunoAI_Poetry.mp3",

                mime="audio/mpeg",

                use_container_width=True

            )


    # -----------------------------------------------------
    # ERROR
    # -----------------------------------------------------

    except Exception as e:

        st.error(
            "❌ Audio Generation Error"
        )

        st.code(
            str(e)
        )
