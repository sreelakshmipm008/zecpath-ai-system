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

    # Common screening-domain terms that can express the same intent
    # without repeating the exact wording of the question.
    TERM_GROUPS = {
        "human resources": {"human resources", "hr", "human resource"},
        "accounting": {
            "accounting",
            "accountant",
            "bookkeeping",
            "bookkeeping software",
            "financial records",
        },
        "tally": {"tally", "accounting software", "bookkeeping software"},
        "terraform": {
            "terraform",
            "infrastructure automation",
            "infrastructure as code",
            "iac",
        },
        "patient care": {
            "patient care",
            "patients",
            "healthcare",
            "clinical care",
            "nursing care",
        },
        "network security": {
            "network security",
            "network protection",
            "network monitoring",
            "cybersecurity",
        },
        "recruitment": {
            "recruitment",
            "recruiting",
            "hiring",
            "candidate screening",
        },
        "crm": {
            "crm",
            "customer relationship management",
            "customer management",
        },
        "lead generation": {
            "lead generation",
            "lead generation activities",
            "prospecting",
            "finding leads",
        },
        "wireframing": {
            "wireframing",
            "wireframes",
            "interface sketches",
            "layout design",
        },
    }

    def classify(self, answer: str, question: str = "") -> str:
        """
        Classify a candidate answer based on its intent relative to the question.
        """
        if not isinstance(answer, str):
            raise TypeError("answer must be a string")

        answer = answer.strip()

        if not answer:
            return self.MISSING

        # A direct yes/no response is valid when the question itself
        # expects a yes/no answer.
        if self._is_yes_no_answer(answer) and self._is_yes_no_question(question):
            return self.ON_TOPIC

        if self._is_vague(answer):
            return self.VAGUE

        if question and self._is_off_topic(answer, question):
            return self.OFF_TOPIC

        return self.ON_TOPIC

    @staticmethod
    def _is_yes_no_answer(answer: str) -> bool:
        """Return True when the answer is a direct yes/no response."""
        normalized = answer.strip().lower().rstrip(".!?")

        return normalized in {"yes", "no"}

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

    @classmethod
    def _is_off_topic(cls, answer: str, question: str) -> bool:
        """
        Detect obvious topic mismatch using meaningful question terms.

        Exact word overlap is checked first. If no direct overlap exists,
        known screening-domain synonym groups are checked before marking
        the answer as off-topic.
        """
        question_normalized = question.lower()
        answer_normalized = answer.lower()

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

        if question_words.intersection(answer_words):
            return False

        for terms in cls.TERM_GROUPS.values():
            question_has_group = any(
                term in question_normalized
                for term in terms
            )

            answer_has_group = any(
                term in answer_normalized
                for term in terms
            )

            if question_has_group and answer_has_group:
                return False

        return True