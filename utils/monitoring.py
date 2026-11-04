"""AI monitoring, observability, metrics, and alerting utilities."""

from __future__ import annotations

import json
import logging
import threading
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


logger = logging.getLogger(__name__)


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


class AIMonitor:
    """Record AI operation events and expose operational metrics."""

    def __init__(
        self,
        log_path: str | Path = "logs/ai_monitoring.jsonl",
        audit_trail: Any = None,
        slow_response_ms: float = 2000.0,
        failure_rate_threshold: float = 0.10,
    ) -> None:
        if slow_response_ms <= 0:
            raise ValueError("slow_response_ms must be positive")
        if not 0 <= failure_rate_threshold <= 1:
            raise ValueError("failure_rate_threshold must be between 0 and 1")

        self.log_path = Path(log_path)
        self.audit_trail = audit_trail
        self.slow_response_ms = float(slow_response_ms)
        self.failure_rate_threshold = float(failure_rate_threshold)

        self._lock = threading.Lock()
        self._counts = Counter()
        self._response_times: list[float] = []
        self._accuracy_correct = 0
        self._accuracy_total = 0

    def _write_event(self, event: dict[str, Any]) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock:
            with self.log_path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(event, ensure_ascii=False) + "\n")

    def log_request(
        self,
        operation: str,
        request_id: Optional[str] = None,
        method: Optional[str] = None,
    ) -> str:
        """Record request metadata without storing request payloads."""
        if not isinstance(operation, str) or not operation.strip():
            raise ValueError("operation must be a non-empty string")

        identifier = request_id or str(uuid.uuid4())
        self._write_event({
            "timestamp": _timestamp(),
            "event_type": "request",
            "request_id": identifier,
            "operation": operation.strip(),
            "method": method,
        })
        with self._lock:
            self._counts["requests"] += 1
        return identifier

    def record_model_output(
        self,
        request_id: str,
        model_name: str,
        output_summary: Optional[dict[str, Any]] = None,
        actual_label: Any = None,
        predicted_label: Any = None,
    ) -> None:
        """Record safe output metadata and optional labelled accuracy."""
        safe_summary = {}
        allowed_keys = {"score", "decision", "status", "model_version"}

        for key, value in (output_summary or {}).items():
            if key in allowed_keys and (
                isinstance(value, (str, int, float, bool)) or value is None
            ):
                safe_summary[key] = value

        event = {
            "timestamp": _timestamp(),
            "event_type": "model_output",
            "request_id": request_id,
            "model_name": model_name,
            "output_summary": safe_summary,
        }
        self._write_event(event)

        if actual_label is not None and predicted_label is not None:
            with self._lock:
                self._accuracy_total += 1
                if actual_label == predicted_label:
                    self._accuracy_correct += 1

    def record_error(
        self,
        request_id: str,
        operation: str,
        error: Exception,
    ) -> None:
        """Record error type and message without candidate information."""
        event = {
            "timestamp": _timestamp(),
            "event_type": "error",
            "request_id": request_id,
            "operation": operation,
            "error_type": type(error).__name__,
            "error_message": str(error)[:500],
        }
        self._write_event(event)
        with self._lock:
            self._counts["failures"] += 1
        logger.error(
            "AI operation failed: %s (%s)",
            operation,
            type(error).__name__,
        )

    def record_response(
        self,
        request_id: str,
        operation: str,
        duration_ms: float,
        success: bool = True,
    ) -> None:
        """Record operation duration and completion status."""
        if duration_ms < 0:
            raise ValueError("duration_ms cannot be negative")

        event = {
            "timestamp": _timestamp(),
            "event_type": "response",
            "request_id": request_id,
            "operation": operation,
            "duration_ms": round(float(duration_ms), 3),
            "success": bool(success),
        }
        self._write_event(event)

        with self._lock:
            self._response_times.append(float(duration_ms))
            self._counts["completed"] += 1
            if not success:
                self._counts["failures"] += 1

    def record_decision(
        self,
        actor_id: str,
        decision: str,
        candidate_id: Optional[str] = None,
        score: Optional[float] = None,
        reason_code: Optional[str] = None,
        model_version: Optional[str] = None,
    ) -> None:
        """Send a decision audit event through the existing AuditTrail."""
        if self.audit_trail is None:
            raise RuntimeError("An AuditTrail instance is required")

        metadata = {
            "decision": decision,
            "score": score,
            "reason_code": reason_code,
            "model_version": model_version,
            "action": "ai_decision",
        }
        self.audit_trail.log_event(
            event_type="ai_decision",
            actor_id=actor_id,
            candidate_id=candidate_id,
            metadata=metadata,
        )

    def metrics(self) -> dict[str, Any]:
        """Return a snapshot of operational and labelled accuracy metrics."""
        with self._lock:
            requests = self._counts["requests"]
            failures = self._counts["failures"]
            completed = self._counts["completed"]
            response_times = list(self._response_times)
            accuracy_total = self._accuracy_total
            accuracy_correct = self._accuracy_correct

        failure_rate = failures / completed if completed else 0.0
        accuracy = (
            accuracy_correct / accuracy_total
            if accuracy_total
            else None
        )

        return {
            "total_requests": requests,
            "completed_operations": completed,
            "failed_operations": failures,
            "failure_rate": round(failure_rate, 4),
            "average_response_time_ms": (
                round(sum(response_times) / len(response_times), 3)
                if response_times else 0.0
            ),
            "max_response_time_ms": (
                round(max(response_times), 3)
                if response_times else 0.0
            ),
            "labelled_accuracy": (
                round(accuracy, 4) if accuracy is not None else None
            ),
            "accuracy_samples": accuracy_total,
        }

    def check_alerts(self) -> list[dict[str, Any]]:
        """Evaluate configured operational alert thresholds."""
        snapshot = self.metrics()
        alerts = []

        if (
            snapshot["completed_operations"] > 0
            and snapshot["failure_rate"] > self.failure_rate_threshold
        ):
            alerts.append({
                "level": "warning",
                "metric": "failure_rate",
                "value": snapshot["failure_rate"],
                "threshold": self.failure_rate_threshold,
                "message": "AI operation failure rate exceeded threshold.",
            })

        if snapshot["max_response_time_ms"] > self.slow_response_ms:
            alerts.append({
                "level": "warning",
                "metric": "response_time_ms",
                "value": snapshot["max_response_time_ms"],
                "threshold": self.slow_response_ms,
                "message": "AI response time exceeded threshold.",
            })

        return alerts

    def dashboard_snapshot(self) -> dict[str, Any]:
        """Provide data for a monitoring dashboard."""
        return {
            "generated_at": _timestamp(),
            "metrics": self.metrics(),
            "alerts": self.check_alerts(),
        }
