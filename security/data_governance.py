"""Application-level audit, consent, storage, and access controls."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def require_consent(interview_state: Any) -> None:
    """Reject governed data operations unless explicit consent is present."""
    if not getattr(interview_state, "consent_given", False):
        raise PermissionError("Candidate consent is required for this operation.")


class AccessControl:
    """Simple deny-by-default role-based permission checks."""

    ROLE_PERMISSIONS = {
        "admin": {"read_candidate", "record_interview", "read_report",
                  "log_decision", "read_audit", "manage_data"},
        "recruiter": {"read_candidate", "read_report", "log_decision"},
        "interviewer": {"read_candidate", "record_interview"},
        "auditor": {"read_audit"},
    }

    @classmethod
    def has_permission(cls, role: str, permission: str) -> bool:
        return permission in cls.ROLE_PERMISSIONS.get(role, set())

    @classmethod
    def require_permission(cls, role: str, permission: str) -> None:
        if not cls.has_permission(role, permission):
            raise PermissionError(
                f"Role '{role}' is not permitted to perform '{permission}'."
            )


class AuditTrail:
    """Append structured audit events without storing raw candidate answers."""

    SAFE_METADATA_KEYS = {
        "stage", "score", "decision", "reason_code",
        "model_version", "action",
    }

    def __init__(self, log_path: str | Path) -> None:
        self.log_path = Path(log_path)

    def log_event(
        self,
        event_type: str,
        actor_id: str,
        candidate_id: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        if not isinstance(event_type, str) or not event_type.strip():
            raise ValueError("event_type must be a non-empty string")
        if not isinstance(actor_id, str) or not actor_id.strip():
            raise ValueError("actor_id must be a non-empty string")

        safe_metadata = {}
        for key, value in (metadata or {}).items():
            if key not in self.SAFE_METADATA_KEYS:
                continue
            if isinstance(value, (str, int, float, bool)) or value is None:
                safe_metadata[key] = value

        event = {
            "timestamp": _utc_now().isoformat(),
            "event_type": event_type.strip(),
            "actor_id": actor_id.strip(),
            "candidate_id": candidate_id,
            "metadata": safe_metadata,
        }

        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(
            self.log_path,
            os.O_CREAT | os.O_APPEND | os.O_WRONLY,
            0o600,
        )
        with os.fdopen(descriptor, "a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(event, ensure_ascii=False) + "\n")

        try:
            self.log_path.chmod(0o600)
        except OSError:
            pass

        return event

    def read_events(self) -> list[dict[str, Any]]:
        if not self.log_path.exists():
            return []
        events = []
        with self.log_path.open("r", encoding="utf-8") as log_file:
            for line in log_file:
                if line.strip():
                    events.append(json.loads(line))
        return events


class SecureDataStorage:
    """Consent-checked local storage with path validation and expiry cleanup.

    File permissions are best-effort. Production deployments must also
    configure operating-system ACLs, encryption, backups, and key management.
    """

    def __init__(self, root_dir: str | Path) -> None:
        self.root_dir = Path(root_dir).resolve()
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def _safe_path(self, relative_path: str | Path) -> Path:
        requested = Path(relative_path)
        if requested.is_absolute():
            raise ValueError("Storage path must be relative")

        destination = (self.root_dir / requested).resolve()
        if not destination.is_relative_to(self.root_dir):
            raise ValueError("Storage path must remain inside the storage directory")
        return destination

    def save_text(
        self,
        relative_path: str | Path,
        content: str,
        interview_state: Any,
        retention_days: int = 90,
    ) -> Path:
        require_consent(interview_state)
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        if isinstance(retention_days, bool) or not isinstance(retention_days, int):
            raise ValueError("retention_days must be a positive integer")
        if retention_days < 1:
            raise ValueError("retention_days must be a positive integer")

        destination = self._safe_path(relative_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

        try:
            destination.chmod(0o600)
        except OSError:
            pass

        return destination

    def purge_expired(
        self,
        retention_days: int = 90,
        now: Optional[datetime] = None,
    ) -> int:
        if isinstance(retention_days, bool) or not isinstance(retention_days, int):
            raise ValueError("retention_days must be a positive integer")
        if retention_days < 1:
            raise ValueError("retention_days must be a positive integer")

        current_time = now or _utc_now()
        if current_time.tzinfo is None:
            raise ValueError("now must be timezone-aware")

        cutoff = (
            current_time.astimezone(timezone.utc)
            - timedelta(days=retention_days)
        ).timestamp()

        removed = 0
        for file_path in self.root_dir.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.stat().st_mtime < cutoff:
                file_path.unlink()
                removed += 1
        return removed
