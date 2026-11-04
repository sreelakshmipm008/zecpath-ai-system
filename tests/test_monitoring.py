import json

import pytest

from security.data_governance import AuditTrail
from utils.monitoring import AIMonitor


def test_monitor_records_requests_outputs_and_responses(tmp_path):
    monitor = AIMonitor(log_path=tmp_path / "monitor.jsonl")

    request_id = monitor.log_request("candidate_scoring")
    monitor.record_model_output(
        request_id,
        "test-model",
        {"score": 85, "decision": "shortlist"},
        actual_label="shortlist",
        predicted_label="shortlist",
    )
    monitor.record_response(request_id, "candidate_scoring", 120, True)

    metrics = monitor.metrics()
    assert metrics["total_requests"] == 1
    assert metrics["completed_operations"] == 1
    assert metrics["labelled_accuracy"] == 1.0
    assert metrics["average_response_time_ms"] == 120


def test_monitor_records_errors_and_failure_metrics(tmp_path):
    monitor = AIMonitor(log_path=tmp_path / "monitor.jsonl")
    request_id = monitor.log_request("interview_analysis")

    monitor.record_error(
        request_id,
        "interview_analysis",
        ValueError("Processing failed"),
    )

    metrics = monitor.metrics()
    assert metrics["failed_operations"] == 1

    events = [
        json.loads(line)
        for line in (tmp_path / "monitor.jsonl").read_text().splitlines()
    ]
    assert any(event["event_type"] == "error" for event in events)


def test_monitor_generates_slow_response_alert(tmp_path):
    monitor = AIMonitor(
        log_path=tmp_path / "monitor.jsonl",
        slow_response_ms=100,
    )
    request_id = monitor.log_request("scoring")
    monitor.record_response(request_id, "scoring", 250, True)

    alerts = monitor.check_alerts()
    assert any(alert["metric"] == "response_time_ms" for alert in alerts)


def test_monitor_generates_failure_rate_alert(tmp_path):
    monitor = AIMonitor(
        log_path=tmp_path / "monitor.jsonl",
        failure_rate_threshold=0.20,
    )
    request_id = monitor.log_request("scoring")
    monitor.record_response(request_id, "scoring", 50, False)

    alerts = monitor.check_alerts()
    assert any(alert["metric"] == "failure_rate" for alert in alerts)


def test_monitor_audits_ai_decisions(tmp_path):
    audit = AuditTrail(tmp_path / "audit.jsonl")
    monitor = AIMonitor(
        log_path=tmp_path / "monitor.jsonl",
        audit_trail=audit,
    )

    monitor.record_decision(
        actor_id="system",
        candidate_id="candidate-001",
        decision="shortlist",
        score=90,
        reason_code="score_threshold_met",
        model_version="v1",
    )

    events = audit.read_events()
    assert len(events) == 1
    assert events[0]["event_type"] == "ai_decision"
    assert events[0]["metadata"]["decision"] == "shortlist"


def test_monitor_rejects_invalid_alert_thresholds(tmp_path):
    with pytest.raises(ValueError):
        AIMonitor(
            log_path=tmp_path / "monitor.jsonl",
            failure_rate_threshold=1.5,
        )
