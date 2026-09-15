from interview_ai.follow_up_engine import FollowUpEngine
from interview_ai.interview_state import InterviewState


def create_state() -> InterviewState:
    """Create a basic interview state for follow-up tests."""
    return InterviewState(session_id="test-session")


def test_incomplete_response_triggers_clarification():
    engine = FollowUpEngine()

    result = engine.determine_follow_up_trigger("Python")

    assert result["follow_up_required"] is True
    assert result["trigger"] == "clarification"


def test_vague_response_triggers_example_based_follow_up():
    engine = FollowUpEngine()
    state = create_state()

    result = engine.build_follow_up_decision(
        response="Yes",
        state=state,
    )

    assert result["follow_up_required"] is True
    assert result["trigger"] == "example_based"
    assert result["follow_up_type"] == "example_based"


def test_sufficient_response_triggers_deepening():
    engine = FollowUpEngine()

    result = engine.determine_follow_up_trigger(
        "I used Python for data analysis."
    )

    assert result["follow_up_required"] is True
    assert result["trigger"] == "deepening"


def test_simple_response_gets_deeper_probe():
    engine = FollowUpEngine()

    result = engine.determine_difficulty_level(
        "I used Python for data analysis."
    )

    assert result == "simple"


def test_confident_response_gets_scenario_based_follow_up():
    engine = FollowUpEngine()

    result = engine.determine_difficulty_level(
        "I developed and implemented a Python system "
        "that automated our reporting process successfully."
    )

    assert result == "confident"


def test_repetitive_question_is_detected():
    engine = FollowUpEngine()

    result = engine.is_repetitive_question(
        "q_005",
        ["q_001", "q_003", "q_005"],
    )

    assert result is True


def test_new_question_is_not_repetitive():
    engine = FollowUpEngine()

    result = engine.is_repetitive_question(
        "q_007",
        ["q_001", "q_003", "q_005"],
    )

    assert result is False


def test_conversation_context_uses_interview_state():
    engine = FollowUpEngine()

    state = create_state()
    state.set_question("q_001", 1, "introduction")
    state.record_response(
        question_id="q_001",
        response="I am a data analyst.",
    )

    context = engine.get_conversation_context(state)

    assert context["current_question_id"] == "q_001"
    assert context["question_index"] == 1
    assert context["response_count"] == 1
    assert context["previous_question_ids"] == ["q_001"]


def test_repetitive_question_prevents_follow_up():
    engine = FollowUpEngine()

    state = create_state()
    state.record_response(
        question_id="q_001",
        response="I am a data analyst.",
    )

    result = engine.build_follow_up_decision(
        response="I used Python for data analysis.",
        state=state,
        next_question_id="q_001",
    )

    assert result["is_repetitive"] is True
    assert result["follow_up_required"] is False


def test_new_question_allows_follow_up():
    engine = FollowUpEngine()

    state = create_state()
    state.record_response(
        question_id="q_001",
        response="I am a data analyst.",
    )

    result = engine.build_follow_up_decision(
        response="I used Python for data analysis.",
        state=state,
        next_question_id="q_002",
    )

    assert result["is_repetitive"] is False
    assert result["follow_up_required"] is True


def test_follow_up_instruction_for_confident_response():
    engine = FollowUpEngine()

    state = create_state()

    result = engine.generate_follow_up_instruction(
        response=(
            "I developed and implemented a Python system "
            "that automated our reporting process successfully."
        ),
        state=state,
        next_question_id="q_002",
    )

    assert result["follow_up_type"] == "scenario_based"
    assert "scenario-based" in result["instruction"].lower()        