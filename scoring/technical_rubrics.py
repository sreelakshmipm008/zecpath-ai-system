"""Rubric guidance for technical interview answer evaluation."""

DIMENSION_DESCRIPTIONS = {
    "accuracy": "Technical correctness and alignment with expected points.",
    "explanation_depth": "Completeness, clarity, and depth of explanation.",
    "logical_reasoning": "Coherent reasoning and justified steps.",
    "real_world_application": "Practical relevance and suitable examples.",
}

QUESTION_TYPE_RUBRICS = {
    "conceptual": {
        "accuracy": "Correct definitions, facts, and distinctions.",
        "explanation_depth": "Explains how and why the concept works.",
        "logical_reasoning": "Connects related concepts logically.",
        "real_world_application": "Provides a relevant use case or example.",
    },
    "practical": {
        "accuracy": "Correct implementation approach and technical details.",
        "explanation_depth": "Covers important steps and required components.",
        "logical_reasoning": "Presents steps in a valid, logical sequence.",
        "real_world_application": "Addresses testing, errors, and practical use.",
    },
    "scenario": {
        "accuracy": "Identifies technically valid causes and solutions.",
        "explanation_depth": "Explains the situation and proposed solution.",
        "logical_reasoning": "Shows diagnosis, prioritization, and justification.",
        "real_world_application": "Considers constraints, risks, and validation.",
    },
}

DIFFICULTY_EXPECTATIONS = {
    "basic": "Demonstrates foundational knowledge and straightforward application.",
    "intermediate": "Demonstrates connected concepts and independent problem-solving.",
    "advanced": "Demonstrates deeper technical judgment, trade-offs, and complex application.",
}


def get_rubric_guidance(question_type, difficulty):
    """Return question-type and difficulty-specific assessor guidance."""

    if question_type not in QUESTION_TYPE_RUBRICS:
        raise ValueError(f"Unsupported question type: {question_type}")

    if difficulty not in DIFFICULTY_EXPECTATIONS:
        raise ValueError(f"Unsupported difficulty: {difficulty}")

    return {
        "dimension_descriptions": DIMENSION_DESCRIPTIONS.copy(),
        "question_type_criteria": QUESTION_TYPE_RUBRICS[question_type].copy(),
        "difficulty_expectation": DIFFICULTY_EXPECTATIONS[difficulty],
        "score_scale": "0-100",
        "score_bands": {
            "0-39": "Shallow or mostly incorrect; major gaps in understanding.",
            "40-69": "Partially correct; limited explanation or weak reasoning.",
            "70-84": "Mostly accurate; clear explanation and reasonable application.",
            "85-100": "Thorough and accurate; strong reasoning, depth, and practical application.",
        },
        "normalization_method": (
            "All dimensions use a common 0-100 scale. "
            "Difficulty changes the expected depth and complexity, "
            "not the numerical scale."
        ),
    }
