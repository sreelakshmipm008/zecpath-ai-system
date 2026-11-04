"""Explainable, human-reviewed candidate recommendation engine."""

from __future__ import annotations

from typing import Any


class FinalRecommendationEngine:
    """Generate evidence-based hiring recommendations for human review."""

    VALID_ELIGIBILITY_STATUSES = {
        "eligible",
        "review",
        "rejected",
    }

    def __init__(
        self,
        selected_threshold: float = 80.0,
        rejected_threshold: float = 60.0,
    ) -> None:
        self._validate_thresholds(
            selected_threshold,
            rejected_threshold,
        )
        self.selected_threshold = float(selected_threshold)
        self.rejected_threshold = float(rejected_threshold)

    @staticmethod
    def _validate_thresholds(
        selected_threshold: float,
        rejected_threshold: float,
    ) -> None:
        for name, value in (
            ("selected_threshold", selected_threshold),
            ("rejected_threshold", rejected_threshold),
        ):
            if isinstance(value, bool) or not isinstance(
                value, (int, float)
            ):
                raise TypeError(f"{name} must be a number.")
            if not 0 <= value <= 100:
                raise ValueError(f"{name} must be between 0 and 100.")

        if rejected_threshold >= selected_threshold:
            raise ValueError(
                "rejected_threshold must be lower than selected_threshold."
            )

    @staticmethod
    def _validate_dict(value: Any, name: str) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a dictionary.")
        return value

    @staticmethod
    def _validate_score(value: Any) -> float | None:
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Candidate score must be a number.")
        if not 0 <= value <= 100:
            raise ValueError("Candidate score must be between 0 and 100.")
        return float(value)

    @staticmethod
    def _validate_string_list(value: Any, name: str) -> list[str]:
        if value is None:
            return []
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a list.")
        return [str(item) for item in value if item is not None]

    def calculate_evidence_confidence(
        self,
        candidate_score: dict[str, Any],
        eligibility_result: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Calculate evidence coverage, not probability of correctness."""

        round_scores = candidate_score.get("round_scores", {})
        if not isinstance(round_scores, dict):
            raise TypeError("round_scores must be a dictionary.")

        stage_names = (
            "ats",
            "screening",
            "hr_interview",
            "technical_interview",
            "machine_test",
        )

        available_stages = [
            stage for stage in stage_names
            if round_scores.get(stage) is not None
        ]

        stage_coverage = len(available_stages) / len(stage_names) * 80
        eligibility_coverage = 20 if eligibility_result is not None else 0
        confidence = round(stage_coverage + eligibility_coverage, 2)

        return {
            "score": confidence,
            "level": (
                "complete" if confidence == 100
                else "partial" if confidence > 0
                else "insufficient"
            ),
            "available_stages": available_stages,
            "missing_stages": [
                stage for stage in stage_names
                if stage not in available_stages
            ],
            "eligibility_evaluated": eligibility_result is not None,
            "meaning": (
                "Evidence completeness indicator only; "
                "not a probability of recommendation correctness."
            ),
        }

    def generate_recommendation(
        self,
        candidate_score: dict[str, Any],
        eligibility_result: dict[str, Any] | None,
        hr_summary: dict[str, Any] | None = None,
        behavioral_report: dict[str, Any] | None = None,
        integrity_alerts: list[Any] | None = None,
    ) -> dict[str, Any]:
        """Generate a transparent recommendation for human review."""

        candidate_score = self._validate_dict(
            candidate_score, "candidate_score"
        )

        if eligibility_result is not None:
            eligibility_result = self._validate_dict(
                eligibility_result, "eligibility_result"
            )

        if hr_summary is not None:
            hr_summary = self._validate_dict(hr_summary, "hr_summary")

        if behavioral_report is not None:
            behavioral_report = self._validate_dict(
                behavioral_report, "behavioral_report"
            )

        if integrity_alerts is not None and not isinstance(
            integrity_alerts, list
        ):
            raise TypeError("integrity_alerts must be a list.")

        score_value = self._validate_score(
            candidate_score.get(
                "hiring_fit_percentage",
                candidate_score.get("unified_score"),
            )
        )

        eligibility_status = None
        eligibility_reasons: list[str] = []

        if eligibility_result is not None:
            raw_status = eligibility_result.get("eligibility_status")
            if not isinstance(raw_status, str):
                raise ValueError(
                    "eligibility_result must contain eligibility_status."
                )

            eligibility_status = raw_status.strip().lower()
            if eligibility_status not in self.VALID_ELIGIBILITY_STATUSES:
                raise ValueError("Unknown eligibility status.")

            eligibility_reasons = self._validate_string_list(
                eligibility_result.get("eligibility_reasons", []),
                "eligibility_reasons",
            )

        hr_risk_flags = self._validate_string_list(
            (hr_summary or {}).get("risk_flags", []),
            "hr risk_flags",
        )

        unresolved_integrity_alerts = list(integrity_alerts or [])

        evidence_confidence = self.calculate_evidence_confidence(
            candidate_score,
            eligibility_result,
        )

        evidence_complete = (
            candidate_score.get("evidence_complete") is True
            and len(evidence_confidence["available_stages"]) == 5
        )

        reasons: list[str] = []
        review_items: list[str] = []

        if score_value is None:
            reasons.append("Unified candidate score is unavailable.")
            review_items.append("Obtain a valid candidate score.")

        if eligibility_status is None:
            reasons.append("Eligibility evaluation is unavailable.")
            review_items.append("Complete eligibility evaluation.")
        elif eligibility_status == "review":
            reasons.append("Eligibility evaluation requires review.")
            review_items.extend(eligibility_reasons or [
                "Review unresolved eligibility requirements."
            ])
        elif eligibility_status == "rejected":
            reasons.append("Eligibility evaluation returned Rejected.")
            review_items.extend(eligibility_reasons or [
                "Verify the eligibility findings before a final decision."
            ])

        if not evidence_complete:
            reasons.append("One or more evaluation stages are incomplete.")
            review_items.append("Review missing evaluation evidence.")

        if hr_risk_flags:
            reasons.append("HR interview findings require recruiter review.")
            review_items.extend(hr_risk_flags)

        if unresolved_integrity_alerts:
            reasons.append(
                "Integrity alerts require separate human investigation."
            )
            review_items.append(
                "Review integrity evidence, consent and candidate explanation."
            )

        if score_value is not None:
            if score_value >= self.selected_threshold:
                reasons.append(
                    "Unified score meets the configured selected threshold."
                )
            elif score_value < self.rejected_threshold:
                reasons.append(
                    "Unified score is below the configured rejection threshold."
                )
            else:
                reasons.append(
                    "Unified score falls within the intermediate review range."
                )

        # Recommendation rules: unresolved evidence and risks take priority.
        if hr_risk_flags or unresolved_integrity_alerts:
            category = "Hold / Review"
        elif eligibility_status == "rejected":
            category = "Rejected"
        elif (
            score_value is not None
            and score_value < self.rejected_threshold
            and evidence_complete
            and eligibility_status == "eligible"
            and not hr_risk_flags
            and not unresolved_integrity_alerts
        ):
            category = "Rejected"
        elif (
            score_value is not None
            and score_value >= self.selected_threshold
            and evidence_complete
            and eligibility_status == "eligible"
            and not hr_risk_flags
            and not unresolved_integrity_alerts
        ):
            category = "Selected"
        else:
            category = "Hold / Review"

        if not reasons:
            reasons.append(
                "Evaluation evidence meets the configured recommendation rules."
            )

        return {
            "candidate_id": candidate_score.get("candidate_id"),
            "candidate_name": candidate_score.get("candidate_name"),
            "job_role": candidate_score.get("job_role"),
            "decision_category": category,
            "unified_score": score_value,
            "eligibility_status": eligibility_status,
            "recommendation_confidence": evidence_confidence,
            "reasons": reasons,
            "eligibility_findings": eligibility_reasons,
            "hr_risk_findings": hr_risk_flags,
            "integrity_review_items": unresolved_integrity_alerts,
            "behavioral_observations": behavioral_report or {},
            "review_required": True,
            "review_items": list(dict.fromkeys(review_items)),
            "final_decision_authority": "Human recruiter",
            "decision_note": (
                "This is an explainable decision-support recommendation, "
                "not an automated final employment decision. "
                "Behavioral observations are informational and do not "
                "independently determine candidate suitability."
            ),
        }
