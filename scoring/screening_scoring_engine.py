"""
Screening Scoring Engine
------------------------
Scores individual candidate screening responses using:

- Clarity
- Relevance
- Completeness
- Consistency

Each parameter is scored from 0 to 100.
Each parameter contributes equally (25%) to the final score.
"""

from __future__ import annotations

import re
from typing import Any

from answer_understanding.answer_understanding_engine import (
    AnswerUnderstandingEngine,
)


class ScreeningScoringEngine:
    """Score individual candidate screening responses."""

    PARAMETER_WEIGHT = 0.25

    def __init__(self) -> None:
        self.answer_understanding = AnswerUnderstandingEngine()

    @staticmethod
    def _normalize_score(score: float) -> float:
        """Keep a score within the 0-100 range."""
        return round(max(0.0, min(100.0, score)), 2)

    def score_clarity(self, answer: str) -> float:
        """
        Score how clearly the candidate communicates the answer.
        """

        if not answer or not answer.strip():
            return 0.0

        text = answer.strip()

        if len(text) <= 3:
            return 20.0

        words = re.findall(r"\b[\w+#.-]+\b", text)
        word_count = len(words)

        if word_count <= 5:
            score = 60.0
        elif word_count <= 30:
            score = 90.0
        else:
            score = 80.0

        if text.endswith((".", "!", "?")):
            score += 5.0

        if re.search(r"\s{2,}", text):
            score -= 5.0

        return self._normalize_score(score)

    def score_relevance(
        self,
        answer: str,
        question: str,
        intent: str,
    ) -> float:
        """
        Score how directly the answer addresses the question.
        """

        if not answer or not answer.strip():
            return 0.0

        if intent == "missing":
            return 0.0

        if intent == "off_topic":
            return 20.0

        if intent == "vague":
            return 50.0

        if not question.strip():
            return 70.0

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
            return 70.0

        overlap = question_words.intersection(answer_words)

        if overlap:
            return 100.0

        return 70.0

    def score_completeness(
        self,
        answer: str,
        question: str,
        understood: dict[str, Any],
    ) -> float:
        """
        Score whether the response provides sufficient information.
        """

        if not answer or not answer.strip():
            return 0.0

        intent = understood.get("intent")

        if intent == "missing":
            return 0.0

        if intent == "vague":
            return 30.0

        word_count = len(
            re.findall(r"\b[\w+#.-]+\b", answer)
        )

        score = 50.0

        if word_count >= 10:
            score += 20.0

        if word_count >= 20:
            score += 15.0

        if understood.get("skills"):
            score += 5.0

        if understood.get("experience"):
            score += 5.0

        if understood.get("availability"):
            score += 5.0

        if understood.get("salary_expectation"):
            score += 5.0

        return self._normalize_score(score)

    def score_consistency(
        self,
        answer: str,
        understood: dict[str, Any],
    ) -> float:
        """
        Score whether the response is internally consistent.
        """

        if not answer or not answer.strip():
            return 0.0

        intent = understood.get("intent")

        if intent == "missing":
            return 0.0

        if intent == "vague":
            return 40.0

        score = 100.0

        # Detect simple contradictory experience statements.
        years = re.findall(
            r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
            answer.lower(),
        )

        if len(years) > 1:
            numeric_years = {
                float(value)
                for value in years
            }

            if len(numeric_years) > 1:
                score -= 30.0

        # Detect simple contradictory availability statements.
        normalized = answer.lower()

        immediate_available = bool(
            re.search(r"\bimmediately\b", normalized)
            or re.search(r"\bavailable\s+immediately\b", normalized)
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
            score -= 30.0

        return self._normalize_score(score)

    def score_question(
        self,
        question: str,
        answer: str,
    ) -> dict[str, Any]:
        """
        Generate the complete score breakdown for one question
        with explainable scoring reasons.
        """

        understood = self.answer_understanding.understand(
            answer=answer,
            question=question,
        )

        clarity = self.score_clarity(answer)

        relevance = self.score_relevance(
            answer=answer,
            question=question,
            intent=understood["intent"],
        )

        completeness = self.score_completeness(
            answer=answer,
            question=question,
            understood=understood,
        )

        consistency = self.score_consistency(
            answer=answer,
            understood=understood,
        )

        explanations = {
            "clarity": self._explain_clarity(
                answer,
                clarity,
            ),
            "relevance": self._explain_relevance(
                understood["intent"],
                relevance,
            ),
            "completeness": self._explain_completeness(
                understood,
                completeness,
            ),
            "consistency": self._explain_consistency(
                answer,
                consistency,
            ),
        }

        overall_score = self.calculate_overall_score(
            {
                "clarity": clarity,
                "relevance": relevance,
                "completeness": completeness,
                "consistency": consistency,
            }
        )

        return {
            "question": question,
            "answer": answer,
            "intent": understood["intent"],
            "scores": {
                "clarity": clarity,
                "relevance": relevance,
                "completeness": completeness,
                "consistency": consistency,
            },
            "weights": {
                "clarity": 25,
                "relevance": 25,
                "completeness": 25,
                "consistency": 25,
            },
            "overall_score": overall_score,
            "explanations": explanations,
        }

    @staticmethod
    def _explain_clarity(
        answer: str,
        score: float,
    ) -> str:
        """Explain the clarity score."""

        if not answer.strip():
            return "No answer was provided."

        if score >= 90:
            return "The answer is clear and sufficiently structured."

        if score >= 60:
            return "The answer is understandable but provides limited detail."

        return "The answer is very short or lacks sufficient clarity."

    @staticmethod
    def _explain_relevance(
        intent: str,
        score: float,
    ) -> str:
        """Explain the relevance score."""

        if intent == "missing":
            return "No answer was provided."

        if intent == "off_topic":
            return "The answer does not directly address the question."

        if intent == "vague":
            return "The answer is related to the question but is too vague."

        if score >= 90:
            return "The answer directly addresses the question."

        return "The answer is generally related to the question."

    @staticmethod
    def _explain_completeness(
        understood: dict[str, Any],
        score: float,
    ) -> str:
        """Explain the completeness score."""

        if understood.get("intent") == "missing":
            return "No information was provided."

        if understood.get("intent") == "vague":
            return "The response contains insufficient information."

        details = []

        if understood.get("skills"):
            details.append("skills")

        if understood.get("experience"):
            details.append("experience")

        if understood.get("availability"):
            details.append("availability")

        if understood.get("salary_expectation"):
            details.append("salary expectation")

        if details:
            return (
                "The answer provides identifiable information about "
                + ", ".join(details)
                + "."
            )

        if score >= 70:
            return "The answer provides a reasonable amount of information."

        return "The answer provides limited supporting information."

    @staticmethod
    def _explain_consistency(
        answer: str,
        score: float,
    ) -> str:
        """Explain the consistency score."""

        if not answer.strip():
            return "No answer was provided."

        if score >= 90:
            return "No obvious internal contradictions were detected."

        if score >= 60:
            return "The answer contains some potentially inconsistent information."

        return "The answer contains conflicting information."

    def calculate_overall_score(
        self,
        scores: dict[str, float],
    ) -> float:
        """
        Calculate the weighted overall screening score.

        All four screening parameters have equal weight:
        Clarity       -> 25%
        Relevance     -> 25%
        Completeness  -> 25%
        Consistency   -> 25%
        """

        clarity = self._normalize_score(
            scores.get("clarity", 0)
        )

        relevance = self._normalize_score(
            scores.get("relevance", 0)
        )

        completeness = self._normalize_score(
            scores.get("completeness", 0)
        )

        consistency = self._normalize_score(
            scores.get("consistency", 0)
        )

        overall_score = (
            clarity * self.PARAMETER_WEIGHT
            + relevance * self.PARAMETER_WEIGHT
            + completeness * self.PARAMETER_WEIGHT
            + consistency * self.PARAMETER_WEIGHT
        )

        return self._normalize_score(overall_score)

    def score_screening(
        self,
        questions_and_answers: list[dict[str, str]],
    ) -> dict[str, Any]:
        """
        Score all screening questions and generate the final
        screening score object.
        """

        question_results = []

        for item in questions_and_answers:
            question = item.get("question", "")
            answer = item.get("answer", "")

            result = self.score_question(
                question=question,
                answer=answer,
            )

            question_results.append(result)

        if not question_results:
            return {
                "total_questions": 0,
                "answered_questions": 0,
                "per_question_scores": [],
                "final_screening_score": 0.0,
            }

        total_score = sum(
            result["overall_score"]
            for result in question_results
        )

        final_screening_score = self._normalize_score(
            total_score / len(question_results)
        )

        answered_questions = sum(
            1
            for result in question_results
            if result["answer"].strip()
        )

        return {
            "total_questions": len(question_results),
            "answered_questions": answered_questions,
            "per_question_scores": question_results,
            "final_screening_score": final_screening_score,
        }