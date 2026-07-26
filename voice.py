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
# CHANGE SPEED
# =========================================================

def change_speed(audio, speed=1.0):

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
# SIMPLE PITCH CHANGE
# =========================================================

def change_pitch(audio, pitch=0):

    if pitch == 0:
        return audio

    new_frame_rate = int(
        audio.frame_rate *
        (2.0 ** (pitch / 12.0))
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
# SIMPLE REVERB
# =========================================================

def add_reverb(audio, reverb_level=10):

    if reverb_level <= 0:
        return audio

    delay = int(
        40 + (reverb_level * 3)
    )

    echo = AudioSegment.silent(
        duration=delay
    ) + (
        audio - 12
    )

    reverb = audio.overlay(
        echo
    )

    return reverb


# =========================================================
# PROCESS VOICE
# =========================================================

def process_voice(
    voice_file,
    voice_tone="Emotional",
    pitch=0,
    speed=1.0,
    bass=0,
    treble=0,
    reverb=10
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

    # Convert to mono
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

        voice = voice.apply_gain(
            1
        )

    elif voice_tone == "Soft":

        voice = voice.low_pass_filter(
            7500
        )

        voice = voice.apply_gain(
            -1
        )

    elif voice_tone == "Warm":

        voice = voice.low_pass_filter(
            9000
        )

        voice = voice.apply_gain(
            1
        )

    elif voice_tone == "Clear":

        voice = voice.high_pass_filter(
            80
        )

        voice = voice.apply_gain(
            1
        )

    elif voice_tone == "Emotional":

        voice = voice.high_pass_filter(
            70
        )

    # =====================================================
    # BASS
    # =====================================================

    if bass != 0:

        voice = voice.low_pass_filter(
            12000
        )

        voice = voice.apply_gain(
            bass * 0.5
        )

    # =====================================================
    # TREBLE
    # =====================================================

    if treble != 0:

        voice = voice.high_pass_filter(
            100
        )

        voice = voice.apply_gain(
            treble * 0.3
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

    # Final normalize
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
# MUSIC LOOP
# =========================================================

def loop_music(
    music,
    required_length
):

    if len(music) == 0:

        raise ValueError(
            "Background music is empty."
        )

    while len(music) < required_length:

        music += music

    return music[
        :required_length
    ]


# =========================================================
# AUTOMATIC MUSIC DUCKING
# =========================================================

def duck_music(
    music,
    voice,
    music_volume=-26
):

    # Music volume during voice
    music = music.apply_gain(
        music_volume
    )

    # Create music bed
    music_bed = AudioSegment.silent(
        duration=len(voice)
    )

    # Add music
    music_bed = music_bed.overlay(
        music[:len(voice)]
    )

    # Voice starts normally
    result = music_bed.overlay(
        voice
    )

    return result


# =========================================================
# AUTOMATIC MIXING
# =========================================================

def automatic_mix(
    voice,
    music_path
):

    print(
        "🎵 Starting Automatic Music Sync..."
    )

    # Load music
    music = AudioSegment.from_file(
        music_path
    )

    # Convert music to stereo
    music = music.set_channels(
        2
    )

    # Convert voice to stereo
    voice = voice.set_channels(
        2
    )

    # =====================================================
    # INTRO / OUTRO
    # =====================================================

    intro_duration = 3000
    outro_duration = 4000

    required_length = (
        intro_duration
        + len(voice)
        + outro_duration
    )

    # Loop music
    music = loop_music(
        music,
        required_length
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
        500
    )

    # =====================================================
    # MAIN MUSIC
    # =====================================================

    main_music = music[
        intro_duration:
        intro_duration + len(voice)
    ]

    # Music volume
    main_music = main_music.apply_gain(
        -27
    )

    # =====================================================
    # MUSIC FADE IN
    # =====================================================

    main_music = main_music.fade_in(
        1000
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

    # Final normalize
    final_audio = normalize(
        final_audio,
        headroom=1.0
    )

    print(
        "✅ Automatic Music Sync Completed"
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
    reverb=10
):

    print(
        "\n=============================="
    )

    print(
        "🎵 MySunoAI Processing Started"
    )

    print(
        f"😊 Mood: {mood}"
    )

    print(
        f"🎙️ Voice Tone: {voice_tone}"
    )

    print(
        f"🎚️ Pitch: {pitch}"
    )

    print(
        f"⏩ Speed: {speed}x"
    )

    print(
        f"🔊 Bass: {bass}"
    )

    print(
        f"✨ Treble: {treble}"
    )

    print(
        f"🌊 Reverb: {reverb}"
    )

    print(
        "=============================="
    )

    # =====================================================
    # STEP 1
    # =====================================================

    voice, processed_voice_path = (
        process_voice(
            voice_file=voice_file,
            voice_tone=voice_tone,
            pitch=pitch,
            speed=speed,
            bass=bass,
            treble=treble,
            reverb=reverb
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
