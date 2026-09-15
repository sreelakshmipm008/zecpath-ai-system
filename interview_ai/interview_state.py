"""
Day 33 - HR Interview State Structure.

Maintains the state of an AI HR interview, including:
- current question
- current HR interview category
- response capture
- follow-up eligibility
- interview phase
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from interview_ai.hr_interview_categories import HRInterviewCategory


@dataclass
class InterviewResponse:
    """Stores a candidate response to an interview question."""

    question_id: str
    response: str
    response_type: str = "text"
    category: Optional[str] = None
    follow_up_eligible: bool = False
    follow_up_reason: Optional[str] = None


@dataclass
class InterviewState:
    """Persistent state for one HR interview session."""

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

    def set_question(
        self,
        question_id: str,
        index: int,
        category: Optional[HRInterviewCategory | str] = None,
    ) -> None:
        """Set the current question and optional HR category."""

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
        follow_up_eligible: bool = False,
        follow_up_reason: Optional[str] = None,
        category: Optional[HRInterviewCategory | str] = None,
    ) -> InterviewResponse:
        """Capture a candidate response."""

        if isinstance(category, HRInterviewCategory):
            category_value = category.value
        else:
            category_value = category or self.current_category

        captured_response = InterviewResponse(
            question_id=question_id,
            response=response.strip(),
            response_type=response_type,
            category=category_value,
            follow_up_eligible=follow_up_eligible,
            follow_up_reason=follow_up_reason,
        )

        self.responses.append(captured_response)

        return captured_response

    def get_response(
        self,
        question_id: str,
    ) -> Optional[InterviewResponse]:
        """Retrieve a response by question ID."""

        for response in self.responses:
            if response.question_id == question_id:
                return response

        return None

    def can_follow_up(self, question_id: str) -> bool:
        """Check whether follow-up is allowed for a question."""

        response = self.get_response(question_id)

        if response is None:
            return False

        return response.follow_up_eligible

    def change_phase(self, phase: str) -> None:
        """Move the interview to another phase."""

        self.phase = phase

    def set_category(
        self,
        category: HRInterviewCategory | str,
    ) -> None:
        """Set the current HR interview category."""

        if isinstance(category, HRInterviewCategory):
            self.current_category = category.value
        else:
            self.current_category = category

    def complete(self) -> None:
        """Mark the interview as completed."""

        self.completed = True
        self.phase = "closing"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize interview state for persistence."""

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
            "responses": [
                {
                    "question_id": response.question_id,
                    "response": response.response,
                    "response_type": response.response_type,
                    "category": response.category,
                    "follow_up_eligible": response.follow_up_eligible,
                    "follow_up_reason": response.follow_up_reason,
                }
                for response in self.responses
            ],
        }