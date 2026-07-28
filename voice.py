import asyncio
from pathlib import Path

import edge_tts
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
# HINDI VOICE
# =========================================================

VOICE = "hi-IN-MadhurNeural"


# =========================================================
# MOOD SETTINGS
# =========================================================

MOOD_SETTINGS = {

    "Emotional": {
        "rate": "-8%",
        "pitch": "-1Hz"
    },

    "Sad": {
        "rate": "-15%",
        "pitch": "-2Hz"
    },

    "Romantic": {
        "rate": "-10%",
        "pitch": "+1Hz"
    },

    "Deep": {
        "rate": "-12%",
        "pitch": "-3Hz"
    },

    "Calm": {
        "rate": "-15%",
        "pitch": "0Hz"
    },

    "Motivational": {
        "rate": "+5%",
        "pitch": "+1Hz"
    },

    "Spiritual": {
        "rate": "-18%",
        "pitch": "-1Hz"
    }
}


# =========================================================
# PREPARE POETRY
# =========================================================

def prepare_poetry(text):

    if not text or not text.strip():
        raise ValueError(
            "Please enter your poetry."
        )

    text = text.strip()

    # Natural pauses
    text = text.replace(
        "...",
        " ... "
    )

    text = text.replace(
        "।",
        "। "
    )

    text = text.replace(
        ",",
        ", "
    )

    # Line breaks
    lines = []

    for line in text.splitlines():

        line = line.strip()

        if line:

            lines.append(line)

    # Separate poetry lines
    final_text = " ... ".join(lines)

    return final_text


# =========================================================
# GENERATE VOICE
# =========================================================

async def generate_voice_async(
    text,
    output_path,
    rate,
    pitch
):

    communicate = edge_tts.Communicate(

        text=text,

        voice=VOICE,

        rate=rate,

        pitch=pitch
    )

    await communicate.save(
        str(output_path)
    )


def generate_hindi_voice(
    text,
    mood="Emotional"
):

    poetry = prepare_poetry(
        text
    )

    settings = MOOD_SETTINGS.get(

        mood,

        MOOD_SETTINGS["Emotional"]

    )

    output_path = (

        OUTPUT_DIR /

        "ai_voice.mp3"

    )

    asyncio.run(

        generate_voice_async(

            text=poetry,

            output_path=output_path,

            rate=settings["rate"],

            pitch=settings["pitch"]

        )

    )

    return str(
        output_path
    )


# =========================================================
# VOICE ENHANCEMENT
# =========================================================

def enhance_voice(

    voice_path,

    voice_style="Natural",

    pitch=0,

    speed=1.0,

    bass=0,

    treble=0,

    reverb=0

):

    voice = AudioSegment.from_file(

        voice_path

    )


    # Mono

    voice = voice.set_channels(1)


    # Remove low rumble

    voice = voice.high_pass_filter(

        70

    )


    # Voice style

    if voice_style == "Soft":

        voice = voice.low_pass_filter(
            8000
        )

        voice = voice.apply_gain(
            -1
        )


    elif voice_style == "Deep":

        voice = voice.low_pass_filter(
            7000
        )


    elif voice_style == "Warm":

        voice = voice.low_pass_filter(
            9000
        )

        voice = voice.apply_gain(
            1
        )


    elif voice_style == "Clear":

        voice = voice.high_pass_filter(
            100
        )

        voice = voice.apply_gain(
            1
        )


    # Compression

    voice = compress_dynamic_range(

        voice,

        threshold=-22,

        ratio=2.5,

        attack=5,

        release=100

    )


    # Bass

    if bass != 0:

        bass_layer = (

            voice

            .low_pass_filter(250)

            .apply_gain(bass)

        )

        voice = voice.overlay(

            bass_layer

        )


    # Treble

    if treble != 0:

        treble_layer = (

            voice

            .high_pass_filter(3000)

            .apply_gain(treble)

        )

        voice = voice.overlay(

            treble_layer

        )


    # Speed

    if speed != 1.0:

        new_rate = int(

            voice.frame_rate * speed

        )

        voice = voice._spawn(

            voice.raw_data,

            overrides={

                "frame_rate":
                new_rate

            }

        )

        voice = voice.set_frame_rate(

            44100

        )


    # Pitch

    if pitch != 0:

        factor = 2 ** (

            pitch / 12.0

        )

        new_rate = int(

            voice.frame_rate * factor

        )

        voice = voice._spawn(

            voice.raw_data,

            overrides={

                "frame_rate":
                new_rate

            }

        )

        voice = voice.set_frame_rate(

            44100

        )


    # Reverb

    if reverb > 0:

        delay = int(

            70 + reverb * 3

        )

        echo = (

            AudioSegment.silent(

                duration=delay

            )

            + voice.apply_gain(-20)

        )

        voice = voice.overlay(

            echo,

            position=delay

        )


    # Final compression

    voice = compress_dynamic_range(

        voice,

        threshold=-20,

        ratio=2.0,

        attack=5,

        release=100

    )


    # Normalize

    voice = normalize(

        voice,

        headroom=1.0

    )


    processed_path = (

        OUTPUT_DIR /

        "processed_voice.mp3"

    )


    voice.export(

        processed_path,

        format="mp3",

        bitrate="192k"

    )


    return str(

        processed_path

    )


# =========================================================
# SELECT MUSIC
# =========================================================

def select_music(

    music_name

):

    if not music_name:

        music_name = (

            "background1.mp3"

        )


    music_path = (

        MUSIC_DIR /

        music_name

    )


    if not music_path.exists():

        raise FileNotFoundError(

            f"Music file not found: "
            f"{music_path}"

        )


    return music_path


# =========================================================
# LOOP MUSIC
# =========================================================

def loop_music(

    music,

    duration

):

    if len(music) == 0:

        raise ValueError(

            "Background music is empty."

        )


    while len(music) < duration:

        music += music


    return music[

        :duration

    ]


# =========================================================
# MIX VOICE + MUSIC
# =========================================================

def mix_voice_music(

    voice_path,

    music_name,

    music_volume=-28

):

    voice = AudioSegment.from_file(

        voice_path

    )

    music_path = select_music(

        music_name

    )

    music = AudioSegment.from_file(

        music_path

    )


    voice = voice.set_channels(2)

    music = music.set_channels(2)


    intro_duration = 3000

    outro_duration = 4000


    total_duration = (

        intro_duration

        + len(voice)

        + outro_duration

    )


    music = loop_music(

        music,

        total_duration

    )


    # =====================================================
    # INTRO
    # =====================================================

    intro = music[

        :intro_duration

    ]

    intro = intro.apply_gain(

        -22

    )

    intro = intro.fade_in(

        1500

    )

    intro = intro.fade_out(

        700

    )


    # =====================================================
    # MAIN MUSIC
    # =====================================================

    main_music = music[

        intro_duration:

        intro_duration + len(voice)

    ]


    main_music = main_music.apply_gain(

        music_volume

    )


    # =====================================================
    # VOICE + MUSIC
    # =====================================================

    main_mix = main_music.overlay(

        voice

    )


    # =====================================================
    # OUTRO
    # =====================================================

    outro_start = (

        intro_duration

        + len(voice)

    )


    outro = music[

        outro_start:

        outro_start + outro_duration

    ]


    outro = outro.apply_gain(

        -22

    )


    outro = outro.fade_in(

        500

    )


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


    final_audio = normalize(

        final_audio,

        headroom=1.0

    )


    final_path = (

        OUTPUT_DIR /

        "final_output.mp3"

    )


    final_audio.export(

        final_path,

        format="mp3",

        bitrate="192k"

    )


    return str(

        final_path

    )


# =========================================================
# MAIN FUNCTION
# =========================================================

def create_poetry_audio(

    lyrics,

    music_name,

    mood="Emotional",

    voice_style="Natural",

    pitch=0,

    speed=1.0,

    bass=0,

    treble=0,

    reverb=0,

    music_volume=-28

):

    # Step 1
    ai_voice = generate_hindi_voice(

        text=lyrics,

        mood=mood

    )


    # Step 2
    processed_voice = enhance_voice(

        voice_path=ai_voice,

        voice_style=voice_style,

        pitch=pitch,

        speed=speed,

        bass=bass,

        treble=treble,

        reverb=reverb

    )


    # Step 3
    final_audio = mix_voice_music(

        voice_path=processed_voice,

        music_name=music_name,

        music_volume=music_volume

    )


    return (

        processed_voice,

        final_audio

    )
