from enum import Enum


class TechnicalInterviewPhase(str, Enum):
    INTRODUCTION = "introduction"
    EXPERIENCE = "experience_based"
    CONCEPTUAL = "conceptual"
    SCENARIO = "scenario_based"
    CLOSING = "closing"
    COMPLETED = "completed"


class TechnicalInterviewFlow:
    """Manage the stages and valid transitions of a technical interview."""

    PHASE_ORDER = [
        TechnicalInterviewPhase.INTRODUCTION,
        TechnicalInterviewPhase.EXPERIENCE,
        TechnicalInterviewPhase.CONCEPTUAL,
        TechnicalInterviewPhase.SCENARIO,
        TechnicalInterviewPhase.CLOSING,
        TechnicalInterviewPhase.COMPLETED,
    ]

    def __init__(self, session_id=None):
        self.session_id = session_id
        self.current_phase = TechnicalInterviewPhase.INTRODUCTION
        self.history = [self.current_phase.value]

    @property
    def is_complete(self):
        return self.current_phase == TechnicalInterviewPhase.COMPLETED

    def transition_to(self, phase):
        """Move to the next valid phase; reject skipped or backward transitions."""
        try:
            target = (
                phase
                if isinstance(phase, TechnicalInterviewPhase)
                else TechnicalInterviewPhase(phase)
            )
        except ValueError as exc:
            raise ValueError(f"Unknown interview phase: {phase}") from exc

        current_index = self.PHASE_ORDER.index(self.current_phase)
        target_index = self.PHASE_ORDER.index(target)

        if target_index != current_index + 1:
            raise ValueError(
                f"Invalid transition: {self.current_phase.value} -> {target.value}. "
                "Only the next interview phase is allowed."
            )

        self.current_phase = target
        self.history.append(target.value)
        return self.current_phase

    def advance(self):
        """Advance the interview by exactly one phase."""
        current_index = self.PHASE_ORDER.index(self.current_phase)

        if current_index == len(self.PHASE_ORDER) - 1:
            raise ValueError("The interview is already completed.")

        return self.transition_to(self.PHASE_ORDER[current_index + 1])

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "current_phase": self.current_phase.value,
            "history": list(self.history),
            "is_complete": self.is_complete,
        }
