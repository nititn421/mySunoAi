from pathlib import Path

from pydub import AudioSegment
from pydub.effects import (
    normalize,
    compress_dynamic_range
)


# =========================================================
# FOLDERS
# =========================================================

OUTPUT_DIR = Path("outputs")
MUSIC_DIR = Path("music")

OUTPUT_DIR.mkdir(exist_ok=True)
MUSIC_DIR.mkdir(exist_ok=True)


# =========================================================
# MUSIC
# =========================================================

MUSIC_FILES = [
    f"background{i}.mp3"
    for i in range(1, 13)
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
# SPEED
# =========================================================

def change_speed(audio, speed):

    if speed == 1.0:
        return audio

    new_rate = int(
        audio.frame_rate * speed
    )

    changed = audio._spawn(
        audio.raw_data,
        overrides={
            "frame_rate": new_rate
        }
    )

    return changed.set_frame_rate(
        audio.frame_rate
    )


# =========================================================
# PITCH
# =========================================================

def change_pitch(audio, pitch):

    if pitch == 0:
        return audio

    factor = 2 ** (
        pitch / 12.0
    )

    new_rate = int(
        audio.frame_rate * factor
    )

    changed = audio._spawn(
        audio.raw_data,
        overrides={
            "frame_rate": new_rate
        }
    )

    return changed.set_frame_rate(
        audio.frame_rate
    )


# =========================================================
# REVERB
# =========================================================

def add_reverb(audio, amount):

    if amount <= 0:
        return audio

    delay = int(
        80 + amount * 4
    )

    echo = (
        AudioSegment.silent(
            duration=delay
        )
        + (audio - 18)
    )

    echo = echo[:len(audio)]

    return audio.overlay(
        echo,
        position=delay
    )


# =========================================================
# VOICE ENHANCEMENT
# =========================================================

def enhance_voice(
    voice,
    preset,
    pitch,
    speed,
    bass,
    treble,
    reverb
):

    # =====================================================
    # MONO
    # =====================================================

    voice = voice.set_channels(1)


    # =====================================================
    # NOISE REDUCTION - BASIC
    # =====================================================

    # Remove very low rumble
    voice = voice.high_pass_filter(
        70
    )


    # =====================================================
    # PRESET
    # =====================================================

    if preset == "Natural":

        voice = voice.apply_gain(
            0
        )


    elif preset == "Warm":

        voice = voice.low_pass_filter(
            9000
        )

        voice = voice.apply_gain(
            1
        )


    elif preset == "Deep":

        voice = voice.low_pass_filter(
            7500
        )

        voice = voice.apply_gain(
            1
        )


    elif preset == "Studio":

        voice = voice.high_pass_filter(
            80
        )

        voice = compress_dynamic_range(
            voice,
            threshold=-22,
            ratio=3.0,
            attack=5,
            release=100
        )

        voice = voice.apply_gain(
            1
        )


    elif preset == "Cinematic":

        voice = voice.high_pass_filter(
            70
        )

        voice = compress_dynamic_range(
            voice,
            threshold=-22,
            ratio=2.5,
            attack=5,
            release=120
        )

        voice = voice.apply_gain(
            1
        )


    # =====================================================
    # BASS
    # =====================================================

    if bass != 0:

        bass_layer = voice.low_pass_filter(
            250
        )

        bass_layer = bass_layer.apply_gain(
            bass
        )

        voice = voice.overlay(
            bass_layer
        )


    # =====================================================
    # TREBLE / CLARITY
    # =====================================================

    if treble != 0:

        treble_layer = voice.high_pass_filter(
            3000
        )

        treble_layer = treble_layer.apply_gain(
            treble
        )

        voice = voice.overlay(
            treble_layer
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
    # REVERB
    # =====================================================

    voice = add_reverb(
        voice,
        reverb
    )


    # =====================================================
    # FINAL COMPRESSION
    # =====================================================

    voice = compress_dynamic_range(
        voice,
        threshold=-20,
        ratio=2.5,
        attack=5,
        release=100
    )


    # =====================================================
    # NORMALIZE
    # =====================================================

    voice = normalize(
        voice,
        headroom=1.0
    )


    return voice


# =========================================================
# PROCESS VOICE
# =========================================================

def process_voice(
    voice_file,
    preset,
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


    voice = AudioSegment.from_file(
        voice_file
    )


    voice = enhance_voice(
        voice=voice,
        preset=preset,
        pitch=pitch,
        speed=speed,
        bass=bass,
        treble=treble,
        reverb=reverb
    )


    processed_path = (
        OUTPUT_DIR /
        "processed_voice.wav"
    )


    voice.export(
        processed_path,
        format="wav"
    )


    print(
        "✅ Voice Enhancement Completed"
    )


    return (
        voice,
        str(processed_path)
    )


# =========================================================
# MUSIC LOOP
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
# AUTOMATIC MUSIC MIX
# =========================================================

def automatic_mix(
    voice,
    music_path,
    music_volume=-28
):

    print(
        "🎵 Automatic Music Mixing..."
    )


    music = AudioSegment.from_file(
        music_path
    )


    # Stereo
    music = music.set_channels(2)

    voice = voice.set_channels(2)


    # =====================================================
    # INTRO / OUTRO
    # =====================================================

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


    # Music under voice
    main_music = main_music.apply_gain(
        music_volume
    )


    # Smooth music start
    main_music = main_music.fade_in(
        800
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


    print(
        "✅ Music Mixing Completed"
    )


    return final_audio


# =========================================================
# MAIN FUNCTION
# =========================================================

def create_poetry_audio(
    voice_file,
    music_name,
    mood,
    preset="Studio",
    pitch=0,
    speed=1.0,
    bass=0,
    treble=0,
    reverb=0,
    music_volume=-28
):

    print(
        "🎵 MySunoAI Processing Started"
    )


    # =====================================================
    # VOICE
    # =====================================================

    voice, processed_path = process_voice(
        voice_file=voice_file,
        preset=preset,
        pitch=pitch,
        speed=speed,
        bass=bass,
        treble=treble,
        reverb=reverb
    )


    # =====================================================
    # MUSIC
    # =====================================================
