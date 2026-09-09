"""
transcript_normalizer.py

Normalizes speech-to-text transcripts for AI screening analysis.
"""

from __future__ import annotations

from pathlib import Path

from stt.speech_to_text import detect_silence

import re


# Common conversational filler words that normally do not add
# meaningful information to a screening response.
FILLER_WORDS = {
    "um",
    "uh",
    "erm",
    "hmm",
    "hm",
    "mm",
    "mhm",
}


def remove_filler_words(text: str) -> str:
    """Remove common filler words and clean punctuation left behind."""
    if not text:
        return ""

    pattern = r"\b(?:" + "|".join(
        re.escape(word)
        for word in sorted(FILLER_WORDS, key=len, reverse=True)
    ) + r")\b"

    text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    # Remove punctuation that becomes duplicated after filler removal.
    text = re.sub(r",\s*,+", ",", text)
    text = re.sub(r",\s+([.!?])", r"\1", text)

    # Remove punctuation left at the beginning of the transcript.
    text = re.sub(r"^\s*[.,!?;:]+\s*", "", text)

    # Remove punctuation immediately before the end of the transcript.
    text = re.sub(r"\s+([.,!?;:])$", r"\1", text)

    # Normalize remaining whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_whitespace(text: str) -> str:
    """Collapse unnecessary whitespace."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return text.strip()


def normalize_punctuation(text: str) -> str:
    """Clean repeated punctuation and normalize sentence endings."""
    text = re.sub(r"([.!?,])\1+", r"\1", text)
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"([,.!?;:])([A-Za-z])", r"\1 \2", text)

    return text.strip()


def normalize_case(text: str) -> str:
    """
    Normalize transcript text to sentence case while preserving
    common technical terms and identifiers.
    """
    text = text.strip()

    if not text:
        return ""

    technical_terms = {
        "python": "Python",
        "sql": "SQL",
        "pandas": "Pandas",
        "numpy": "NumPy",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "aws": "AWS",
        "azure": "Azure",
        "gcp": "GCP",
        "api": "API",
        "ai": "AI",
        "ml": "ML",
        "nlp": "NLP",
        "excel": "Excel",
        "powerbi": "Power BI",
        "tableau": "Tableau",
        "github": "GitHub",
        "git": "Git",
    }

    text = text.lower()

    for term, replacement in technical_terms.items():
        pattern = rf"\b{re.escape(term)}\b"
        text = re.sub(
            pattern,
            replacement,
            text,
            flags=re.IGNORECASE,
        )

    # Capitalize the beginning of each sentence.
    text = re.sub(
        r"(^|[.!?]\s+)([a-z])",
        lambda match: match.group(1) + match.group(2).upper(),
        text,
    )

    return text


def normalize_transcript(text: str) -> str:
    """
    Apply the complete transcript normalization pipeline.

    Order:
    1. Whitespace cleanup
    2. Filler-word removal
    3. Punctuation normalization
    4. Case normalization
    5. Final whitespace cleanup
    """
    if not isinstance(text, str):
        raise TypeError("Transcript text must be a string.")

    text = normalize_whitespace(text)
    text = remove_filler_words(text)
    text = normalize_punctuation(text)
    text = normalize_case(text)
    text = normalize_whitespace(text)

    return text


def test_detects_silence_in_audio_fixture():
    audio_path = (
        Path(__file__).resolve().parents[2]
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
