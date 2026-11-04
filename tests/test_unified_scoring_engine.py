
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


# Day 51: Five-stage cross-round aggregation tests

def test_five_stage_calculation_with_all_scores():
    engine = UnifiedScoringEngine()

    result = engine.calculate_five_stage_hiring_fit(
        ats_score=80,
        screening_score=70,
        hr_interview_score=90,
        technical_interview_score=85,
        machine_test_score=75,
    )

    assert result["hiring_fit_percentage"] == 80.0
    assert result["evidence_complete"] is True
    assert result["human_review_required"] is False
    assert len(result["available_stages"]) == 5


def test_missing_scores_are_not_treated_as_zero():
    engine = UnifiedScoringEngine()

    result = engine.calculate_five_stage_hiring_fit(
        ats_score=80,
        technical_interview_score=60,
    )

    assert result["hiring_fit_percentage"] == 70.0
    assert result["round_scores"]["machine_test"] is None
    assert "machine_test" in result["missing_stages"]
    assert result["evidence_complete"] is False
    assert result["human_review_required"] is True


def test_zero_is_a_valid_available_score():
    engine = UnifiedScoringEngine()

    result = engine.calculate_five_stage_hiring_fit(
        ats_score=0,
        screening_score=100,
    )

    assert result["round_scores"]["ats"] == 0
    assert result["hiring_fit_percentage"] == 50.0
    assert "ats" in result["available_stages"]


def test_five_stage_weights_are_normalized():
    engine = UnifiedScoringEngine()

    result = engine.calculate_five_stage_hiring_fit(
        ats_score=80,
        screening_score=80,
    )

    assert sum(result["weights"].values()) == 1.0
    assert result["weights"]["ats"] == 0.5
    assert result["weights"]["screening"] == 0.5


def test_five_stage_invalid_scores_are_rejected():
    engine = UnifiedScoringEngine()

    with pytest.raises(ValueError):
        engine.calculate_five_stage_hiring_fit(
            ats_score=80,
            screening_score=101,
        )


def test_five_stage_boolean_scores_are_rejected():
    engine = UnifiedScoringEngine()

    with pytest.raises(ValueError):
        engine.calculate_five_stage_hiring_fit(
            ats_score=True,
        )


def test_five_stage_requires_at_least_one_score():
    engine = UnifiedScoringEngine()

    with pytest.raises(ValueError):
        engine.calculate_five_stage_hiring_fit()


def test_custom_five_stage_role_weights():
    custom_weights = {
        "ats": 0.10,
        "screening": 0.10,
        "hr_interview": 0.20,
        "technical_interview": 0.30,
        "machine_test": 0.30,
    }

    engine = UnifiedScoringEngine(
        five_stage_role_weights={
            "Test Engineer": custom_weights
        }
    )

    result = engine.calculate_five_stage_hiring_fit(
        ats_score=80,
        screening_score=80,
        hr_interview_score=80,
        technical_interview_score=80,
        machine_test_score=80,
        role="Test Engineer",
    )

    assert result["configured_weights"] == custom_weights
    assert result["hiring_fit_percentage"] == 80.0


def test_full_candidate_score_contains_five_stage_details():
    engine = UnifiedScoringEngine()

    result = engine.build_full_candidate_score(
        candidate_id="C101",
        candidate_name="Test Candidate",
        role="Software Engineer",
        ats_score=80,
        screening_score=75,
        hr_interview_score=85,
        technical_interview_score=90,
        machine_test_score=80,
    )

    assert result["candidate_id"] == "C101"
    assert result["candidate_name"] == "Test Candidate"
    assert result["job_role"] == "Software Engineer"
    assert result["evidence_complete"] is True
    assert len(result["round_scores"]) == 5

@pytest.mark.parametrize(
    "stage_scores, expected_complete",
    [
        (
            {
                "ats_score": 80,
                "screening_score": 70,
                "hr_interview_score": 90,
                "technical_interview_score": 85,
                "machine_test_score": 75,
            },
            True,
        ),
        (
            {
                "ats_score": 80,
                "screening_score": 70,
                "hr_interview_score": 90,
                "technical_interview_score": 85,
            },
            False,
        ),
    ],
)
def test_cross_round_evidence_completeness_is_consistent(
    stage_scores, expected_complete
):
    result = UnifiedScoringEngine().calculate_five_stage_hiring_fit(
        **stage_scores
    )

    assert result["evidence_complete"] is expected_complete
    assert result["human_review_required"] is (not expected_complete)
    assert len(result["available_stages"]) + len(result["missing_stages"]) == 5
