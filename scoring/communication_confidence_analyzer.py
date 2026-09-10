"""
Communication confidence and behavioral analysis.

Day 27:
- Detect hesitation patterns.
- Measure response length and pace.
- Detect uncertainty.
- Detect contradictions.
- Create communication strength indicators.

This module evaluates observable communication signals.
It does not attempt to determine a candidate's psychological state.
"""

from __future__ import annotations

import re
from typing import Any


class CommunicationConfidenceAnalyzer:
    """Analyze observable communication and behavioral signals."""

    HESITATION_WORDS = {
        "um",
        "uh",
        "uhh",
        "umm",
        "er",
        "err",
        "hmm",
        "hm",
        "well",
        "actually",
        "basically",
        "like",
        "you know",
        "i mean",
    }

    UNCERTAINTY_PHRASES = {
        "i think",
        "i guess",
        "maybe",
        "perhaps",
        "probably",
        "possibly",
        "not sure",
        "i'm not sure",
        "i am not sure",
        "i don't know",
        "i do not know",
        "as far as i know",
        "i believe",
        "i suppose",
        "might be",
        "could be",
    }

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Return normalized word tokens."""
        return re.findall(r"\b[\w+#.-]+\b", text.lower())

    @staticmethod
    def _normalize_score(score: float) -> float:
        """Keep a score within the 0-100 range."""
        return round(max(0.0, min(100.0, score)), 2)

    def analyze(
        self,
        answer: str,
        duration_seconds: float | None = None,
    ) -> dict[str, Any]:
        """
        Analyze one candidate response.

        Parameters
        ----------
        answer:
            Candidate's response text.

        duration_seconds:
            Optional duration of the spoken response in seconds.
            When supplied, words-per-minute can be calculated.

        Returns
        -------
        dict[str, Any]
            Behavioral and communication indicators.
        """

        if not isinstance(answer, str):
            raise TypeError("Answer must be a string.")

        answer = answer.strip()

        if duration_seconds is not None:
            if not isinstance(duration_seconds, (int, float)):
                raise TypeError(
                    "duration_seconds must be a number or None."
                )

            if duration_seconds < 0:
                raise ValueError(
                    "duration_seconds cannot be negative."
                )

        hesitation = self.detect_hesitation(answer)
        response_length = self.measure_response_length(answer)
        response_pace = self.measure_response_pace(
            answer,
            duration_seconds,
        )
        uncertainty = self.detect_uncertainty(answer)
        contradictions = self.detect_contradictions(answer)
        communication_strength = self.calculate_communication_strength(
            hesitation_score=hesitation["score"],
            length_score=response_length["score"],
            pace_score=response_pace["score"],
            uncertainty_score=uncertainty["score"],
            contradiction_score=contradictions["score"],
        )

        return {
            "answer": answer,
            "hesitation": hesitation,
            "response_length": response_length,
            "response_pace": response_pace,
            "uncertainty": uncertainty,
            "contradictions": contradictions,
            "communication_strength": communication_strength,
        }

    def detect_hesitation(
        self,
        answer: str,
    ) -> dict[str, Any]:
        """
        Detect textual hesitation patterns.

        Signals include filler words/phrases and repeated words.
        """

        if not answer:
            return {
                "detected": False,
                "count": 0,
                "patterns": [],
                "score": 0.0,
            }

        normalized = answer.lower()
        tokens = self._tokenize(answer)

        detected_patterns: list[str] = []
        count = 0

        for phrase in sorted(
            self.HESITATION_WORDS,
            key=len,
            reverse=True,
        ):
            if " " in phrase:
                matches = re.findall(
                    rf"\b{re.escape(phrase)}\b",
                    normalized,
                )
                if matches:
                    count += len(matches)
                    detected_patterns.append(phrase)

        single_word_hesitations = {
            phrase
            for phrase in self.HESITATION_WORDS
            if " " not in phrase
        }

        for token in tokens:
            if token in single_word_hesitations:
                count += 1
                if token not in detected_patterns:
                    detected_patterns.append(token)

        repeated_words = []

        for index in range(1, len(tokens)):
            if tokens[index] == tokens[index - 1]:
                repeated_words.append(tokens[index])

        if repeated_words:
            count += len(repeated_words)
            detected_patterns.extend(
                f"repeated:{word}"
                for word in repeated_words
            )

        word_count = len(tokens)

        if count == 0:
            score = 100.0
        else:
            rate = count / max(word_count, 1)

            if rate <= 0.03:
                score = 85.0
            elif rate <= 0.07:
                score = 70.0
            elif rate <= 0.12:
                score = 50.0
            else:
                score = 30.0

        return {
            "detected": count > 0,
            "count": count,
            "patterns": sorted(set(detected_patterns)),
            "score": self._normalize_score(score),
        }

    def measure_response_length(
        self,
        answer: str,
    ) -> dict[str, Any]:
        """Measure response length using word count and sentence count."""

        if not answer:
            return {
                "word_count": 0,
                "sentence_count": 0,
                "character_count": 0,
                "score": 0.0,
            }

        tokens = self._tokenize(answer)

        sentences = [
            sentence
            for sentence in re.split(
                r"[.!?]+",
                answer,
            )
            if sentence.strip()
        ]

        word_count = len(tokens)
        sentence_count = len(sentences)
        character_count = len(answer)

        if word_count == 0:
            score = 0.0
        elif word_count < 5:
            score = 40.0
        elif word_count < 10:
            score = 60.0
        elif word_count <= 100:
            score = 100.0
        elif word_count <= 150:
            score = 85.0
        else:
            score = 70.0

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "character_count": character_count,
            "score": self._normalize_score(score),
        }

    def measure_response_pace(
        self,
        answer: str,
        duration_seconds: float | None = None,
    ) -> dict[str, Any]:
        """
        Measure response pace.

        If duration is available, calculate words per minute.
        Without duration, pace cannot be calculated reliably and
        the result explicitly reports that timing data is unavailable.
        """

        word_count = len(self._tokenize(answer))

        if not answer:
            return {
                "available": False,
                "words_per_minute": None,
                "duration_seconds": duration_seconds,
                "score": 0.0,
            }

        if duration_seconds is None or duration_seconds == 0:
            return {
                "available": False,
                "words_per_minute": None,
                "duration_seconds": duration_seconds,
                "score": None,
            }

        words_per_minute = (
            word_count / duration_seconds
        ) * 60.0

        # A practical communication-range indicator.
        # This measures speaking pace, not confidence.
        if 110 <= words_per_minute <= 160:
            score = 100.0
        elif 90 <= words_per_minute < 110:
            score = 85.0
        elif 160 < words_per_minute <= 180:
            score = 85.0
        elif 70 <= words_per_minute < 90:
            score = 65.0
        elif 180 < words_per_minute <= 200:
            score = 65.0
        else:
            score = 45.0

        return {
            "available": True,
            "words_per_minute": round(
                words_per_minute,
                2,
            ),
            "duration_seconds": round(
                float(duration_seconds),
                2,
            ),
            "score": self._normalize_score(score),
        }

    def detect_uncertainty(
        self,
        answer: str,
    ) -> dict[str, Any]:
        """Detect explicit uncertainty phrases."""

        if not answer:
            return {
                "detected": False,
                "count": 0,
                "phrases": [],
                "score": 100.0,
            }

        normalized = answer.lower()
        detected = []

        for phrase in sorted(
            self.UNCERTAINTY_PHRASES,
            key=len,
            reverse=True,
        ):
            if re.search(
                rf"\b{re.escape(phrase)}\b",
                normalized,
            ):
                detected.append(phrase)

        count = len(detected)

        if count == 0:
            score = 100.0
        elif count == 1:
            score = 80.0
        elif count == 2:
            score = 65.0
        else:
            score = 45.0

        return {
            "detected": count > 0,
            "count": count,
            "phrases": detected,
            "score": self._normalize_score(score),
        }

    def detect_contradictions(
        self,
        answer: str,
    ) -> dict[str, Any]:
        """
        Detect simple internally contradictory statements.

        The checks focus on observable numeric experience and
        availability statements already relevant to screening.
        """

        if not answer:
            return {
                "detected": False,
                "count": 0,
                "types": [],
                "score": 0.0,
            }

        normalized = answer.lower()
        contradiction_types = []

        years = re.findall(
            r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
            normalized,
        )

        numeric_years = {
            float(value)
            for value in years
        }

        if len(numeric_years) > 1:
            contradiction_types.append(
                "conflicting_experience_years"
            )

        immediate_available = bool(
            re.search(
                r"\bimmediately\b",
                normalized,
            )
            or re.search(
                r"\bavailable\s+immediately\b",
                normalized,
            )
        )

        notice_period = bool(
            re.search(
                r"\b\d+\s+(?:days?|weeks?)\s+notice\b",
                normalized,
            )
            or re.search(
                r"\bnotice\s+period\b",
                normalized,
            )
        )

        if immediate_available and notice_period:
            contradiction_types.append(
                "conflicting_availability"
            )

        contradiction_count = len(contradiction_types)

        if contradiction_count == 0:
            score = 100.0
        elif contradiction_count == 1:
            score = 70.0
        else:
            score = 40.0

        return {
            "detected": contradiction_count > 0,
            "count": contradiction_count,
            "types": contradiction_types,
            "score": self._normalize_score(score),
        }

    def calculate_communication_strength(
        self,
        hesitation_score: float,
        length_score: float,
        pace_score: float | None,
        uncertainty_score: float,
        contradiction_score: float,
    ) -> dict[str, Any]:
        """
        Calculate an overall observable communication-strength indicator.

        When pace data is unavailable, the score is calculated from
        the remaining four observable indicators.
        """

        scores = [
            hesitation_score,
            length_score,
            uncertainty_score,
            contradiction_score,
        ]

        if pace_score is not None:
            scores.append(pace_score)

        overall_score = sum(scores) / len(scores)

        overall_score = self._normalize_score(
            overall_score
        )

        if overall_score >= 80:
            level = "strong"
        elif overall_score >= 60:
            level = "moderate"
        else:
            level = "needs_improvement"

        return {
            "score": overall_score,
            "level": level,
            "signals_used": len(scores),
        }