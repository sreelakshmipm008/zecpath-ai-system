
"""
Unified Candidate Scoring Engine

Combines ATS, Screening, and HR Interview scores into a
single hiring-fit percentage with configurable role-based weights.

Default weights are implementation defaults, not company-prescribed
values from the Day 41 task sheet.
"""


class UnifiedScoringEngine:
    """Calculate a unified hiring-fit score for a candidate."""

    DEFAULT_WEIGHTS = {
        "ats": 0.40,
        "screening": 0.25,
        "hr_interview": 0.35,
    }

    ROLE_WEIGHTS = {
        "Data Analyst": {
            "ats": 0.45,
            "screening": 0.25,
            "hr_interview": 0.30,
        },
        "Data Scientist": {
            "ats": 0.45,
            "screening": 0.20,
            "hr_interview": 0.35,
        },
        "Software Engineer": {
            "ats": 0.45,
            "screening": 0.20,
            "hr_interview": 0.35,
        },
        "UI/UX Designer": {
            "ats": 0.35,
            "screening": 0.25,
            "hr_interview": 0.40,
        },
    }

    SCORE_KEYS = ("ats", "screening", "hr_interview")

    def __init__(self, role_weights=None):
        """Initialize default weights and optional role overrides."""
        self.role_weights = {
            role: weights.copy()
            for role, weights in self.ROLE_WEIGHTS.items()
        }

        if role_weights:
            for role, weights in role_weights.items():
                self.role_weights[role] = weights.copy()

        self._validate_weights(self.DEFAULT_WEIGHTS)

        for weights in self.role_weights.values():
            self._validate_weights(weights)

    @classmethod
    def _validate_weights(cls, weights):
        """Validate weight keys, ranges, and total."""
        if set(weights) != set(cls.SCORE_KEYS):
            raise ValueError(
                f"Weights must contain exactly: {cls.SCORE_KEYS}"
            )

        for key, weight in weights.items():
            if (
                isinstance(weight, bool)
                or not isinstance(weight, (int, float))
                or not 0 <= weight <= 1
            ):
                raise ValueError(
                    f"Weight for '{key}' must be between 0 and 1."
                )

        if not abs(sum(weights.values()) - 1.0) <= 1e-9:
            raise ValueError("Cross-round weights must sum to 1.0.")

    @staticmethod
    def _validate_score(name, score):
        """Ensure every round score is numeric and within 0–100."""
        if (
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not 0 <= score <= 100
        ):
            raise ValueError(
                f"'{name}' score must be a number between 0 and 100."
            )

    def get_weights(self, role=None):
        """Return role-specific weights or the default configuration."""
        weights = self.role_weights.get(
            role, self.DEFAULT_WEIGHTS
        )
        self._validate_weights(weights)
        return weights.copy()

    def calculate_hiring_fit(
        self,
        ats_score,
        screening_score,
        hr_interview_score,
        role=None,
    ):
        """Calculate the weighted hiring-fit percentage."""
        scores = {
            "ats": ats_score,
            "screening": screening_score,
            "hr_interview": hr_interview_score,
        }

        for name, score in scores.items():
            self._validate_score(name, score)

        weights = self.get_weights(role)

        contributions = {
            name: round(scores[name] * weights[name], 2)
            for name in self.SCORE_KEYS
        }

        hiring_fit = round(sum(contributions.values()), 2)

        return {
            "job_role": role,
            "round_scores": scores,
            "weights": weights,
            "weighted_contributions": contributions,
            "hiring_fit_percentage": hiring_fit,
            "unified_score": hiring_fit,
        }

    def build_candidate_score(
        self,
        candidate_id,
        candidate_name,
        role,
        ats_score,
        screening_score,
        hr_interview_score,
    ):
        """Build a unified candidate score object."""
        result = self.calculate_hiring_fit(
            ats_score=ats_score,
            screening_score=screening_score,
            hr_interview_score=hr_interview_score,
            role=role,
        )

        return {
            "candidate_id": candidate_id,
            "candidate_name": candidate_name,
            **result,
        }
