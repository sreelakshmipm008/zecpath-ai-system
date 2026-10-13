
import pytest

from scoring.unified_scoring_engine import UnifiedScoringEngine


def test_default_hiring_fit_calculation():
    engine = UnifiedScoringEngine()

    result = engine.calculate_hiring_fit(
        ats_score=80,
        screening_score=60,
        hr_interview_score=90,
    )

    assert result["hiring_fit_percentage"] == 78.5
    assert result["unified_score"] == 78.5


def test_role_specific_weights_are_applied():
    engine = UnifiedScoringEngine()

    result = engine.calculate_hiring_fit(
        ats_score=80,
        screening_score=60,
        hr_interview_score=90,
        role="Data Analyst",
    )

    assert result["weights"] == {
        "ats": 0.45,
        "screening": 0.25,
        "hr_interview": 0.30,
    }
    assert result["hiring_fit_percentage"] == 78.0


def test_unknown_role_uses_default_weights():
    engine = UnifiedScoringEngine()

    result = engine.calculate_hiring_fit(
        ats_score=80,
        screening_score=60,
        hr_interview_score=90,
        role="Unconfigured Role",
    )

    assert result["weights"] == engine.DEFAULT_WEIGHTS
    assert result["hiring_fit_percentage"] == 78.5


def test_candidate_score_object_contains_required_fields():
    engine = UnifiedScoringEngine()

    result = engine.build_candidate_score(
        candidate_id="C001",
        candidate_name="Test Candidate",
        role="Data Analyst",
        ats_score=80,
        screening_score=60,
        hr_interview_score=90,
    )

    assert result["candidate_id"] == "C001"
    assert result["candidate_name"] == "Test Candidate"
    assert result["job_role"] == "Data Analyst"
    assert result["round_scores"]["ats"] == 80
    assert result["round_scores"]["screening"] == 60
    assert result["round_scores"]["hr_interview"] == 90
    assert result["hiring_fit_percentage"] == 78.0
    assert result["unified_score"] == 78.0


@pytest.mark.parametrize(
    "invalid_score",
    [-1, 101, "80", None, True],
)
def test_invalid_scores_are_rejected(invalid_score):
    engine = UnifiedScoringEngine()

    with pytest.raises(ValueError):
        engine.calculate_hiring_fit(
            ats_score=invalid_score,
            screening_score=60,
            hr_interview_score=90,
        )


def test_weights_must_sum_to_one():
    with pytest.raises(ValueError):
        UnifiedScoringEngine(
            role_weights={
                "Test Role": {
                    "ats": 0.5,
                    "screening": 0.3,
                    "hr_interview": 0.3,
                }
            }
        )


def test_weight_configuration_must_have_all_rounds():
    with pytest.raises(ValueError):
        UnifiedScoringEngine(
            role_weights={
                "Test Role": {
                    "ats": 0.5,
                    "screening": 0.5,
                }
            }
        )


def test_custom_role_weights_are_supported():
    engine = UnifiedScoringEngine(
        role_weights={
            "Product Designer": {
                "ats": 0.30,
                "screening": 0.30,
                "hr_interview": 0.40,
            }
        }
    )

    result = engine.calculate_hiring_fit(
        ats_score=80,
        screening_score=60,
        hr_interview_score=90,
        role="Product Designer",
    )

    assert result["hiring_fit_percentage"] == 78.0
