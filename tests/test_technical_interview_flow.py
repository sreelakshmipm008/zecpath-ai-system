import pytest

from interview_ai.technical_interview_flow import (
    TechnicalInterviewFlow,
    TechnicalInterviewPhase,
)


def test_initial_phase():
    flow = TechnicalInterviewFlow("TEST-001")

    assert flow.current_phase == TechnicalInterviewPhase.INTRODUCTION
    assert flow.history == ["introduction"]
    assert not flow.is_complete


def test_all_phases_follow_correct_order():
    flow = TechnicalInterviewFlow("TEST-002")

    expected = [
        "introduction",
        "experience_based",
        "conceptual",
        "scenario_based",
        "closing",
        "completed",
    ]

    for _ in range(5):
        flow.advance()

    assert flow.history == expected
    assert flow.is_complete


def test_transition_to_next_phase():
    flow = TechnicalInterviewFlow()
    result = flow.transition_to("experience_based")

    assert result == TechnicalInterviewPhase.EXPERIENCE


def test_skipping_phase_is_rejected():
    flow = TechnicalInterviewFlow()

    with pytest.raises(ValueError, match="Invalid transition"):
        flow.transition_to("conceptual")


def test_backward_transition_is_rejected():
    flow = TechnicalInterviewFlow()
    flow.advance()

    with pytest.raises(ValueError, match="Invalid transition"):
        flow.transition_to("introduction")


def test_unknown_phase_is_rejected():
    flow = TechnicalInterviewFlow()

    with pytest.raises(ValueError, match="Unknown interview phase"):
        flow.transition_to("technical_test")


def test_cannot_advance_after_completion():
    flow = TechnicalInterviewFlow()

    for _ in range(5):
        flow.advance()

    with pytest.raises(ValueError, match="already completed"):
        flow.advance()


def test_to_dict_returns_session_state():
    flow = TechnicalInterviewFlow("SESSION-123")
    flow.advance()

    result = flow.to_dict()

    assert result["session_id"] == "SESSION-123"
    assert result["current_phase"] == "experience_based"
    assert result["history"] == ["introduction", "experience_based"]
    assert result["is_complete"] is False

@pytest.mark.parametrize("phase", [None, [], {}, 123])
def test_invalid_phase_input_is_rejected(phase):
    flow = TechnicalInterviewFlow()
    with pytest.raises(ValueError, match="Unknown interview phase"):
        flow.transition_to(phase)
