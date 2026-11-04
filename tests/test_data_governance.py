from datetime import datetime, timedelta, timezone

import pytest

from interview_ai.interview_state import InterviewState
from security.data_governance import (
    AccessControl,
    AuditTrail,
    SecureDataStorage,
    require_consent,
)


def test_governed_operation_requires_candidate_consent():
    state = InterviewState(session_id="governance-1")
    with pytest.raises(PermissionError, match="consent"):
        require_consent(state)

    state.grant_consent()
    require_consent(state)


def test_audit_trail_records_score_and_decision_without_raw_answers(tmp_path):
    trail = AuditTrail(tmp_path / "logs" / "audit.jsonl")
    trail.log_event(
        "decision_recorded",
        actor_id="recruiter-1",
        candidate_id="candidate-1",
        metadata={
            "score": 84.5,
            "decision": "Review",
            "reason_code": "HUMAN_REVIEW",
            "transcript": "private candidate answer",
        },
    )

    events = trail.read_events()
    assert len(events) == 1
    assert events[0]["metadata"]["score"] == 84.5
    assert events[0]["metadata"]["decision"] == "Review"
    assert "transcript" not in events[0]["metadata"]
    assert "private candidate answer" not in str(events)


def test_audit_trail_appends_multiple_events(tmp_path):
    trail = AuditTrail(tmp_path / "audit.jsonl")
    trail.log_event("score_calculated", "system", metadata={"score": 75})
    trail.log_event("decision_recorded", "recruiter", metadata={"decision": "Hold"})

    assert len(trail.read_events()) == 2


def test_storage_requires_consent_and_rejects_path_traversal(tmp_path):
    storage = SecureDataStorage(tmp_path / "candidate_data")
    state = InterviewState(session_id="governance-2")

    with pytest.raises(PermissionError, match="consent"):
        storage.save_text("report.txt", "report", state)

    state.grant_consent()
    with pytest.raises(ValueError, match="inside"):
        storage.save_text("../outside.txt", "report", state)


def test_storage_saves_and_purges_expired_files(tmp_path):
    storage = SecureDataStorage(tmp_path / "candidate_data")
    state = InterviewState(session_id="governance-3")
    state.grant_consent()

    saved = storage.save_text("reports/report.txt", "approved report", state)
    assert saved.exists()
    assert saved.read_text(encoding="utf-8") == "approved report"

    old_time = (datetime.now(timezone.utc) - timedelta(days=100)).timestamp()
    import os
    os.utime(saved, (old_time, old_time))

    removed = storage.purge_expired(retention_days=90)
    assert removed == 1
    assert not saved.exists()


def test_access_control_denies_unauthorized_roles():
    assert AccessControl.has_permission("recruiter", "log_decision")
    assert AccessControl.has_permission("auditor", "read_audit")
    assert not AccessControl.has_permission("interviewer", "log_decision")
    assert not AccessControl.has_permission("unknown", "read_candidate")

    with pytest.raises(PermissionError):
        AccessControl.require_permission("unknown", "read_candidate")
