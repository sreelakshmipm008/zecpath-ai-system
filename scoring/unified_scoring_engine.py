"""
Unified Candidate Scoring Engine

Maintains the original three-stage scoring API and adds a configurable
five-stage cross-round hiring-fit calculation.

Five-stage default weights are provisional implementation defaults,
not company-prescribed or empirically validated hiring criteria.
"""


class UnifiedScoringEngine:
    """Calculate transparent candidate scores across evaluation stages."""

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

    FIVE_STAGE_SCORE_KEYS = (
        "ats",
        "screening",
        "hr_interview",
        "technical_interview",
        "machine_test",
    )

    FIVE_STAGE_DEFAULT_WEIGHTS = {
        "ats": 0.20,
        "screening": 0.20,
        "hr_interview": 0.20,
        "technical_interview": 0.20,
        "machine_test": 0.20,
    }

    def __init__(self, role_weights=None, five_stage_role_weights=None):
        self.role_weights = {
            role: weights.copy()
            for role, weights in self.ROLE_WEIGHTS.items()
        }

        if role_weights:
            for role, weights in role_weights.items():
                self.role_weights[role] = weights.copy()

        self.five_stage_role_weights = {}

        if five_stage_role_weights:
            for role, weights in five_stage_role_weights.items():
                self.five_stage_role_weights[role] = weights.copy()

        self._validate_weights(self.DEFAULT_WEIGHTS)

        for weights in self.role_weights.values():
            self._validate_weights(weights)

        self._validate_five_stage_weights(
            self.FIVE_STAGE_DEFAULT_WEIGHTS
        )

        for weights in self.five_stage_role_weights.values():
            self._validate_five_stage_weights(weights)

    @classmethod
    def _validate_weights(cls, weights):
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

    @classmethod
    def _validate_five_stage_weights(cls, weights):
        if not isinstance(weights, dict):
            raise ValueError("Five-stage weights must be a dictionary.")

        if set(weights) != set(cls.FIVE_STAGE_SCORE_KEYS):
            raise ValueError(
                "Five-stage weights must contain exactly: "
                f"{cls.FIVE_STAGE_SCORE_KEYS}"
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
            raise ValueError("Five-stage weights must sum to 1.0.")

    @staticmethod
    def _validate_score(name, score):
        if (
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not 0 <= score <= 100
        ):
            raise ValueError(
                f"'{name}' score must be a number between 0 and 100."
            )

    def get_weights(self, role=None):
        weights = self.role_weights.get(role, self.DEFAULT_WEIGHTS)
        self._validate_weights(weights)
        return weights.copy()

    def get_five_stage_weights(self, role=None):
        weights = self.five_stage_role_weights.get(
            role, self.FIVE_STAGE_DEFAULT_WEIGHTS
        )
        self._validate_five_stage_weights(weights)
        return weights.copy()

    def calculate_hiring_fit(
        self,
        ats_score,
        screening_score,
        hr_interview_score,
        role=None,
    ):
        """Preserve the original three-stage scoring API."""
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
        """Preserve the original three-stage candidate object."""
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

    def calculate_five_stage_hiring_fit(
        self,
        ats_score=None,
        screening_score=None,
        hr_interview_score=None,
        technical_interview_score=None,
        machine_test_score=None,
        role=None,
    ):
        """Calculate a five-stage score with explicit missing-score handling."""
        scores = {
            "ats": ats_score,
            "screening": screening_score,
            "hr_interview": hr_interview_score,
            "technical_interview": technical_interview_score,
            "machine_test": machine_test_score,
        }

        available_scores = {}
        missing_stages = []

        for name, score in scores.items():
            if score is None:
                missing_stages.append(name)
                continue

            self._validate_score(name, score)
            available_scores[name] = score

        if not available_scores:
            raise ValueError(
                "At least one valid evaluation-stage score is required."
            )

        configured_weights = self.get_five_stage_weights(role)

        available_weight_total = sum(
            configured_weights[name] for name in available_scores
        )

        if available_weight_total <= 0:
            raise ValueError(
                "Available evaluation stages must have a combined "
                "configured weight greater than zero."
            )

        applied_weights = {
            name: round(
                configured_weights[name] / available_weight_total, 10
            )
            for name in available_scores
        }

        contributions = {
            name: round(
                available_scores[name] * applied_weights[name], 2
            )
            for name in available_scores
        }

        hiring_fit = round(sum(contributions.values()), 2)
        evidence_complete = not missing_stages

        return {
            "job_role": role,
            "round_scores": scores,
            "configured_weights": configured_weights,
            "weights": applied_weights,
            "weighted_contributions": contributions,
            "available_stages": list(available_scores),
            "missing_stages": missing_stages,
            "evidence_complete": evidence_complete,
            "human_review_required": not evidence_complete,
            "hiring_fit_percentage": hiring_fit,
            "unified_score": hiring_fit,
            "scoring_note": (
                "Provisional five-stage weights were normalized across "
                "available stages. This score is decision support, not "
                "an automatic hiring decision."
            ),
        }

    def build_full_candidate_score(
        self,
        candidate_id,
        candidate_name,
        role,
        ats_score=None,
        screening_score=None,
        hr_interview_score=None,
        technical_interview_score=None,
        machine_test_score=None,
    ):
        """Build a transparent five-stage candidate score object."""
        result = self.calculate_five_stage_hiring_fit(
            ats_score=ats_score,
            screening_score=screening_score,
            hr_interview_score=hr_interview_score,
            technical_interview_score=technical_interview_score,
            machine_test_score=machine_test_score,
            role=role,
        )

        return {
            "candidate_id": candidate_id,
            "candidate_name": candidate_name,
            **result,
        }
