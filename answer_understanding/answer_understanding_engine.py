"""
Answer understanding engine for candidate screening responses.
"""

from __future__ import annotations

import re
from typing import Any

from .intent_classifier import IntentClassifier


class AnswerUnderstandingEngine:
    """Convert a candidate's screening answer into a structured object."""

    def __init__(self) -> None:
        self.intent_classifier = IntentClassifier()

    def understand(
        self,
        answer: str,
        question: str = "",
    ) -> dict[str, Any]:
        """
        Understand a candidate answer and return a structured semantic object.
        """
        if not isinstance(answer, str):
            raise TypeError("Answer must be a string.")

        answer = answer.strip()

        intent = self.intent_classifier.classify(
            answer=answer,
            question=question,
        )

        result = {
            "answer": answer,
            "intent": intent,
            "skills": self.extract_skills(answer),
            "experience": self.extract_experience(answer),
            "availability": self.extract_availability(answer),
            "salary_expectation": self.extract_salary(answer),
        }

        return result

    @staticmethod
    def extract_skills(answer: str) -> list[str]:
        """Extract commonly mentioned technical skills."""
        skill_patterns = [
            "python",
            "java",
            "javascript",
            "typescript",
            "sql",
            "excel",
            "power bi",
            "tableau",
            "pandas",
            "numpy",
            "tensorflow",
            "pytorch",
            "aws",
            "azure",
            "gcp",
            "docker",
            "kubernetes",
            "git",
            "github",
            "machine learning",
            "deep learning",
            "nlp",
            "data analysis",
        ]

        normalized = answer.lower()
        found_skills = []

        for skill in skill_patterns:
            if re.search(
                rf"(?<!\w){re.escape(skill)}(?!\w)",
                normalized,
            ):
                found_skills.append(skill)

        return found_skills

    @staticmethod
    def extract_experience(answer: str) -> dict[str, Any] | None:
        """Extract years or months of professional experience."""
        patterns = [
            (
                r"(\d+(?:\.\d+)?)\s*"
                r"(?:years?|yrs?)",
                "years",
            ),
            (
                r"(\d+(?:\.\d+)?)\s*"
                r"(?:months?|mos?)",
                "months",
            ),
        ]

        normalized = answer.lower()

        for pattern, unit in patterns:
            match = re.search(pattern, normalized)

            if match:
                value = float(match.group(1))

                if value.is_integer():
                    value = int(value)

                return {
                    "value": value,
                    "unit": unit,
                }

        return None

    @staticmethod
    def extract_availability(answer: str) -> str | None:
        """Extract availability or joining information."""
        availability_patterns = [
            r"\bimmediately\b",
            r"\bimmediate(?:ly)?\s+available\b",
            r"\bavailable\s+immediately\b",
            r"\bwithin\s+\d+\s+(?:days?|weeks?)\b",
            r"\b\d+\s+(?:days?|weeks?)\s+notice\b",
            r"\bnotice\s+period\s+of\s+\d+\s+(?:days?|weeks?)\b",
            r"\bavailable\s+(?:from|after)\s+.{1,40}",
        ]

        normalized = answer.lower()

        for pattern in availability_patterns:
            match = re.search(pattern, normalized)

            if match:
                return match.group(0).strip()

        return None

    @staticmethod
    def extract_salary(answer: str) -> dict[str, Any] | None:
        """Extract a salary expectation from the answer."""
        normalized = answer.lower()

        salary_patterns = [
            r"(?:₹|rs\.?|inr)\s*[\d,]+(?:\.\d+)?\s*(?:lpa|lakhs?|k)?",
            r"[\d,]+(?:\.\d+)?\s*(?:lpa|lakhs?|k)\b",
        ]

        for pattern in salary_patterns:
            match = re.search(pattern, normalized)

            if match:
                return {
                    "value": match.group(0).strip(),
                }

        return None