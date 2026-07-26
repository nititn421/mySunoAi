from pathlib import Path

import numpy as np
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
# MUSIC FILES
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
# SELECT MUSIC
# =========================================================

def select_music(music_name):

    if not music_name:
        music_name = "background1.mp3"

    music_path = MUSIC_DIR / music_name

    if not music_path.exists():
        raise FileNotFoundError(
            f"Music file not found: {music_path}"
        )

    return music_path


# =========================================================
# SPEED CONTROL
# =========================================================

def change_speed(audio, speed):

    if speed == 1.0:
        return audio

    new_frame_rate = int(
        audio.frame_rate * speed
    )

    changed = audio._spawn(
        audio.raw_data,
        overrides={
            "frame_rate": new_frame_rate
        }
    )

    return changed.set_frame_rate(
        audio.frame_rate
    )


# =========================================================
# PITCH CONTROL
# =========================================================

def change_pitch(audio, semitones):

    if semitones == 0:
        return audio

    factor = 2 ** (
        semitones / 12.0
    )

    new_frame_rate = int(
        audio.frame_rate * factor
    )

    pitched = audio._spawn(
        audio.raw_data,
        overrides={
            "frame_rate": new_frame_rate
        }
    )

    return pitched.set_frame_rate(
        audio.frame_rate
    )


# =========================================================
# BASS CONTROL
# =========================================================

def change_bass(audio, bass):

    if bass == 0:
        return audio

    if bass > 0:

        boosted = audio.low_pass_filter(
            250
        )

        boosted = boosted + bass

        return audio.overlay(
            boosted
        )

    return audio


# =========================================================
# TREBLE CONTROL
# =========================================================

def change_treble(audio, treble):

    if treble == 0:
        return audio

    if treble > 0:

        high = audio.high_pass_filter(
            3000
        )

        high = high + treble

        return audio.overlay(
            high
        )

    return audio


# =========================================================
# REVERB
# =========================================================

def add_reverb(audio, amount):

    if amount <= 0:
        return audio

    delay1 = audio.delay(
        120
    ) if hasattr(audio, "delay") else None

    # Simple echo simulation
    echo1 = AudioSegment.silent(
        duration=len(audio) + 120
    )

    echo1 = echo1.overlay(
        audio,
        position=120
    )

    echo1 = echo1 - (30 - amount)

    result = audio.overlay(
        echo1
    )

    return result[:len(audio)]


# =========================================================
# PROCESS VOICE
# =========================================================

def process_voice(
    voice_file,
    voice_tone,
    pitch,
    speed,
    bass,
    treble,
    reverb
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


    # =====================================================
    # PITCH
    # =====================================================

    voice = change_pitch(
        voice,
        pitch
    )


    # =====================================================
    # SPEED
    # =====================================================

    voice = change_speed(
        voice,
        speed
    )


    # =====================================================
    # BASS
    # =====================================================

    voice = change_bass(
        voice,
        bass
    )


    # =====================================================
    # TREBLE
    # =====================================================

    voice = change_treble(
        voice,
        treble
    )


    # =====================================================
    # REVERB
    # =====================================================

    voice = add_reverb(
        voice,
        reverb
    )


    # Final Normalize

    voice = normalize(
        voice,
        headroom=1.0
    )


    # Save

    processed_voice_path = (

        OUTPUT_DIR /

        "processed_voice.wav"

    )


    voice.export(

        processed_voice_path,

        format="wav"

    )


    print(
        "✅ Voice Processing Completed"
    )


    return (

        voice,

        str(processed_voice_path)

    )


# =========================================================
# AUTOMATIC MUSIC MIXING
# =========================================================

def automatic_mix(

    voice,

    music_path

):

    print(
        "🎵 Starting Automatic Mixing..."
    )


    music = AudioSegment.from_file(
        music_path
    )


    intro_duration = 3000

    outro_duration = 3000


    required_length = (

        intro_duration

        + len(voice)

        + outro_duration

    )


    # Loop music

    while len(music) < required_length:

        music += music


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
    # FINAL
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


    return final_audio


# =========================================================
# MAIN FUNCTION
# =========================================================

def create_poetry_audio(

    voice_file,

    music_name,

    mood,

    voice_tone,

    pitch=0,

    speed=1.0,

    bass=0,

    treble=0,

    reverb=0

):


    print(
        "🎵 MySunoAI Processing Started"
    )


    # Process Voice

    voice, processed_voice_path = (

        process_voice(

            voice_file,

            voice_tone,

            pitch,

            speed,

            bass,

            treble,

            reverb

        )

    )


    # Select Music

    music_path = select_music(
        music_name
    )


    # Automatic Mix

    final_audio = automatic_mix(

        voice,

        music_path

    )


    # Save Final

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
        "🎧 Final Audio Generated"
    )


    return (

        processed_voice_path,

        str(final_path)

    )
