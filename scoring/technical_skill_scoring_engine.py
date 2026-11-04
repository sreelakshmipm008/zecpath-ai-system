"""Explainable scoring engine for technical interview answers."""

from config import TECHNICAL_SCORING_WEIGHTS
from scoring.technical_rubrics import get_rubric_guidance


class TechnicalSkillScoringEngine:
    """Calculate technical answer scores from rubric-based assessments."""

    REQUIRED_DIMENSIONS = {
        "accuracy",
        "explanation_depth",
        "logical_reasoning",
        "real_world_application",
    }

    def __init__(self, weights=None):
        self.weights = dict(
            weights if weights is not None else TECHNICAL_SCORING_WEIGHTS
        )

        if set(self.weights) != self.REQUIRED_DIMENSIONS:
            raise ValueError("All technical scoring dimensions are required")

        for dimension, weight in self.weights.items():
            if (
                isinstance(weight, bool)
                or not isinstance(weight, (int, float))
                or weight < 0
            ):
                raise ValueError(f"Invalid weight for {dimension}")

        if abs(sum(self.weights.values()) - 1.0) > 1e-9:
            raise ValueError("Technical scoring weights must sum to 1.0")

    @staticmethod
    def _validate_score(value, dimension):
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not 0 <= value <= 100
        ):
            raise ValueError(
                f"{dimension} score must be a number between 0 and 100"
            )

        return float(value)

    @staticmethod
    def _classify_score(score):
        if score < 40:
            return "Needs Improvement"
        if score < 70:
            return "Developing"
        if score < 85:
            return "Proficient"
        return "Strong"

    def score_answer(
        self,
        question,
        answer,
        dimension_scores,
        assessor_notes=None,
    ):
        """Score one answer using assessor-provided rubric ratings."""

        if not isinstance(question, dict):
            raise ValueError("question must be a dictionary")

        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("answer must be a non-empty string")

        if not isinstance(question.get("expected_points"), list):
            raise ValueError("question must contain expected_points")

        if not question["expected_points"]:
            raise ValueError("expected_points cannot be empty")

        rubric_guidance = get_rubric_guidance(
            question.get("type"), question.get("difficulty")
        )

        if not isinstance(dimension_scores, dict):
            raise ValueError("dimension_scores must be a dictionary")

        if set(dimension_scores) != self.REQUIRED_DIMENSIONS:
            raise ValueError("Provide scores for all four dimensions")

        scores = {
            dimension: self._validate_score(
                dimension_scores[dimension], dimension
            )
            for dimension in self.REQUIRED_DIMENSIONS
        }

        contributions = {
            dimension: round(
                scores[dimension] * self.weights[dimension], 2
            )
            for dimension in self.REQUIRED_DIMENSIONS
        }

        final_score = round(sum(contributions.values()), 2)

        return {
            "question_id": question.get("id"),
            "question_type": question.get("type"),
            "difficulty": question.get("difficulty"),
            "skill_domain": question.get("domain"),
            "answer": answer.strip(),
            "expected_points": question["expected_points"],
            "rubric_guidance": rubric_guidance,
            "dimension_scores": scores,
            "weights": self.weights.copy(),
            "weighted_contributions": contributions,
            "technical_score": final_score,
            "performance_level": self._classify_score(final_score),
            "assessor_notes": assessor_notes or "",
            "assessment_method": "assessor_rubric",
        }

    def build_skill_breakdown(self, answer_results):
        """Aggregate assessed answers by technical skill domain."""

        if not isinstance(answer_results, list) or not answer_results:
            raise ValueError("answer_results must be a non-empty list")

        grouped = {}

        for result in answer_results:
            if not isinstance(result, dict):
                raise ValueError("Each answer result must be a dictionary")

            domain = result.get("skill_domain")
            score = result.get("technical_score")

            if not isinstance(domain, str) or not domain.strip():
                raise ValueError("Each result must have a skill_domain")

            self._validate_score(score, "technical_score")
            grouped.setdefault(domain, []).append(float(score))

        breakdown = {}

        for domain, scores in grouped.items():
            average = round(sum(scores) / len(scores), 2)
            breakdown[domain] = {
                "average_score": average,
                "question_count": len(scores),
                "performance_level": self._classify_score(average),
            }

        overall = round(
            sum(item["technical_score"] for item in answer_results)
            / len(answer_results),
            2,
        )

        return {
            "overall_technical_score": overall,
            "performance_level": self._classify_score(overall),
            "total_questions": len(answer_results),
            "skill_breakdown": breakdown,
        }

