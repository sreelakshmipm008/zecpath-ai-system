import pytest

from scoring.final_recommendation_engine import FinalRecommendationEngine


@pytest.fixture
def complete_candidate_score():
    return {
        "candidate_id": "C101",
        "candidate_name": "Test Candidate",
        "job_role": "Data Analyst",
        "hiring_fit_percentage": 85,
        "unified_score": 85,
        "evidence_complete": True,
        "round_scores": {
            "ats": 85,
            "screening": 80,
            "hr_interview": 90,
            "technical_interview": 85,
            "machine_test": 85,
        },
    }


@pytest.fixture
def eligible_result():
    return {
        "eligibility_status": "Eligible",
        "eligibility_reasons": [],
    }


def test_complete_candidate_is_recommended_selected(
    complete_candidate_score, eligible_result
):
    engine = FinalRecommendationEngine()

    result = engine.generate_recommendation(
        complete_candidate_score, eligible_result
    )

    assert result["decision_category"] == "Selected"
    assert result["review_required"] is True
    assert result["final_decision_authority"] == "Human recruiter"


def test_missing_stage_results_in_hold(
    complete_candidate_score, eligible_result
):
    engine = FinalRecommendationEngine()
    complete_candidate_score["evidence_complete"] = False
    complete_candidate_score["round_scores"]["machine_test"] = None

    result = engine.generate_recommendation(
        complete_candidate_score, eligible_result
    )

    assert result["decision_category"] == "Hold / Review"
    assert "machine_test" in result["recommendation_confidence"]["missing_stages"]


def test_eligibility_review_results_in_hold(
    complete_candidate_score
):
    engine = FinalRecommendationEngine()

    result = engine.generate_recommendation(
        complete_candidate_score,
        {
            "eligibility_status": "Review",
            "eligibility_reasons": ["Mandatory skill requires verification."],
        },
    )

    assert result["decision_category"] == "Hold / Review"
    assert result["eligibility_findings"]


def test_eligibility_rejection_is_reported(
    complete_candidate_score
):
    engine = FinalRecommendationEngine()

    result = engine.generate_recommendation(
        complete_candidate_score,
        {
            "eligibility_status": "Rejected",
            "eligibility_reasons": ["Minimum requirement not met."],
        },
    )

    assert result["decision_category"] == "Rejected"
    assert result["review_required"] is True
    assert result["review_items"]


def test_hr_risk_flags_require_review(
    complete_candidate_score, eligible_result
):
    engine = FinalRecommendationEngine()

    result = engine.generate_recommendation(
        complete_candidate_score,
        eligible_result,
        hr_summary={"risk_flags": ["Conflicting interview responses."]},
    )

    assert result["decision_category"] == "Hold / Review"
    assert result["hr_risk_findings"]


def test_integrity_alerts_require_separate_review(
    complete_candidate_score, eligible_result
):
    engine = FinalRecommendationEngine()

    result = engine.generate_recommendation(
        complete_candidate_score,
        eligible_result,
        integrity_alerts=[{"event": "tab_switch", "review_status": "pending"}],
    )

    assert result["decision_category"] == "Hold / Review"
    assert result["integrity_review_items"]
    assert result["review_required"] is True


def test_behavioral_observations_alone_do_not_change_recommendation(
    complete_candidate_score, eligible_result
):
    engine = FinalRecommendationEngine()

    result = engine.generate_recommendation(
        complete_candidate_score,
        eligible_result,
        behavioral_report={"sentiment": "negative", "score": 10},
    )

    assert result["decision_category"] == "Selected"
    assert result["behavioral_observations"]["sentiment"] == "negative"


def test_evidence_confidence_is_not_probability(
    complete_candidate_score, eligible_result
):
    engine = FinalRecommendationEngine()

    result = engine.generate_recommendation(
        complete_candidate_score, eligible_result
    )

    confidence = result["recommendation_confidence"]

    assert confidence["score"] == 100
    assert confidence["level"] == "complete"
    assert "not a probability" in confidence["meaning"]


def test_invalid_score_is_rejected(
    complete_candidate_score, eligible_result
):
    engine = FinalRecommendationEngine()
    complete_candidate_score["hiring_fit_percentage"] = 101

    with pytest.raises(ValueError):
        engine.generate_recommendation(
            complete_candidate_score, eligible_result
        )


def test_invalid_thresholds_are_rejected():
    with pytest.raises(ValueError):
        FinalRecommendationEngine(
            selected_threshold=60,
            rejected_threshold=80,
        )
def test_unresolved_risks_override_rejection_recommendation(
    complete_candidate_score
):
    engine = FinalRecommendationEngine()

    result = engine.generate_recommendation(
        complete_candidate_score,
        {
            "eligibility_status": "Rejected",
            "eligibility_reasons": ["Requirement needs verification."],
        },
        hr_summary={"risk_flags": ["Conflicting responses."]},
        integrity_alerts=[{"event": "pending_review"}],
    )

    assert result["decision_category"] == "Hold / Review"
    assert result["review_required"] is True

@pytest.mark.parametrize(
    "score, expected_category",
    [
        (80, "Selected"),
        (60, "Hold / Review"),
        (59.99, "Rejected"),
    ],
)
def test_recommendation_threshold_boundaries(
    complete_candidate_score, eligible_result, score, expected_category
):
    complete_candidate_score["hiring_fit_percentage"] = score
    complete_candidate_score["unified_score"] = score

    result = FinalRecommendationEngine().generate_recommendation(
        complete_candidate_score, eligible_result
    )

    assert result["decision_category"] == expected_category
