from scoring.end_to_end_simulation import run_simulation


def test_end_to_end_simulation_runs_all_candidates():
    report = run_simulation()
    assert report["candidate_count"] == 3
    assert len(report["candidates"]) == 3
    assert 0 <= report["reference_agreement_percentage"] <= 100


def test_every_candidate_has_all_five_stage_scores():
    report = run_simulation()
    expected = {
        "ats", "screening", "hr_interview",
        "technical_interview", "machine_test"
    }
    for candidate in report["candidates"]:
        assert set(candidate["stage_scores"]) == expected
        assert candidate["evidence_complete"] is True


def test_recommendations_keep_human_authority():
    report = run_simulation()
    for candidate in report["candidates"]:
        assert candidate["recommendation"]["review_required"] is True
        assert candidate["recommendation"]["final_decision_authority"] == "Human recruiter"


def test_simulated_human_reference_is_explicitly_labelled():
    report = run_simulation()
    for candidate in report["candidates"]:
        assert "simulated_human_reference" in candidate
