import pytest

from scoring.technical_skill_scoring_engine import (
    TechnicalSkillScoringEngine,
)


@pytest.fixture
def engine():
    return TechnicalSkillScoringEngine()


@pytest.fixture
def question():
    return {
        "id": "PY-001",
        "type": "conceptual",
        "difficulty": "basic",
        "domain": "Python",
        "question": "Explain Python dictionaries.",
        "expected_points": [
            "Key-value pairs",
            "Unique keys",
            "Mutable structure",
            "Fast key-based lookup",
        ],
    }


def test_weighted_technical_score(engine, question):
    result = engine.score_answer(
        question,
        "A dictionary stores key-value pairs.",
        {
            "accuracy": 80,
            "explanation_depth": 70,
            "logical_reasoning": 60,
            "real_world_application": 90,
        },
    )

    assert result["technical_score"] == 74.5
    assert result["performance_level"] == "Proficient"
    assert result["question_id"] == "PY-001"


def test_score_contains_explainable_breakdown(engine, question):
    result = engine.score_answer(
        question,
        "A dictionary stores key-value pairs.",
        {
            "accuracy": 80,
            "explanation_depth": 70,
            "logical_reasoning": 60,
            "real_world_application": 90,
        },
        assessor_notes="Good example, but explanation needs more depth.",
    )

    assert set(result["dimension_scores"]) == engine.REQUIRED_DIMENSIONS
    assert set(result["weighted_contributions"]) == engine.REQUIRED_DIMENSIONS
    assert result["assessor_notes"]


def test_skill_wise_breakdown(engine):
    results = [
        {"skill_domain": "Python", "technical_score": 80},
        {"skill_domain": "Python", "technical_score": 60},
        {"skill_domain": "SQL", "technical_score": 90},
    ]

    report = engine.build_skill_breakdown(results)

    assert report["overall_technical_score"] == 76.67
    assert report["skill_breakdown"]["Python"]["average_score"] == 70
    assert report["skill_breakdown"]["Python"]["question_count"] == 2
    assert report["skill_breakdown"]["SQL"]["average_score"] == 90


def test_empty_answer_is_rejected(engine, question):
    with pytest.raises(ValueError, match="non-empty"):
        engine.score_answer(question, "  ", {
            "accuracy": 80,
            "explanation_depth": 70,
            "logical_reasoning": 60,
            "real_world_application": 90,
        })


@pytest.mark.parametrize("score", [-1, 101, "80", None, True])
def test_invalid_dimension_score_is_rejected(engine, question, score):
    scores = {
        "accuracy": 80,
        "explanation_depth": 70,
        "logical_reasoning": 60,
        "real_world_application": 90,
    }
    scores["accuracy"] = score

    with pytest.raises(ValueError):
        engine.score_answer(question, "Sample answer", scores)


def test_missing_dimension_is_rejected(engine, question):
    with pytest.raises(ValueError, match="all four"):
        engine.score_answer(
            question,
            "Sample answer",
            {"accuracy": 80},
        )


def test_invalid_weights_are_rejected():
    with pytest.raises(ValueError, match="sum to 1.0"):
        TechnicalSkillScoringEngine({
            "accuracy": 0.5,
            "explanation_depth": 0.2,
            "logical_reasoning": 0.2,
            "real_world_application": 0.2,
        })


def test_empty_skill_results_are_rejected(engine):
    with pytest.raises(ValueError, match="non-empty"):
        engine.build_skill_breakdown([])

from scoring.technical_rubrics import get_rubric_guidance


@pytest.mark.parametrize(
    "question_type",
    ["conceptual", "practical", "scenario"],
)
@pytest.mark.parametrize(
    "difficulty",
    ["basic", "intermediate", "advanced"],
)
def test_all_rubric_combinations(question_type, difficulty):
    result = get_rubric_guidance(question_type, difficulty)

    assert len(result["question_type_criteria"]) == 4
    assert result["score_scale"] == "0-100"
    assert result["difficulty_expectation"]


@pytest.mark.parametrize(
    "question_type,difficulty",
    [
        ("unknown", "basic"),
        ("conceptual", "expert"),
    ],
)
def test_invalid_rubric_inputs_are_rejected(question_type, difficulty):
    with pytest.raises(ValueError):
        get_rubric_guidance(question_type, difficulty)


def test_scoring_result_contains_question_specific_rubric(engine, question):
    result = engine.score_answer(
        question,
        "A dictionary stores key-value pairs.",
        {
            "accuracy": 80,
            "explanation_depth": 70,
            "logical_reasoning": 60,
            "real_world_application": 90,
        },
    )

    assert result["rubric_guidance"]["question_type_criteria"]
    assert result["rubric_guidance"]["difficulty_expectation"]

def test_rubric_contains_all_four_score_bands():
    from scoring.technical_rubrics import get_rubric_guidance

    result = get_rubric_guidance("conceptual", "basic")
    bands = result["score_bands"]

    assert len(bands) == 4
    assert "0-39" in bands
    assert "40-69" in bands
    assert "70-84" in bands
    assert "85-100" in bands
