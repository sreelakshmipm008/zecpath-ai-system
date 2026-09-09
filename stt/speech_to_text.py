"""
speech_to_text.py

Speech-to-text service using Faster-Whisper.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io import wavfile
from faster_whisper import WhisperModel

DEFAULT_MODEL = "tiny"
DEFAULT_DEVICE = "cpu"
DEFAULT_COMPUTE_TYPE = "int8"


def detect_silence(
    audio_path: str | Path,
    threshold: float = 0.02,
    window_seconds: float = 0.5,
) -> list[tuple[float, float]]:
    """
    Detect low-energy regions in a WAV audio file.

    Returns silent regions as (start_seconds, end_seconds).
    """

    sample_rate, audio = wavfile.read(str(audio_path))

    was_integer = np.issubdtype(audio.dtype, np.integer)
    max_value = np.iinfo(audio.dtype).max if was_integer else 1.0

    audio = audio.astype(np.float32)

    if audio.ndim == 2:
        audio = audio.mean(axis=1)

    if was_integer:
        audio /= max_value

    window_size = max(1, int(sample_rate * window_seconds))
    silent_regions: list[tuple[float, float]] = []

    for start in range(0, len(audio), window_size):
        end = min(start + window_size, len(audio))
        window = audio[start:end]

        if len(window) == 0:
            continue

        rms = float(np.sqrt(np.mean(window**2)))

        if rms < threshold:
            silent_regions.append(
                (
                    start / sample_rate,
                    end / sample_rate,
                )
            )

    return silent_regions


class SpeechToTextService:
    """Convert speech audio into text using Faster-Whisper."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        device: str = DEFAULT_DEVICE,
        compute_type: str = DEFAULT_COMPUTE_TYPE,
    ) -> None:
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type

        self._model = WhisperModel(
            model_name,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(
        self,
        audio: str | Path,
        language: str = "en",
        vad_filter: bool = False,
    ) -> str:
        """
        Transcribe an audio file.

        Parameters
        ----------
        audio:
            Path to the audio file.
        language:
            Expected spoken language.
        vad_filter:
            Enable voice activity detection for silence handling.

        Returns
        -------
        str
            Raw transcript.
        """

        if not isinstance(audio, (str, Path)):
            raise TypeError("audio must be a file path.")

        segments, _ = self._model.transcribe(
            str(audio),
            language=language,
            vad_filter=vad_filter,
        )

        transcript = " ".join(
            segment.text.strip()
            for segment in segments
            if segment.text.strip()
        )

        return transcript.strip()
