"""
Rule-based sentiment scoring for interview responses.

Day 27:
- Identify positive sentiment.
- Identify negative sentiment.
- Provide a transparent sentiment score.

This module uses a lightweight rule-based approach and does not
require external sentiment-analysis libraries.
"""

from __future__ import annotations

import re
from typing import Any


class SentimentScorer:
    """Analyze positive and negative sentiment in a text response."""

    POSITIVE_WORDS = {
        "achieved",
        "achievement",
        "confident",
        "excellent",
        "good",
        "great",
        "happy",
        "improved",
        "improvement",
        "success",
        "successful",
        "strong",
        "support",
        "supported",
        "enjoy",
        "enjoyed",
        "effective",
        "efficient",
        "motivated",
        "positive",
        "solved",
        "solve",
        "helpful",
        "progress",
        "proud",
    }

    NEGATIVE_WORDS = {
        "bad",
        "difficult",
        "difficulty",
        "failed",
        "failure",
        "frustrated",
        "frustrating",
        "hate",
        "problem",
        "problems",
        "negative",
        "poor",
        "weak",
        "worried",
        "worry",
        "confused",
        "confusing",
        "unable",
        "issue",
        "issues",
        "mistake",
        "mistakes",
        "disappointed",
        "disappointing",
        "struggle",
        "struggled",
    }

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Return normalized word tokens."""
        return re.findall(r"\b[\w+#.-]+\b", text.lower())

    @staticmethod
    def _normalize_score(score: float) -> float:
        """Keep sentiment score within -1 to 1."""
        return round(max(-1.0, min(1.0, score)), 2)

    def analyze(self, text: str) -> dict[str, Any]:
        """
        Analyze sentiment in a text response.

        Returns a polarity score from -1 to 1:
        - Negative values indicate negative sentiment.
        - Positive values indicate positive sentiment.
        - Zero indicates neutral or balanced sentiment.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        text = text.strip()

        if not text:
            return {
                "sentiment": "neutral",
                "score": 0.0,
                "positive_count": 0,
                "negative_count": 0,
                "positive_words": [],
                "negative_words": [],
            }

        tokens = self._tokenize(text)

        positive_words = [
            token for token in tokens if token in self.POSITIVE_WORDS
        ]
        negative_words = [
            token for token in tokens if token in self.NEGATIVE_WORDS
        ]

        positive_count = len(positive_words)
        negative_count = len(negative_words)
        total_matches = positive_count + negative_count

        if total_matches == 0:
            score = 0.0
        else:
            score = (positive_count - negative_count) / total_matches

        score = self._normalize_score(score)

        if score > 0:
            sentiment = "positive"
        elif score < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "score": score,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "positive_words": positive_words,
            "negative_words": negative_words,
        }