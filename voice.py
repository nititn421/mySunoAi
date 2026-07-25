import os
from pathlib import Path

from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range


# =========================================================
# FOLDERS
# =========================================================

OUTPUT_DIR = Path("outputs")
MUSIC_DIR = Path("music")

OUTPUT_DIR.mkdir(exist_ok=True)
MUSIC_DIR.mkdir(exist_ok=True)


# =========================================================
# AVAILABLE MUSIC
# =========================================================

MUSIC_FILES = [
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
# GET SELECTED MUSIC
# =========================================================

def select_music(music_name):

    if not music_name:
        music_name = "background1.mp3"

    music_path = MUSIC_DIR / music_name

    if not music_path.exists():

        raise FileNotFoundError(
            f"Music file not found: {music_path}"
        )

    print(
        f"🎵 Selected Music: {music_path.name}"
    )

    return music_path


# =========================================================
# PROCESS VOICE
# =========================================================

def process_voice(
    voice_file,
    voice_tone
):

    if not voice_file:

        raise ValueError(
            "Please upload your voice recording."
        )


    print(
        "🎤 Processing Voice..."
    )


    # Load voice

    voice = AudioSegment.from_file(
        voice_file
    )


    # Mono

    voice = voice.set_channels(
        1
    )


    # Normalize

    voice = normalize(
        voice,
        headroom=1.0
    )


    # Compression

    voice = compress_dynamic_range(

        voice,

        threshold=-20.0,

        ratio=2.5,

        attack=5,

        release=80

    )


    # =====================================================
    # VOICE TONE
    # =====================================================

    if voice_tone == "Deep":

        voice = voice.low_pass_filter(
            8500
        )


    elif voice_tone == "Soft":

        voice = voice.low_pass_filter(
            7500
        )


    elif voice_tone == "Warm":

        voice = voice.low_pass_filter(
            9000
        )


    elif voice_tone == "Clear":

        voice = voice.high_pass_filter(
            80
        )


    elif voice_tone == "Emotional":

        voice = voice.high_pass_filter(
            70
        )


    # Final Normalize

    voice = normalize(
        voice,
        headroom=1.0
    )


    # Save processed voice

    processed_voice_path = (

        OUTPUT_DIR /

        "processed_voice.wav"

    )


    voice.export(

        processed_voice_path,

        format="wav"

    )


    print(
        "✅ Voice Processed"
    )


    return (

        voice,

        str(processed_voice_path)

    )


# =========================================================
# AUTOMATIC MIXING
# =========================================================

def automatic_mix(

    voice,

    music_path

):

    print(
        "🎵 Starting Automatic Mixing..."
    )


    # Load music

    music = AudioSegment.from_file(

        music_path

    )


    # =====================================================
    # REQUIRED MUSIC LENGTH
    # =====================================================

    intro_duration = 3000

    outro_duration = 3000


    required_length = (

        intro_duration

        + len(voice)

        + outro_duration

    )


    # Loop music if short

    while len(music) < required_length:

        music += music


    # Cut exact length

    music = music[

        :required_length

    ]


    # =====================================================
    # INTRO
    # =====================================================

    intro = music[

        :intro_duration

    ]


    intro = intro - 22


    intro = intro.fade_in(

        1500

    )


    # =====================================================
    # MAIN MUSIC
    # =====================================================

    main_music = music[

        intro_duration:

        intro_duration + len(voice)

    ]


    # Music low under voice

    main_music = main_music - 27


    # =====================================================
    # VOICE + MUSIC
    # =====================================================

    main_mix = main_music.overlay(

        voice

    )


    # =====================================================
    # OUTRO
    # =====================================================

    outro = music[

        intro_duration + len(voice):

        required_length

    ]


    outro = outro - 22


    outro = outro.fade_out(

        outro_duration

    )


    # =====================================================
    # FINAL AUDIO
    # =====================================================

    final_audio = (

        intro

        + main_mix

        + outro

    )


    # Final normalize

    final_audio = normalize(

        final_audio,

        headroom=1.0

    )


    print(
        "✅ Automatic Mixing Completed"
    )


    return final_audio


# =========================================================
# MAIN FUNCTION
# =========================================================

def create_poetry_audio(

    voice_file,

    music_name,

    mood,

    voice_tone

):


    print(
        "\n=============================="
    )

    print(
        "🎵 MySunoAI Processing Started"
    )

    print(
        "=============================="
    )


    # =====================================================
    # STEP 1
    # =====================================================

    voice, processed_voice_path = (

        process_voice(

            voice_file,

            voice_tone

        )

    )


    # =====================================================
    # STEP 2
    # =====================================================

    music_path = select_music(

        music_name

    )


    # =====================================================
    # STEP 3
    # =====================================================

    final_audio = automatic_mix(

        voice,

        music_path

    )


    # =====================================================
    # STEP 4
    # =====================================================

    final_path = (

        OUTPUT_DIR /

        "final_output.mp3"

    )


    final_audio.export(

        final_path,

        format="mp3",

        bitrate="192k"

    )


    print(
        "🎧 Final Poetry Audio Generated"
    )


    print(
        f"📁 Saved: {final_path}"
    )


    print(
        "=============================="
    )


    return (

        processed_voice_path,

        str(final_path)

    )