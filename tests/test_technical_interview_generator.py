import pytest

from question_generator.technical_interview_generator import (
    TechnicalInterviewGenerator,
)


@pytest.fixture
def generator():
    return TechnicalInterviewGenerator()


@pytest.mark.parametrize(
    "role",
    [
        "Python Developer",
        "Data Analyst",
        "AWS Cloud Engineer",
        "Cyber Security Analyst",
    ],
)
@pytest.mark.parametrize(
    "years, expected_band",
    [
        (1, "0-2"),
        (4, "3-5"),
        (6, "5+"),
    ],
)
def test_generates_questions_for_all_roles_and_experience(
    generator, role, years, expected_band
):
    result = generator.generate_interview(role, years)

    assert result["role"] == role
    assert result["experience_band"] == expected_band
    assert result["question_count"] == 3
    assert {q["type"] for q in result["questions"]} == {
        "conceptual",
        "practical",
        "scenario",
    }


def test_role_name_is_case_and_separator_insensitive(generator):
    result = generator.generate_interview("python-developer", 1)
    assert result["role"] == "Python Developer"


def test_question_count_limit(generator):
    result = generator.generate_interview(
        "Python Developer", 1, question_count=2
    )
    assert result["question_count"] == 2


def test_skill_domain_filter(generator):
    result = generator.generate_interview(
        "Python Developer", 1, skill_domains=["Python"]
    )
    assert result["questions"]
    assert all(q["domain"].lower() == "python" for q in result["questions"])


def test_unknown_role_raises_error(generator):
    with pytest.raises(ValueError, match="Unknown role"):
        generator.generate_interview("Graphic Designer", 1)


@pytest.mark.parametrize("years", [-1, "two", True])
def test_invalid_experience_raises_error(generator, years):
    with pytest.raises(ValueError):
        generator.generate_interview("Python Developer", years)


@pytest.mark.parametrize("count", [0, -1, 1.5, True])
def test_invalid_question_count_raises_error(generator, count):
    with pytest.raises(ValueError, match="question_count"):
        generator.generate_interview(
            "Python Developer", 1, question_count=count
        )


def test_unavailable_skill_domain_raises_error(generator):
    with pytest.raises(ValueError, match="No questions found"):
        generator.generate_interview(
            "Python Developer", 1, skill_domains=["Blockchain"]
        )


def test_exactly_five_years_belongs_to_intermediate_band(generator):
    result = generator.generate_interview("Python Developer", 5)
    assert result["experience_band"] == "3-5"
