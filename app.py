import gradio as gr

from voice import create_poetry_audio


# =========================================================
# GENERATE POETRY
# =========================================================

def generate_poetry(

    lyrics,

    mood,

    voice_tone,

    music_name,

    voice_file

):


    if not voice_file:

        return (

            "❌ Please upload your voice recording.",

            None,

            None

        )


    if not lyrics:

        lyrics = (

            "Voice recording uploaded"

        )


    try:


        # Create final audio

        processed_voice, final_audio = (

            create_poetry_audio(

                voice_file=voice_file,

                music_name=music_name,

                mood=mood,

                voice_tone=voice_tone

            )

        )


        details = f"""
🎵 MySunoAI Poetry Studio

✅ Poetry Audio Generated Successfully

😊 Mood:
{mood}

🎙️ Voice Tone:
{voice_tone}

🎵 Background Music:
{music_name}

🎤 Voice:
Your Uploaded Voice

🎧 Processing:
Voice Enhancement + Automatic Music Mixing

🎬 Intro:
3 Seconds

🎬 Outro:
3 Seconds

📁 Final Audio:
Generated Successfully
"""


        return (

            details,

            processed_voice,

            final_audio

        )


    except Exception as e:


        error_message = f"""
❌ ERROR

{str(e)}

Please check the terminal for details.
"""


        print(
            error_message
        )


        return (

            error_message,

            None,

            None

        )


# =========================================================
# MUSIC LIST
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

    "background12.mp3",

]


# =========================================================
# GRADIO APP
# =========================================================

with gr.Blocks(

    title="MySunoAI Poetry Studio"

) as demo:


    gr.Markdown(

        "# 🎵 MySunoAI Poetry Studio"

    )


    gr.Markdown(

        "### 🎤 अपनी आवाज़ में Poetry बनाइए"

    )


    # =====================================================
    # POETRY
    # =====================================================

    lyrics = gr.Textbox(

        lines=10,

        label="✍️ Your Poetry",

        placeholder=(

            "यहाँ अपनी कविता लिखें..."

        )

    )


    # =====================================================
    # MOOD
    # =====================================================

    mood = gr.Dropdown(

        [
        "Emotional",
        "Sad",
        "Romantic",
        "Deep",
        "Calm",
        "Motivational",
        "Spiritual"
    ],
    value="Emotional",
    label="😊 Poetry Mood"

    )


    # =====================================================
    # VOICE TONE
    # =====================================================

    voice_tone = gr.Dropdown(

        [

            "Emotional",

            "Deep",

            "Soft",

            "Warm",

            "Clear"

        ],

        value="Emotional",

        label="🎙️ Voice Tone"

    )


    # =====================================================
    # MUSIC
    # =====================================================

    music_name = gr.Dropdown(

        choices=music_choices,

        value="background1.mp3",

        label="🎵 Select Background Music"

    )


    # =====================================================
    # VOICE UPLOAD
    # =====================================================

    voice_file = gr.Audio(

        sources=[

            "upload",

            "microphone"

        ],

        type="filepath",

        label=(

            "🎤 Upload Your Poetry Voice"

        )

    )


    # =====================================================
    # GENERATE BUTTON
    # =====================================================

    generate_button = gr.Button(

        "🎵 Generate Poetry",

        variant="primary"

    )


    # =====================================================
    # DETAILS
    # =====================================================

    details = gr.Textbox(

        label="📄 Processing Details",

        lines=10

    )


    # =====================================================
    # PROCESSED VOICE
    # =====================================================

    processed_voice = gr.Audio(

        type="filepath",

        label=(

            "🎙️ Processed Voice"

        )

    )


    # =====================================================
    # FINAL AUDIO
    # =====================================================

    final_audio = gr.Audio(

        type="filepath",

        label=(

            "🎧 Final Poetry With Music"

        )

    )


    # =====================================================
    # BUTTON ACTION
    # =====================================================

    generate_button.click(

        fn=generate_poetry,

        inputs=[

            lyrics,

            mood,

            voice_tone,

            music_name,

            voice_file

        ],

        outputs=[

            details,

            processed_voice,

            final_audio

        ]

    )


# =========================================================
# LAUNCH APP
# =========================================================

if __name__ == "__main__":

    demo.launch(

        share=True

    )