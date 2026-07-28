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
# GENERATE HINDI AI VOICE
# =========================================================

async def generate_voice_async(
    text,
    output_path,
    rate="+0%",
    pitch="+0Hz"
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
    rate="+0%",
    pitch="+0Hz"
):

    if not text or not text.strip():

        raise ValueError(
            "Please enter your poetry."
        )


    output_path = (
        OUTPUT_DIR /
        "ai_voice.mp3"
    )


    asyncio.run(
        generate_voice_async(
            text=text,
            output_path=output_path,
            rate=rate,
            pitch=pitch
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


    # Compression
    voice = compress_dynamic_range(
        voice,
        threshold=-20,
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


    # Treble / Clarity
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
                "frame_rate": new_rate
            }
        )

        voice = voice.set_frame_rate(
            44100
        )


    # Pitch
    if pitch != 0:

        factor = 2 ** (
            pitch / 12
        )

        new_rate = int(
            voice.frame_rate * factor
        )

        voice = voice._spawn(
            voice.raw_data,
            overrides={
                "frame_rate": new_rate
            }
        )

        voice = voice.set_frame_rate(
            44100
        )


    # Reverb
    if reverb > 0:

        delay = int(
            80 + reverb * 4
        )

        echo = (
            AudioSegment.silent(
                duration=delay
            )
            + voice.apply_gain(-18)
        )

        echo = echo[
            :len(voice)
        ]

        voice = voice.overlay(
            echo,
            position=delay
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
# MUSIC
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
            f"Music file not found: {music_path}"
        )


    return music_path


# =========================================================
# LOOP MUSIC
# =========================================================

def loop_music(
    music,
    duration
):

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


    voice = voice.set_channels(
        2
    )

    music = music.set_channels(
        2
    )


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


    # Intro
    intro = music[
        :intro_duration
    ]

    intro = intro.apply_gain(
        -22
    )

    intro = intro.fade_in(
        1500
    )


    # Main music
    main_music = music[
        intro_duration:
        intro_duration + len(voice)
    ]


    main_music = main_music.apply_gain(
        music_volume
    )


    # Voice + music
    main_mix = main_music.overlay(
        voice
    )


    # Outro
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


    outro = outro.fade_out(
        outro_duration
    )


    # Final
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
    pitch=0,
    speed=1.0,
    bass=0,
    treble=0,
    reverb=0,
    music_volume=-28
):

    # STEP 1
    ai_voice = generate_hindi_voice(
        text=lyrics
    )


    # STEP 2
    processed_voice = enhance_voice(
        voice_path=ai_voice,
        pitch=pitch,
        speed=speed,
        bass=bass,
        treble=treble,
        reverb=reverb
    )


    # STEP 3
    final_audio = mix_voice_music(
        voice_path=processed_voice,
        music_name=music_name,
        music_volume=music_volume
    )


    return (
        processed_voice,
        final_audio
    )
