"""
Day 33 - HR Interview State Structure.

Maintains interview state, consent, response capture, follow-up
eligibility, interview phase, and response-retention controls.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from interview_ai.hr_interview_categories import HRInterviewCategory


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC time."""
    return datetime.now(timezone.utc)


@dataclass
class InterviewResponse:
    """Stores a candidate response to an interview question."""

    question_id: str
    response: str
    response_type: str = "text"
    question: Optional[str] = None
    category: Optional[str] = None
    follow_up_eligible: bool = False
    follow_up_reason: Optional[str] = None
    recorded_at: datetime = field(default_factory=_utc_now)


@dataclass
class InterviewState:
    """State for one HR interview session."""

    session_id: str
    candidate_id: Optional[str] = None
    role: Optional[str] = None
    experience_level: Optional[str] = None

    phase: str = "introduction"
    current_question_id: Optional[str] = None
    current_category: Optional[str] = None
    question_index: int = 0
    responses: List[InterviewResponse] = field(default_factory=list)
    completed: bool = False

    consent_given: bool = False
    consent_recorded_at: Optional[datetime] = None
    retention_days: int = 90

    def __post_init__(self) -> None:
        if self.retention_days < 1:
            raise ValueError("retention_days must be at least 1")

    def grant_consent(
        self,
        consent_time: Optional[datetime] = None,
    ) -> None:
        """Record explicit candidate consent before response capture."""
        timestamp = consent_time or _utc_now()
        if timestamp.tzinfo is None:
            raise ValueError("consent_time must be timezone-aware")

        self.consent_given = True
        self.consent_recorded_at = timestamp.astimezone(timezone.utc)

    def withdraw_consent(self) -> None:
        """Withdraw consent and remove captured responses from this state."""
        self.consent_given = False
        self.responses.clear()

    def purge_expired_responses(
        self,
        now: Optional[datetime] = None,
    ) -> int:
        """Remove responses older than the configured retention period."""
        current_time = now or _utc_now()
        if current_time.tzinfo is None:
            raise ValueError("now must be timezone-aware")

        cutoff = current_time.astimezone(timezone.utc) - timedelta(
            days=self.retention_days
        )
        original_count = len(self.responses)
        self.responses = [
            response
            for response in self.responses
            if response.recorded_at >= cutoff
        ]
        return original_count - len(self.responses)

    def set_question(
        self,
        question_id: str,
        index: int,
        category: Optional[HRInterviewCategory | str] = None,
    ) -> None:
        self.current_question_id = question_id
        self.question_index = index
        if isinstance(category, HRInterviewCategory):
            self.current_category = category.value
        else:
            self.current_category = category

    def record_response(
        self,
        question_id: str,
        response: str,
        response_type: str = "text",
        question: Optional[str] = None,
        follow_up_eligible: bool = False,
        follow_up_reason: Optional[str] = None,
        category: Optional[HRInterviewCategory | str] = None,
    ) -> InterviewResponse:
        """Capture a response only after explicit consent."""
        if not self.consent_given:
            raise PermissionError(
                "Candidate consent is required before recording responses."
            )

        if isinstance(category, HRInterviewCategory):
            category_value = category.value
        else:
            category_value = category or self.current_category

        captured_response = InterviewResponse(
            question_id=question_id,
            response=response.strip(),
            response_type=response_type,
            question=question,
            category=category_value,
            follow_up_eligible=follow_up_eligible,
            follow_up_reason=follow_up_reason,
        )
        self.responses.append(captured_response)
        return captured_response

    def get_response(self, question_id: str) -> Optional[InterviewResponse]:
        for response in self.responses:
            if response.question_id == question_id:
                return response
        return None

    def can_follow_up(self, question_id: str) -> bool:
        response = self.get_response(question_id)
        return response is not None and response.follow_up_eligible

    def change_phase(self, phase: str) -> None:
        self.phase = phase

    def set_category(self, category: HRInterviewCategory | str) -> None:
        if isinstance(category, HRInterviewCategory):
            self.current_category = category.value
        else:
            self.current_category = category

    def complete(self) -> None:
        self.completed = True
        self.phase = "closing"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize state and consent metadata."""
        return {
            "session_id": self.session_id,
            "candidate_id": self.candidate_id,
            "role": self.role,
            "experience_level": self.experience_level,
            "phase": self.phase,
            "current_question_id": self.current_question_id,
            "current_category": self.current_category,
            "question_index": self.question_index,
            "completed": self.completed,
            "consent_given": self.consent_given,
            "consent_recorded_at": (
                self.consent_recorded_at.isoformat()
                if self.consent_recorded_at else None
            ),
            "retention_days": self.retention_days,
            "responses": [
                {
                    "question_id": response.question_id,
                    "response": response.response,
                    "response_type": response.response_type,
                    "question": response.question,
                    "category": response.category,
                    "follow_up_eligible": response.follow_up_eligible,
                    "follow_up_reason": response.follow_up_reason,
                    "recorded_at": response.recorded_at.isoformat(),
                }
                for response in self.responses
            ],
        }
