"""
Intent classification for candidate screening answers.
"""

from __future__ import annotations

import re


class IntentClassifier:
    """Classify the basic intent/status of a candidate answer."""

    MISSING = "missing"
    VAGUE = "vague"
    OFF_TOPIC = "off_topic"
    ON_TOPIC = "on_topic"

    def classify(self, answer: str, question: str = "") -> str:
        """
        Classify a candidate answer as missing, vague, off-topic, or on-topic.
        """
        if not isinstance(answer, str):
            raise TypeError("Answer must be a string.")

        answer = answer.strip()

        if not answer:
            return self.MISSING

        if self._is_yes_no_answer(answer) and self._is_yes_no_question(question):
            return self.ON_TOPIC

        if self._is_vague(answer):
            return self.VAGUE

        if question and self._is_off_topic(answer, question):
            return self.OFF_TOPIC

        return self.ON_TOPIC

    @staticmethod
    def _is_yes_no_answer(answer: str) -> bool:
        """Detect a direct yes/no candidate response."""
        return answer.lower().strip() in {"yes", "no"}

    @staticmethod
    def _is_yes_no_question(question: str) -> bool:
        """Detect questions that expect a yes/no response."""
        normalized = question.lower().strip()

        yes_no_starts = (
            "do ",
            "does ",
            "did ",
            "are ",
            "is ",
            "can ",
            "could ",
            "have ",
            "has ",
            "will ",
            "would ",
            "were ",
            "was ",
        )

        return normalized.startswith(yes_no_starts)

    @staticmethod
    def _is_vague(answer: str) -> bool:
        """Detect answers that provide little or no useful information."""
        vague_patterns = [
            r"^i don't know\.?$",
            r"^not sure\.?$",
            r"^maybe\.?$",
            r"^perhaps\.?$",
            r"^nothing\.?$",
            r"^no idea\.?$",
            r"^it depends\.?$",
            r"^some experience\.?$",
            r"^yes\.?$",
            r"^no\.?$",
        ]

        normalized = answer.lower().strip()

        return any(
            re.fullmatch(pattern, normalized)
            for pattern in vague_patterns
        )

    @staticmethod
    def _is_off_topic(answer: str, question: str) -> bool:
        """
        Detect obvious topic mismatch using meaningful question terms.

        This deliberately uses a lightweight rule-based approach because
        the Day 25 task does not specify an external NLP/LLM dependency.
        """
        question_words = {
            word.lower()
            for word in re.findall(r"[A-Za-z0-9+#.]+", question)
            if len(word) > 3
        }

        answer_words = {
            word.lower()
            for word in re.findall(r"[A-Za-z0-9+#.]+", answer)
        }

        if not question_words:
            return False

        return not question_words.intersection(answer_words)
        