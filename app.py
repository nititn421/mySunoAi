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
# POETRY
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
    ]
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
    ]
)


# =========================================================
# PITCH
# =========================================================

pitch = st.slider(
    "🎚️ Voice Pitch",
    -5,
    5,
    0,
    1
)


# =========================================================
# SPEED
# =========================================================

speed = st.slider(
    "⏩ Voice Speed",
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
    "✨ Voice Clarity / Treble",
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
    "🎵 Background Music",
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
# GENERATE BUTTON
# =========================================================

if st.button(
    "🎵 Generate Poetry Audio",
    type="primary"
):

    # =====================================================
    # CHECK POETRY
    # =====================================================

    if not lyrics.strip():

        st.error(
            "❌ पहले अपनी कविता लिखिए।"
        )

        st.stop()


    # =====================================================
    # PROCESS
    # =====================================================

    try:

        with st.spinner(
            "🎙️ आपकी कविता को Hindi AI Voice में बदला जा रहा है..."
        ):

            processed_voice, final_audio = create_poetry_audio(

                lyrics=lyrics,

                music_name=music_name,

                pitch=pitch,

                speed=speed,

                bass=bass,

                treble=treble,

                reverb=reverb,

                music_volume=music_volume

            )


        # =================================================
        # SUCCESS
        # =================================================

        st.success(
            "✅ आपकी Poetry Audio तैयार है!"
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


        # =================================================
        # AI VOICE
        # =================================================

        st.write(
            "### 🎙️ Hindi AI Voice"
        )

        st.audio(
            processed_voice
        )


        # =================================================
        # FINAL AUDIO
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

                file_name="MySunoAI_Poetry.mp3",

                mime="audio/mpeg"

            )


    except Exception as e:

        st.error(
            "❌ Audio Generation Error"
        )

        st.code(
            str(e)
        )
