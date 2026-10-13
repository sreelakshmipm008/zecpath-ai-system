from datetime import datetime, timedelta, timezone

import pytest

from interview_ai.interview_state import InterviewState


def test_response_recording_requires_consent():
    state = InterviewState(session_id="privacy-1")

    with pytest.raises(PermissionError, match="consent"):
        state.record_response(
            question_id="Q001",
            response="Candidate answer",
        )

    assert state.responses == []


def test_consent_is_recorded_in_serialized_state():
    state = InterviewState(session_id="privacy-2")
    state.grant_consent()

    data = state.to_dict()

    assert data["consent_given"] is True
    assert data["consent_recorded_at"] is not None


def test_withdrawing_consent_clears_responses():
    state = InterviewState(session_id="privacy-3")
    state.grant_consent()
    state.record_response(
        question_id="Q001",
        response="Candidate answer",
    )

    state.withdraw_consent()

    assert state.consent_given is False
    assert state.responses == []

    with pytest.raises(PermissionError):
        state.record_response(
            question_id="Q002",
            response="Another answer",
        )


def test_expired_responses_are_purged():
    state = InterviewState(session_id="privacy-4", retention_days=30)
    state.grant_consent()

    now = datetime.now(timezone.utc)
    state.record_response(question_id="OLD", response="Old answer")
    state.record_response(question_id="NEW", response="Recent answer")

    state.responses[0].recorded_at = now - timedelta(days=31)
    state.responses[1].recorded_at = now - timedelta(days=2)

    removed = state.purge_expired_responses(now=now)

    assert removed == 1
    assert [response.question_id for response in state.responses] == ["NEW"]


def test_retention_period_must_be_positive():
    with pytest.raises(ValueError, match="retention_days"):
        InterviewState(session_id="privacy-5", retention_days=0)
