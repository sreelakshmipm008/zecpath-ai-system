"""
HR Interview Scoring Engine.

Provides:
- response-level quality and HR dimensions
- answer relevance
- communication score
- observable confidence score
- cross-response consistency
- 25/25/25/25 explainable weighting
- category and interview-level normalization
- structured interview summary
"""

from __future__ import annotations

from typing import Any, Dict, List

from answer_understanding.answer_understanding_engine import (
    AnswerUnderstandingEngine,
)
from config import HR_SCORING_WEIGHTS
from interview_ai.hr_interview_categories import (
    HRInterviewCategory,
    HR_INTERVIEW_CATEGORY_ORDER,
)
from scoring.communication_confidence_analyzer import (
    CommunicationConfidenceAnalyzer,
)
from scoring.communication_scorer import CommunicationScorer
from scoring.sentiment_scorer import SentimentScorer


class HRInterviewScoringEngine:
    """Score and summarize an HR interview session."""

    DEFAULT_CATEGORY_WEIGHTS = {
        HRInterviewCategory.SELF_INTRODUCTION.value: 1.0,
        HRInterviewCategory.CAREER_JOURNEY.value: 1.0,
        HRInterviewCategory.STRENGTHS_WEAKNESSES.value: 1.0,
        HRInterviewCategory.TEAMWORK_CULTURE_FIT.value: 1.0,
        HRInterviewCategory.CAREER_GOALS.value: 1.0,
        HRInterviewCategory.AVAILABILITY_COMMITMENT.value: 1.0,
    }

    RELEVANCE_SCORES = {
        "on_topic": 100.0,
        "vague": 50.0,
        "off_topic": 20.0,
        "missing": 0.0,
    }

    def __init__(
        self,
        category_weights: Dict[str, float] | None = None,
    ) -> None:
        self.category_weights = (
            category_weights.copy()
            if category_weights is not None
            else self.DEFAULT_CATEGORY_WEIGHTS.copy()
        )

        self.hr_scoring_weights = HR_SCORING_WEIGHTS.copy()

        self._validate_category_weights()
        self._validate_hr_scoring_weights()

        self.communication_scorer = CommunicationScorer()
        self.confidence_analyzer = CommunicationConfidenceAnalyzer()
        self.sentiment_scorer = SentimentScorer()
        self.answer_understanding_engine = AnswerUnderstandingEngine()

    def _validate_category_weights(self) -> None:
        valid_categories = {
            category.value for category in HR_INTERVIEW_CATEGORY_ORDER
        }

        for category, weight in self.category_weights.items():
            if category not in valid_categories:
                raise ValueError(
                    f"Unknown HR interview category: {category}"
                )

            if not isinstance(weight, (int, float)):
                raise TypeError(
                    f"Weight for {category} must be numeric."
                )

            if weight < 0:
                raise ValueError(
                    f"Weight for {category} cannot be negative."
                )

    def _validate_hr_scoring_weights(self) -> None:
        required = {
            "answer_relevance",
            "communication_score",
            "confidence_score",
            "consistency",
        }

        if set(self.hr_scoring_weights) != required:
            raise ValueError(
                "HR scoring weights must contain exactly the four "
                "required parameters."
            )

        if any(
            not isinstance(weight, (int, float)) or weight < 0
            for weight in self.hr_scoring_weights.values()
        ):
            raise ValueError(
                "HR scoring weights must be non-negative numbers."
            )

        if abs(sum(self.hr_scoring_weights.values()) - 1.0) > 1e-9:
            raise ValueError(
                "HR scoring weights must sum to 1.0."
            )

    @staticmethod
    def _normalize_score(score: float) -> float:
        """Keep scores within the 0-100 range."""
        return round(
            max(0.0, min(100.0, float(score))),
            2,
        )

    def _score_relevance(
        self,
        response: str,
        question: str,
    ) -> Dict[str, Any]:
        understanding = self.answer_understanding_engine.understand(
            answer=response,
            question=question,
        )

        intent = understanding.get("intent", "on_topic")
        score = self.RELEVANCE_SCORES.get(intent, 0.0)

        return {
            "score": self._normalize_score(score),
            "intent": intent,
            "question_available": bool(question.strip()),
            "analysis": understanding,
        }

    def _build_score_breakdown(
        self,
        answer_relevance: float,
        communication_score: float,
        confidence_score: float,
        consistency_score: float,
    ) -> Dict[str, Any]:
        """Build the transparent 25/25/25/25 score breakdown."""

        dimensions = {
            "answer_relevance": self._normalize_score(
                answer_relevance
            ),
            "communication_score": self._normalize_score(
                communication_score
            ),
            "confidence_score": self._normalize_score(
                confidence_score
            ),
            "consistency": self._normalize_score(
                consistency_score
            ),
        }

        contributions = {
            name: round(
                dimensions[name] * self.hr_scoring_weights[name],
                2,
            )
            for name in dimensions
        }

        combined_score = self._normalize_score(
            sum(contributions.values())
        )

        return {
            "dimensions": dimensions,
            "weights": self.hr_scoring_weights.copy(),
            "contributions": contributions,
            "combined_score": combined_score,
        }

    def score_response(
        self,
        response: str,
        category: str | HRInterviewCategory,
        duration_seconds: float | None = None,
        question: str = "",
    ) -> Dict[str, Any]:
        """
        Score one response.

        ``score`` remains the original response-quality score for
        backward compatibility. ``combined_score`` is the new
        four-dimensional HR score.
        """

        if not isinstance(response, str):
            raise TypeError("response must be a string.")

        if not isinstance(question, str):
            raise TypeError("question must be a string.")

        if isinstance(category, HRInterviewCategory):
            category_value = category.value
        else:
            category_value = category

        valid_categories = {
            item.value for item in HR_INTERVIEW_CATEGORY_ORDER
        }

        if category_value not in valid_categories:
            raise ValueError(
                f"Unknown HR interview category: {category_value}"
            )

        cleaned_response = response.strip()
        word_count = len(cleaned_response.split())

        if word_count == 0:
            response_quality_score = 0.0
            quality = "insufficient"
        elif word_count < 10:
            response_quality_score = 50.0
            quality = "brief"
        elif word_count <= 100:
            response_quality_score = 100.0
            quality = "adequate"
        elif word_count <= 150:
            response_quality_score = 85.0
            quality = "detailed"
        else:
            response_quality_score = 70.0
            quality = "very_detailed"

        communication_result = self.communication_scorer.evaluate(
            cleaned_response
        )
        communication_score = float(
            communication_result["communication_score"]
        )

        confidence_result = self.confidence_analyzer.analyze(
            cleaned_response,
            duration_seconds=duration_seconds,
        )

        sentiment_result = self.sentiment_scorer.analyze(
            cleaned_response
        )

        if not cleaned_response:
            stress_result = {
                "stress_score": 0.0,
                "stress_level": "none",
            }

            behavioral_confidence_result = {
                "score": 0.0,
            }

            relevance_result = {
                "score": 0.0,
                "intent": "missing",
                "question_available": bool(question.strip()),
                "analysis": {
                    "answer": "",
                    "intent": "missing",
                },
            }

            behavioral_confidence_score = 0.0
            relevance_score = 0.0
            consistency_score = 0.0
            sentiment_quality_score = 0.0

        else:
            hesitation_score = confidence_result["hesitation"]["score"]
            uncertainty_score = confidence_result["uncertainty"]["score"]
            contradiction_score = confidence_result["contradictions"]["score"]

            negative_sentiment_score = max(
                0.0,
                -float(sentiment_result["score"]),
            )

            stress_result = (
                self.confidence_analyzer.measure_stress_indicators(
                    hesitation_count=confidence_result["hesitation"][
                        "count"
                    ],
                    uncertainty_count=confidence_result["uncertainty"][
                        "count"
                    ],
                    contradiction_count=confidence_result[
                        "contradictions"
                    ]["count"],
                    negative_sentiment_score=negative_sentiment_score,
                )
            )

            behavioral_confidence_result = (
                self.confidence_analyzer.generate_behavioral_confidence_score(
                    hesitation_score=hesitation_score,
                    uncertainty_score=uncertainty_score,
                    contradiction_score=contradiction_score,
                    stress_score=stress_result["stress_score"],
                    sentiment_score=float(
                        sentiment_result["score"]
                    ),
                )
            )

            behavioral_confidence_score = float(
                behavioral_confidence_result["score"]
            )

            relevance_result = self._score_relevance(
                cleaned_response,
                question,
            )
            relevance_score = relevance_result["score"]

            # At response level this is the observable within-answer
            # consistency signal. Cross-response consistency is calculated
            # at interview level.
            consistency_score = float(
                confidence_result["contradictions"]["score"]
            )

            sentiment_quality_score = (
                (float(sentiment_result["score"]) + 1.0)
                / 2.0
            ) * 100.0

        breakdown = self._build_score_breakdown(
            answer_relevance=relevance_score,
            communication_score=communication_score,
            confidence_score=behavioral_confidence_score,
            consistency_score=consistency_score,
        )

        return {
            "category": category_value,
            "word_count": word_count,

            # Backward-compatible legacy score.
            "score": self._normalize_score(
                response_quality_score
            ),

            "quality": quality,

            # New four-dimensional HR score.
            "combined_score": breakdown["combined_score"],

            "response_quality_score": self._normalize_score(
                response_quality_score
            ),
            "answer_relevance_score": self._normalize_score(
                relevance_score
            ),
            "communication_score": self._normalize_score(
                communication_score
            ),
            "behavioral_confidence_score": self._normalize_score(
                behavioral_confidence_score
            ),
            "consistency_score": self._normalize_score(
                consistency_score
            ),
            "sentiment_score": round(
                float(sentiment_result["score"]),
                2,
            ),
            "sentiment_quality_score": self._normalize_score(
                sentiment_quality_score
            ),

            "score_breakdown": breakdown,
            "communication_analysis": communication_result,
            "behavioral_analysis": confidence_result,
            "stress_analysis": stress_result,
            "sentiment_analysis": sentiment_result,
            "relevance_analysis": relevance_result,
        }

    def _extract_claims(
        self,
        response: Dict[str, Any],
    ) -> Dict[str, Any]:
        text = str(response.get("response", "") or "").strip()

        understood = self.answer_understanding_engine.understand(
            answer=text,
            question=str(response.get("question", "") or ""),
        )

        return {
            "question_id": response.get("question_id"),
            "experience": understood.get("experience"),
            "availability": understood.get("availability"),
            "salary_expectation": understood.get(
                "salary_expectation"
            ),
        }

    @staticmethod
    def _normalize_experience(
        claim: Dict[str, Any] | None,
    ) -> float | None:
        if not claim:
            return None

        try:
            value = float(claim["value"])
        except (KeyError, TypeError, ValueError):
            return None

        if claim.get("unit") == "years":
            return value

        if claim.get("unit") == "months":
            return value / 12.0

        return None

    @staticmethod
    def _normalize_text_claim(
        claim: Any,
    ) -> str | None:
        if claim is None:
            return None

        if isinstance(claim, dict):
            value = claim.get("value")
        else:
            value = claim

        if value is None:
            return None

        return " ".join(
            str(value).lower().split()
        )

    def _score_consistency(
        self,
        responses: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Calculate interview-level consistency.

        The score combines:
        - within-answer contradiction signals
        - cross-answer claim consistency
        """

        claims = [
            self._extract_claims(response)
            for response in responses
        ]

        conflicts = []

        experience_values = [
            value
            for value in (
                self._normalize_experience(
                    item["experience"]
                )
                for item in claims
            )
            if value is not None
        ]

        if len(experience_values) >= 2:
            baseline = experience_values[0]

            if any(
                abs(value - baseline) > 0.01
                for value in experience_values[1:]
            ):
                conflicts.append(
                    {
                        "type": "experience",
                        "values": experience_values,
                        "description": (
                            "Different experience durations "
                            "were reported."
                        ),
                    }
                )

        availability_values = [
            value
            for value in (
                self._normalize_text_claim(
                    item["availability"]
                )
                for item in claims
            )
            if value
        ]

        if len(set(availability_values)) > 1:
            conflicts.append(
                {
                    "type": "availability",
                    "values": availability_values,
                    "description": (
                        "Different availability or joining "
                        "information was reported."
                    ),
                }
            )

        salary_values = [
            value
            for value in (
                self._normalize_text_claim(
                    item["salary_expectation"]
                )
                for item in claims
            )
            if value
        ]

        if len(set(salary_values)) > 1:
            conflicts.append(
                {
                    "type": "salary_expectation",
                    "values": salary_values,
                    "description": (
                        "Different salary expectations "
                        "were reported."
                    ),
                }
            )

        within_response_scores = []

        for response in responses:
            text = str(
                response.get("response", "") or ""
            ).strip()

            if text:
                analysis = self.confidence_analyzer.analyze(
                    text
                )
                within_response_scores.append(
                    float(
                        analysis["contradictions"]["score"]
                    )
                )

        within_score = (
            sum(within_response_scores)
            / len(within_response_scores)
            if within_response_scores
            else 0.0
        )

        if not within_response_scores:
            return {
                "score": 0.0,
                "within_response_score": 0.0,
                "cross_response_score": 0.0,
                "conflict_count": 0,
                "conflicts": [],
                "responses_analyzed": len(responses),
            }

        # Each distinct cross-response conflict reduces the
        # cross-response score by 25 points.
        conflict_penalty = min(
            100.0,
            len(conflicts) * 25.0,
        )

        cross_response_score = max(
            0.0,
            100.0 - conflict_penalty,
        )

        consistency_score = self._normalize_score(
            (within_score * 0.50)
            + (cross_response_score * 0.50)
        )

        return {
            "score": consistency_score,
            "within_response_score": self._normalize_score(
                within_score
            ),
            "cross_response_score": self._normalize_score(
                cross_response_score
            ),
            "conflict_count": len(conflicts),
            "conflicts": conflicts,
            "responses_analyzed": len(responses),
        }

    def score_category(
        self,
        responses: List[Dict[str, Any]],
        category: str | HRInterviewCategory,
    ) -> Dict[str, Any]:
        """Calculate a normalized score for one HR interview category."""

        if isinstance(category, HRInterviewCategory):
            category_value = category.value
        else:
            category_value = category

        category_responses = [
            response
            for response in responses
            if response.get("category") == category_value
        ]

        if not category_responses:
            return {
                "category": category_value,
                "response_count": 0,
                "score": 0.0,
                "status": "not_evaluated",
            }

        scored_responses = [
            self.score_response(
                response=response.get("response", ""),
                category=category_value,
                duration_seconds=response.get(
                    "duration_seconds"
                ),
                question=response.get(
                    "question",
                    "",
                ),
            )
            for response in category_responses
        ]

        average_score = (
            sum(
                item["score"]
                for item in scored_responses
            )
            / len(scored_responses)
        )

        average_combined_score = (
            sum(
                item["combined_score"]
                for item in scored_responses
            )
            / len(scored_responses)
        )

        dimension_scores = {
            "answer_relevance_score": self._normalize_score(
                sum(
                    item["answer_relevance_score"]
                    for item in scored_responses
                )
                / len(scored_responses)
            ),
            "communication_score": self._normalize_score(
                sum(
                    item["communication_score"]
                    for item in scored_responses
                )
                / len(scored_responses)
            ),
            "behavioral_confidence_score": self._normalize_score(
                sum(
                    item["behavioral_confidence_score"]
                    for item in scored_responses
                )
                / len(scored_responses)
            ),
            "consistency_score": self._normalize_score(
                sum(
                    item["consistency_score"]
                    for item in scored_responses
                )
                / len(scored_responses)
            ),
        }

        return {
            "category": category_value,
            "response_count": len(scored_responses),
            "score": self._normalize_score(
                average_score
            ),
            "hr_score": self._normalize_score(
                average_combined_score
            ),
            "status": "evaluated",
            "dimension_scores": dimension_scores,
            "responses": scored_responses,
        }

    def score_interview(
        self,
        responses: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Score the complete HR interview.

        Normalization is performed by averaging each dimension inside
        each evaluated category first, then averaging categories
        equally. Therefore, adding more questions to one category
        does not automatically increase its influence.
        """

        if not isinstance(responses, list):
            raise TypeError(
                "responses must be a list."
            )

        category_scores = {}

        for category in HR_INTERVIEW_CATEGORY_ORDER:
            result = self.score_category(
                responses=responses,
                category=category,
            )

            category_scores[category.value] = result

        evaluated_categories = [
            result
            for result in category_scores.values()
            if result["status"] == "evaluated"
        ]

        consistency_result = self._score_consistency(
            responses
        )

        if not evaluated_categories:
            dimension_scores = {
                "answer_relevance": 0.0,
                "communication_score": 0.0,
                "confidence_score": 0.0,
                "consistency": 0.0,
            }

        else:
            dimension_scores = {
                "answer_relevance": self._normalize_score(
                    sum(
                        result["dimension_scores"][
                            "answer_relevance_score"
                        ]
                        for result in evaluated_categories
                    )
                    / len(evaluated_categories)
                ),
                "communication_score": self._normalize_score(
                    sum(
                        result["dimension_scores"][
                            "communication_score"
                        ]
                        for result in evaluated_categories
                    )
                    / len(evaluated_categories)
                ),
                "confidence_score": self._normalize_score(
                    sum(
                        result["dimension_scores"][
                            "behavioral_confidence_score"
                        ]
                        for result in evaluated_categories
                    )
                    / len(evaluated_categories)
                ),
                "consistency": consistency_result[
                    "score"
                ],
            }

        contributions = {
            name: round(
                dimension_scores[name]
                * self.hr_scoring_weights[name],
                2,
            )
            for name in dimension_scores
        }

        overall_score = self._normalize_score(
            sum(contributions.values())
        )

        strengths = [
            name
            for name, score in dimension_scores.items()
            if score >= 80
        ]

        improvement_areas = [
            name
            for name, score in dimension_scores.items()
            if score < 60
        ]

        if overall_score >= 80:
            overall_rating = "strong"
        elif overall_score >= 60:
            overall_rating = "moderate"
        else:
            overall_rating = "needs_improvement"

        return {
            "overall_score": overall_score,
            "overall_rating": overall_rating,
            "category_scores": category_scores,
            "dimension_scores": dimension_scores,
            "scoring_weights": self.hr_scoring_weights.copy(),
            "score_contributions": contributions,
            "consistency_analysis": consistency_result,
            "evaluated_category_count": len(
                evaluated_categories
            ),
            "total_response_count": len(
                responses
            ),
            "strengths": strengths,
            "improvement_areas": improvement_areas,
            "normalization": {
                "method": (
                    "equal-weight category averages"
                ),
                "evaluated_categories": len(
                    evaluated_categories
                ),
                "response_count": len(
                    responses
                ),
            },
        }

    def score_interview_state(
        self,
        interview_state: Any,
    ) -> Dict[str, Any]:
        """Score an InterviewState instance."""

        if not hasattr(
            interview_state,
            "responses",
        ):
            raise TypeError(
                "interview_state must contain "
                "a responses attribute."
            )

        responses = []

        for response in interview_state.responses:
            responses.append(
                {
                    "question_id": response.question_id,
                    "question": getattr(
                        response,
                        "question",
                        "",
                    ),
                    "response": response.response,
                    "response_type": response.response_type,
                    "category": response.category,
                }
            )

        result = self.score_interview(
            responses
        )

        result["session_id"] = getattr(
            interview_state,
            "session_id",
            None,
        )
        result["candidate_id"] = getattr(
            interview_state,
            "candidate_id",
            None,
        )
        result["role"] = getattr(
            interview_state,
            "role",
            None,
        )
        result["experience_level"] = getattr(
            interview_state,
            "experience_level",
            None,
        )
        result["completed"] = getattr(
            interview_state,
            "completed",
            False,
        )

        return result
