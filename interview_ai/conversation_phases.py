"""
Day 33 - HR Interview Conversation Phases.

Defines the high-level phases of the AI HR interview:
1. Introduction
2. Core HR questions
3. Role-based evaluation
4. Closing
"""

from __future__ import annotations

from enum import Enum
from typing import Dict


class ConversationPhase(str, Enum):
    INTRODUCTION = "introduction"
    CORE_HR = "core_hr"
    ROLE_EVALUATION = "role_evaluation"
    CLOSING = "closing"


class ConversationPhaseManager:
    """Controls valid transitions between interview phases."""

    TRANSITIONS: Dict[ConversationPhase, ConversationPhase] = {
        ConversationPhase.INTRODUCTION:
            ConversationPhase.CORE_HR,
        ConversationPhase.CORE_HR:
            ConversationPhase.ROLE_EVALUATION,
        ConversationPhase.ROLE_EVALUATION:
            ConversationPhase.CLOSING,
        ConversationPhase.CLOSING:
            ConversationPhase.CLOSING,
    }

    def __init__(
        self,
        initial_phase: ConversationPhase = ConversationPhase.INTRODUCTION,
    ) -> None:
        self.current_phase = initial_phase

    def next_phase(self) -> ConversationPhase:
        """Move to the next conversation phase."""
        self.current_phase = self.TRANSITIONS[self.current_phase]
        return self.current_phase

    def can_advance(self) -> bool:
        """Return whether another phase exists."""
        return self.current_phase != ConversationPhase.CLOSING

    def is_complete(self) -> bool:
        """Return whether the interview has reached closing."""
        return self.current_phase == ConversationPhase.CLOSING

    def phase_description(self) -> str:
        """Return a human-readable description of the current phase."""
        descriptions = {
            ConversationPhase.INTRODUCTION:
                "Candidate introduction and initial background.",
            ConversationPhase.CORE_HR:
                "Core HR questions covering education, experience, skills, availability and related areas.",
            ConversationPhase.ROLE_EVALUATION:
                "Role-based evaluation using questions selected for the candidate's role and experience level.",
            ConversationPhase.CLOSING:
                "Interview closing and completion.",
        }

        return descriptions[self.current_phase]