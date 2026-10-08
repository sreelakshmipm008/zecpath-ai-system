import pytest

from interview_ai.hr_interview_categories import HRInterviewCategory
from interview_ai.interview_state import InterviewState
from scoring.hr_interview_scoring_engine import HRInterviewScoringEngine


def _response(
    question_id,
    question,
    response,
    category,
):
    return {
        "question_id": question_id,
        "question": question,
        "response": response,
        "category": category,
    }


def test_score_response_with_adequate_answer():
    engine = HRInterviewScoringEngine()

    result = engine.score_response(
        response=(
            "I am a data analyst with experience in Python, SQL, "
            "Excel and Power BI. I enjoy working with data."
        ),
        category=HRInterviewCategory.SELF_INTRODUCTION,
    )

    assert result["category"] == "self_introduction"
    assert result["word_count"] > 10
    assert result["score"] == 100.0
    assert "combined_score" in result
    assert "score_breakdown" in result


def test_score_empty_response():
    engine = HRInterviewScoringEngine()

    result = engine.score_response(
        response="",
        category="career_goals",
    )

    assert result["word_count"] == 0
    assert result["score"] == 0.0
    assert result["combined_score"] == 0.0
    assert result["answer_relevance_score"] == 0.0
    assert result["communication_score"] == 0.0
    assert result["behavioral_confidence_score"] == 0.0
    assert result["consistency_score"] == 0.0


def test_score_category():
    engine = HRInterviewScoringEngine()

    responses = [
        _response(
            "q1",
            "Tell me about yourself.",
            "I am a data analyst with experience in Python and SQL.",
            "self_introduction",
        ),
        _response(
            "q2",
            "What are your strengths?",
            "I am organized, analytical, and enjoy solving business problems.",
            "strengths_weaknesses",
        ),
    ]

    result = engine.score_category(
        responses=responses,
        category="self_introduction",
    )

    assert result["status"] == "evaluated"
    assert result["response_count"] == 1
    assert result["score"] == 100.0
    assert "dimension_scores" in result


def test_category_without_response():
    engine = HRInterviewScoringEngine()

    result = engine.score_category(
        responses=[],
        category="career_goals",
    )

    assert result["status"] == "not_evaluated"
    assert result["response_count"] == 0
    assert result["score"] == 0.0


def test_relevance_scores():
    engine = HRInterviewScoringEngine()

    on_topic = engine.score_response(
        "I have worked with Python and SQL for data analysis.",
        "career_journey",
        question="Tell me about your experience with data analysis.",
    )
    off_topic = engine.score_response(
        "My favorite food is pizza and I like watching movies.",
        "career_journey",
        question="Tell me about your experience with data analysis.",
    )
    vague = engine.score_response(
        "I don't know.",
        "career_journey",
        question="Tell me about your experience with data analysis.",
    )

    assert on_topic["answer_relevance_score"] == 100.0
    assert off_topic["answer_relevance_score"] == 20.0
    assert vague["answer_relevance_score"] == 50.0


def test_weightage_is_25_percent_each():
    engine = HRInterviewScoringEngine()

    assert engine.hr_scoring_weights == {
        "answer_relevance": 0.25,
        "communication_score": 0.25,
        "confidence_score": 0.25,
        "consistency": 0.25,
    }


def test_explainable_contributions_sum_to_overall_score():
    engine = HRInterviewScoringEngine()

    responses = [
        _response(
            "q1",
            "Tell me about yourself.",
            "I am a data analyst with experience in Python, SQL and Excel.",
            "self_introduction",
        ),
        _response(
            "q2",
            "What are your career goals?",
            "I want to grow as a data analyst and contribute to meaningful business decisions.",
            "career_goals",
        ),
    ]

    result = engine.score_interview(responses)

    assert result["overall_score"] == round(
        sum(result["score_contributions"].values()),
        2,
    )
    assert result["scoring_weights"] == {
        "answer_relevance": 0.25,
        "communication_score": 0.25,
        "confidence_score": 0.25,
        "consistency": 0.25,
    }


def test_cross_response_consistency_detects_conflicting_experience():
    engine = HRInterviewScoringEngine()

    responses = [
        _response(
            "q1",
            "How much experience do you have?",
            "I have 2 years of experience in data analysis.",
            "career_journey",
        ),
        _response(
            "q2",
            "Tell me more about your background.",
            "I have 5 years of professional experience.",
            "career_journey",
        ),
    ]

    result = engine.score_interview(responses)

    consistency = result["consistency_analysis"]

    assert consistency["conflict_count"] == 1
    assert consistency["cross_response_score"] == 75.0
    assert consistency["score"] < 100.0


def test_interview_length_normalization_uses_category_averages():
    engine = HRInterviewScoringEngine()

    one_response = [
        _response(
            "q1",
            "Tell me about yourself.",
            "I am a data analyst with experience in Python and SQL.",
            "self_introduction",
        )
    ]

    many_responses_same_category = [
        _response(
            "q1",
            "Tell me about yourself.",
            "I am a data analyst with experience in Python and SQL.",
            "self_introduction",
        ),
        _response(
            "q2",
            "Tell me about your background.",
            "I have worked with Excel and Power BI for data analysis.",
            "self_introduction",
        ),
        _response(
            "q3",
            "Why did you choose analytics?",
            "I enjoy using data to solve business problems.",
            "self_introduction",
        ),
    ]

    one_result = engine.score_interview(one_response)
    many_result = engine.score_interview(many_responses_same_category)

    assert (
        one_result["normalization"]["method"]
        == "equal-weight category averages"
    )
    assert (
        many_result["normalization"]["method"]
        == "equal-weight category averages"
    )
    assert one_result["evaluated_category_count"] == 1
    assert many_result["evaluated_category_count"] == 1


def test_score_interview_state():
    engine = HRInterviewScoringEngine()

    state = InterviewState(
        session_id="session-1",
        candidate_id="candidate-1",
        role="Data Analyst",
        experience_level="fresher",
    )

    state.record_response(
        question_id="q1",
        question="Tell me about yourself.",
        response=(
            "I am a data analyst interested in Python, SQL, "
            "and business analytics."
        ),
        category="self_introduction",
    )

    result = engine.score_interview_state(state)

    assert result["session_id"] == "session-1"
    assert result["candidate_id"] == "candidate-1"
    assert result["role"] == "Data Analyst"
    assert result["total_response_count"] == 1
    assert "dimension_scores" in result


def test_invalid_category():
    engine = HRInterviewScoringEngine()

    with pytest.raises(ValueError):
        engine.score_response(
            response="This is a valid answer.",
            category="invalid_category",
        )
