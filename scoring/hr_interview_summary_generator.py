
"""Generate structured, recruiter-ready HR interview summaries."""

from __future__ import annotations

from typing import Any

from interview_ai.hr_interview_categories import (
    HRInterviewCategory,
    HR_INTERVIEW_CATEGORY_DESCRIPTIONS,
)
from scoring.hr_interview_scoring_engine import HRInterviewScoringEngine


class HRInterviewSummaryGenerator:
    """Build HR summaries from existing interview scoring results."""

    def __init__(
        self,
        scoring_engine: HRInterviewScoringEngine | None = None,
    ) -> None:
        self.scoring_engine = (
            scoring_engine or HRInterviewScoringEngine()
        )

    def generate_summary(
        self,
        responses: list[dict[str, Any]],
        candidate_name: str = "Not provided",
        job_role: str = "Not provided",
    ) -> dict[str, Any]:
        """Generate structured insights and a natural-language report."""

        if not isinstance(responses, list):
            raise TypeError("responses must be a list.")

        for response in responses:
            if not isinstance(response, dict):
                raise TypeError("Each response must be a dictionary.")

        scores = self.scoring_engine.score_interview(responses)

        strengths = []
        weaknesses = []
        cultural_fit = []
        risk_flags = []

        for name, score in scores["dimension_scores"].items():
            if score >= 80:
                strengths.append(
                    f"{name.replace('_', ' ').title()} "
                    f"demonstrated a strong score of {score:.2f}/100."
                )
            elif score < 60:
                weaknesses.append(
                    f"{name.replace('_', ' ').title()} "
                    f"requires improvement (score: {score:.2f}/100)."
                )

        for response in responses:
            category = response.get("category")
            answer = str(response.get("response", "") or "").strip()
            question = str(response.get("question", "") or "").strip()

            if not answer:
                risk_flags.append(
                    f"Missing response for question: "
                    f"{question or response.get('question_id', 'Unknown')}"
                )

            if category == HRInterviewCategory.TEAMWORK_CULTURE_FIT.value:
                if answer:
                    cultural_fit.append(
                        {
                            "question": question,
                            "evidence": answer,
                            "status": "Evidence available; recruiter review required",
                        }
                    )
                else:
                    cultural_fit.append(
                        {
                            "question": question,
                            "evidence": None,
                            "status": "Insufficient evidence",
                        }
                    )

        consistency = scores["consistency_analysis"]

        for conflict in consistency["conflicts"]:
            risk_flags.append(conflict["description"])

        for category, result in scores["category_scores"].items():
            if result["status"] == "evaluated" and result["score"] < 60:
                risk_flags.append(
                    f"Low score in {category.replace('_', ' ')}: "
                    f"{result['score']:.2f}/100."
                )

        if not cultural_fit:
            cultural_fit.append(
                {
                    "question": None,
                    "evidence": None,
                    "status": "No teamwork or culture-fit responses available",
                }
            )

        strengths = self._unique(strengths)
        weaknesses = self._unique(weaknesses)
        risk_flags = self._unique(risk_flags)

        overall_score = scores["overall_score"]
        overall_rating = scores["overall_rating"]

        consistency_lines = [
            f"- {item['description']}"
            for item in consistency["conflicts"]
        ] or ["- No cross-response conflicts were identified."]

        strength_lines = (
            [f"- {item}" for item in strengths]
            or ["- No dimensions met the strong-score threshold."]
        )

        weakness_lines = (
            [f"- {item}" for item in weaknesses]
            or ["- No dimensions fell below the improvement threshold."]
        )

        risk_lines = (
            [f"- {item}" for item in risk_flags]
            or ["- No risk flags were identified by the configured checks."]
        )

        cultural_fit_lines = [
            (
                f"- {item['status']}: {item['evidence']}"
                if item["evidence"]
                else f"- {item['status']}"
            )
            for item in cultural_fit
        ]

        report_lines = [
            f"HR Interview Summary for {candidate_name}",
            f"Role: {job_role}",
            f"Overall HR Score: {overall_score:.2f}/100",
            f"Overall Rating: {overall_rating.replace('_', ' ').title()}",
            "",
            "Strengths:",
            *strength_lines,
            "",
            "Areas for Improvement:",
            *weakness_lines,
            "",
            "Consistency Findings:",
            *consistency_lines,
            "",
            "Risk Flags:",
            *risk_lines,
            "",
            "Cultural Fit:",
            *cultural_fit_lines,
            "",
            (
                "Recruiter Note: Review the original responses and "
                "available evidence before making a hiring decision."
            ),
        ]

        category_summaries = {
            category: {
                "description": HR_INTERVIEW_CATEGORY_DESCRIPTIONS[
                    HRInterviewCategory(category)
                ],
                "score": result["score"],
                "status": result["status"],
            }
            for category, result in scores["category_scores"].items()
        }

        return {
            "report_title": "HR Interview Summary",
            "candidate_information": {
                "candidate_name": candidate_name,
                "job_role": job_role,
            },
            "overall_performance": {
                "score": overall_score,
                "rating": overall_rating,
                "dimension_scores": scores["dimension_scores"],
            },
            "category_summaries": category_summaries,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "cultural_fit_indicators": cultural_fit,
            "consistency_analysis": consistency,
            "risk_flags": risk_flags,
            "natural_language_report": "\n".join(report_lines),
            "scoring_details": scores,
        }

    @staticmethod
    def _unique(items: list[str]) -> list[str]:
        """Remove duplicate non-empty strings while preserving order."""
        return list(dict.fromkeys(item for item in items if item))
