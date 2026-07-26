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
    "### 🎤 अपनी आवाज़ में Poetry बनाइए"
)


# =========================================================
# POETRY
# =========================================================

lyrics = st.text_area(

    "✍️ Your Poetry",

    placeholder="यहाँ अपनी कविता लिखें...",

    height=200

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
# VOICE TONE
# =========================================================

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


# =========================================================
# VOICE EFFECTS
# =========================================================

st.markdown(
    "## 🎚️ Voice Effects"
)


# Pitch

pitch = st.slider(

    "🎚️ Voice Pitch",

    min_value=-5,

    max_value=5,

    value=0,

    step=1,

    help="Negative = मोटी आवाज़ | Positive = पतली आवाज़"

)


# Speed

speed = st.slider(

    "🐢 Voice Speed",

    min_value=0.5,

    max_value=1.5,

    value=1.0,

    step=0.05

)


# Bass

bass = st.slider(

    "🔊 Bass",

    min_value=0,

    max_value=10,

    value=0

)


# Treble

treble = st.slider(

    "✨ Treble",

    min_value=0,

    max_value=10,

    value=0

)


# Reverb

reverb = st.slider(

    "🌊 Reverb",

    min_value=0,

    max_value=20,

    value=0

)


# =========================================================
# MUSIC
# =========================================================

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

    "🎵 Generate Poetry Remix",

    type="primary"

):


    if voice_file is None:

        st.error(

            "❌ Please upload your voice recording."

        )


    else:


        try:


            # Temporary file

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


            st.info(

                "🎵 आपकी आवाज़ process हो रही है..."

            )


            # Generate

            processed_voice, final_audio = (

                create_poetry_audio(

                    voice_file=input_voice,

                    music_name=music_name,

                    mood=mood,

                    voice_tone=voice_tone,

                    pitch=pitch,

                    speed=speed,

                    bass=bass,

                    treble=treble,

                    reverb=reverb

                )

            )


            st.success(

                "✅ Poetry Remix Successfully Generated!"

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

🎙️ Voice Tone: {voice_tone}

🎚️ Pitch: {pitch}

🐢 Speed: {speed}x

🔊 Bass: {bass}

✨ Treble: {treble}

🌊 Reverb: {reverb}

🎵 Background Music: {music_name}

"""

            )


            # =================================================
            # PROCESSED VOICE
            # =================================================

            st.write(

                "### 🎙️ Processed Voice"

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

                        "MySunoAI_Poetry_Remix.mp3"

                    ),

                    mime="audio/mpeg"

                )


        except Exception as e:


            st.error(

                f"❌ ERROR: {str(e)}"

            )
