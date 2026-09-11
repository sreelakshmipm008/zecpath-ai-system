"""
AI Screening Report Builder
----------------------------
Transforms raw AI screening evaluations into
structured, recruiter-friendly screening reports.
"""

from __future__ import annotations

from typing import Any

from answer_understanding.answer_understanding_engine import (
    AnswerUnderstandingEngine,
)
from scoring.screening_scoring_engine import ScreeningScoringEngine


class AIScreeningReportBuilder:
    """Build recruiter-ready reports from AI screening responses."""

    def __init__(self) -> None:
        self.scoring_engine = ScreeningScoringEngine()
        self.answer_understanding = AnswerUnderstandingEngine()

    def build_report(
        self,
        candidate_name: str,
        job_role: str,
        questions_and_answers: list[dict[str, str]],
    ) -> dict[str, Any]:
        """
        Build a structured AI screening report.
        """

        screening_result = self.scoring_engine.score_screening(
            questions_and_answers
        )

        understood_answers = []

        for item in questions_and_answers:
            question = item.get("question", "")
            answer = item.get("answer", "")

            understood = self.answer_understanding.understand(
                answer=answer,
                question=question,
            )

            understood_answers.append(
                {
                    "question": question,
                    "answer": answer,
                    "understood": understood,
                }
            )

        return {
            "report_title": "AI Screening Report",
            "candidate_information": {
                "candidate_name": candidate_name,
                "job_role": job_role,
            },
            "screening_summary": {
                "key_answers": self._build_key_answers(
                    understood_answers
                ),
                "strengths": self._build_strengths(
                    screening_result
                ),
                "risks": self._build_risks(
                    screening_result
                ),
                "missing_data": self._build_missing_data(
                    understood_answers
                ),
            },
            "screening_highlights": {
                "salary_expectation": self._extract_salary(
                    understood_answers
                ),
                "availability": self._extract_availability(
                    understood_answers
                ),
                "skill_confirmations": self._extract_skills(
                    understood_answers
                ),
            },
            "screening_evaluation": {
                "total_questions": screening_result[
                    "total_questions"
                ],
                "answered_questions": screening_result[
                    "answered_questions"
                ],
                "final_screening_score": screening_result[
                    "final_screening_score"
                ],
            },
        }

    @staticmethod
    def _build_key_answers(
        understood_answers: list[dict[str, Any]],
    ) -> list[dict[str, str]]:
        """Collect non-empty candidate answers."""

        key_answers = []

        for item in understood_answers:
            answer = item["answer"].strip()

            if answer:
                key_answers.append(
                    {
                        "question": item["question"],
                        "answer": answer,
                    }
                )

        return key_answers

    @staticmethod
    def _build_strengths(
        screening_result: dict[str, Any],
    ) -> list[str]:
        """Identify strengths from strong screening responses."""

        strengths = []

        for result in screening_result["per_question_scores"]:
            scores = result["scores"]

            if result["intent"] == "missing":
                continue

            if result["overall_score"] >= 80:
                strengths.append(
                    result["explanations"]["clarity"]
                )

                if scores["relevance"] >= 90:
                    strengths.append(
                        result["explanations"]["relevance"]
                    )

                if scores["consistency"] >= 90:
                    strengths.append(
                        result["explanations"]["consistency"]
                    )

        return AIScreeningReportBuilder._unique_items(
            strengths
        )

    @staticmethod
    def _build_risks(
        screening_result: dict[str, Any],
    ) -> list[str]:
        """Identify risks from weak or problematic responses."""

        risks = []

        for result in screening_result["per_question_scores"]:
            if result["intent"] == "missing":
                continue

            if result["overall_score"] < 60:
                risks.append(
                    result["explanations"]["completeness"]
                )

            if result["intent"] == "off_topic":
                risks.append(
                    result["explanations"]["relevance"]
                )

            if result["intent"] == "vague":
                risks.append(
                    result["explanations"]["completeness"]
                )

            if result["scores"]["consistency"] < 90:
                risks.append(
                    result["explanations"]["consistency"]
                )

        return AIScreeningReportBuilder._unique_items(
            risks
        )

    @staticmethod
    def _build_missing_data(
        understood_answers: list[dict[str, Any]],
    ) -> list[str]:
        """Identify questions for which required information is missing."""

        missing_data = []

        for item in understood_answers:
            answer = item["answer"].strip()

            if not answer:
                missing_data.append(item["question"])

        return missing_data

    @staticmethod
    def _extract_salary(
        understood_answers: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        """Extract the candidate's salary expectation."""

        for item in understood_answers:
            salary = item["understood"].get(
                "salary_expectation"
            )

            if salary:
                return salary

        return None

    @staticmethod
    def _extract_availability(
        understood_answers: list[dict[str, Any]],
    ) -> str | None:
        """Extract the candidate's availability."""

        for item in understood_answers:
            availability = item["understood"].get(
                "availability"
            )

            if availability:
                return availability

        return None

    @staticmethod
    def _extract_skills(
        understood_answers: list[dict[str, Any]],
    ) -> list[str]:
        """Collect confirmed skills mentioned in answers."""

        skills = []

        for item in understood_answers:
            extracted_skills = item["understood"].get(
                "skills",
                [],
            )

            skills.extend(extracted_skills)

        return AIScreeningReportBuilder._unique_items(
            skills
        )

    @staticmethod
    def _unique_items(items: list[str]) -> list[str]:
        """Return unique non-empty items while preserving order."""

        unique = []

        for item in items:
            if item and item not in unique:
                unique.append(item)

        return unique