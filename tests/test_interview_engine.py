
from interview_ai.conversation_phases import (
    ConversationPhase,
    ConversationPhaseManager,
)
from interview_ai.hr_interview_categories import HRInterviewCategory
from interview_ai.interview_state import InterviewState


def test_initial_interview_state():
    state = InterviewState(session_id="SESSION001")

    assert state.phase == "introduction"
    assert state.current_question_id is None
    assert state.question_index == 0
    assert state.responses == []
    assert state.completed is False


def test_set_question():
    state = InterviewState(session_id="SESSION001")

    state.set_question("Q001", 0)

    assert state.current_question_id == "Q001"
    assert state.question_index == 0


def test_record_response():
    state = InterviewState(session_id="SESSION001")

    response = state.record_response(
        question_id="Q001",
        response="I am a Python developer.",
        response_type="text",
        follow_up_eligible=True,
        follow_up_reason="Candidate mentioned relevant experience.",
    )

    assert response.question_id == "Q001"
    assert response.response == "I am a Python developer."
    assert response.follow_up_eligible is True
    assert len(state.responses) == 1


def test_follow_up_eligibility():
    state = InterviewState(session_id="SESSION001")

    state.record_response(
        question_id="Q001",
        response="I have experience with Python.",
        follow_up_eligible=True,
    )

    assert state.can_follow_up("Q001") is True
    assert state.can_follow_up("Q999") is False


def test_non_follow_up_response():
    state = InterviewState(session_id="SESSION001")

    state.record_response(
        question_id="Q002",
        response="Yes.",
        follow_up_eligible=False,
    )

    assert state.can_follow_up("Q002") is False


def test_state_serialization():
    state = InterviewState(
        session_id="SESSION001",
        candidate_id="C001",
        role="Python Developer",
        experience_level="experienced",
    )

    state.set_question("Q001", 0)
    state.record_response(
        question_id="Q001",
        response="I have five years of experience.",
        follow_up_eligible=True,
    )

    data = state.to_dict()

    assert data["session_id"] == "SESSION001"
    assert data["candidate_id"] == "C001"
    assert data["role"] == "Python Developer"
    assert data["experience_level"] == "experienced"
    assert data["current_question_id"] == "Q001"
    assert len(data["responses"]) == 1


def test_initial_conversation_phase():
    manager = ConversationPhaseManager()

    assert manager.current_phase == ConversationPhase.INTRODUCTION
    assert manager.can_advance() is True
    assert manager.is_complete() is False


def test_conversation_phase_progression():
    manager = ConversationPhaseManager()

    assert manager.next_phase() == ConversationPhase.CORE_HR
    assert manager.next_phase() == ConversationPhase.ROLE_EVALUATION
    assert manager.next_phase() == ConversationPhase.CLOSING


def test_closing_is_terminal():
    manager = ConversationPhaseManager()

    manager.next_phase()
    manager.next_phase()
    manager.next_phase()

    assert manager.current_phase == ConversationPhase.CLOSING
    assert manager.can_advance() is False
    assert manager.is_complete() is True

    assert manager.next_phase() == ConversationPhase.CLOSING


def test_phase_descriptions():
    manager = ConversationPhaseManager()

    assert "introduction" in manager.phase_description().lower()

    manager.next_phase()

    assert "core hr" in manager.phase_description().lower()

    manager.next_phase()

    assert "role-based" in manager.phase_description().lower()


def test_question_tracks_hr_category():
    state = InterviewState(session_id="SESSION001")

    state.set_question(
        question_id="Q001",
        index=0,
        category=HRInterviewCategory.SELF_INTRODUCTION,
    )

    assert state.current_question_id == "Q001"
    assert state.current_category == "self_introduction"


def test_response_inherits_current_hr_category():
    state = InterviewState(session_id="SESSION001")

    state.set_category(HRInterviewCategory.CAREER_JOURNEY)

    response = state.record_response(
        question_id="Q002",
        response="I started my career as an intern.",
    )

    assert response.category == "career_journey"


def test_response_can_set_explicit_category():
    state = InterviewState(session_id="SESSION001")

    response = state.record_response(
        question_id="Q003",
        response="I work well with teams.",
        category=HRInterviewCategory.TEAMWORK_CULTURE_FIT,
    )

    assert response.category == "teamwork_culture_fit"


def test_category_persisted_in_state():
    state = InterviewState(
        session_id="SESSION001",
        role="Python Developer",
        experience_level="experienced",
    )

    state.set_question(
        question_id="Q001",
        index=0,
        category=HRInterviewCategory.SELF_INTRODUCTION,
    )

    state.record_response(
        question_id="Q001",
        response="I am a Python developer.",
        follow_up_eligible=True,
    )

    data = state.to_dict()

    assert data["current_category"] == "self_introduction"
    assert data["responses"][0]["category"] == "self_introduction"