from pathlib import Path

from stt.speech_to_text import detect_silence
from stt.transcript_normalizer import normalize_transcript

def test_removes_filler_words():
    text = "um I have experience in Python uh"
    assert normalize_transcript(text) == "I have experience in Python"


def test_normalizes_whitespace():
    text = "  I   am   a   data analyst  "
    assert normalize_transcript(text) == "I am a data analyst"


def test_normalizes_punctuation():
    text = "I have experience in SQL!!!"
    assert normalize_transcript(text) == "I have experience in SQL!"


def test_removes_leading_filler_punctuation():
    text = "hmm... i worked with AWS??"
    assert normalize_transcript(text) == "I worked with AWS?"


def test_empty_filler_transcript():
    text = "um uh hmm"
    assert normalize_transcript(text) == ""

def test_detects_silence_in_audio_fixture():
    audio_path = (
        Path(__file__).resolve().parents[4]
        / "day24"
        / "silence_speech.wav"
    )

    silent_regions = detect_silence(
        audio_path,
        threshold=0.02,
        window_seconds=0.5,
    )

    assert silent_regions
    assert len(silent_regions) == 6

    # The fixture becomes low-energy at approximately 2.5 seconds.
    assert silent_regions[0][0] == 2.5
    assert silent_regions[-1][1] == 5.28