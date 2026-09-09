"""
clean_transcript_processor.py

Processes raw speech audio into clean text suitable for AI analysis.
"""

from __future__ import annotations

from pathlib import Path

from stt.speech_to_text import SpeechToTextService
from stt.transcript_normalizer import normalize_transcript


class CleanTranscriptProcessor:
    """Convert speech audio into normalized transcript text."""

    def __init__(
        self,
        stt_service: SpeechToTextService | None = None,
    ) -> None:
        self.stt_service = stt_service or SpeechToTextService()

    def process(
        self,
        audio: str | Path,
        language: str = "en",
        vad_filter: bool = False,
    ) -> str:
        """
        Transcribe audio and normalize the resulting transcript.

        Parameters
        ----------
        audio:
            Path to the audio file.
        language:
            Expected spoken language.
        vad_filter:
            Enable Faster-Whisper voice activity detection.

        Returns
        -------
        str
            Clean transcript suitable for AI analysis.
        """

        raw_transcript = self.stt_service.transcribe(
            audio,
            language=language,
            vad_filter=vad_filter,
        )

        return normalize_transcript(raw_transcript)