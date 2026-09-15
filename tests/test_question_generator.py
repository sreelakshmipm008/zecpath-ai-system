import pytest

from question_generator.role_based_question_generator import (
    RoleBasedQuestionGenerator,
)


@pytest.fixture
def generator():
    return RoleBasedQuestionGenerator()


def test_question_bank_loads(generator):
    assert len(generator.questions) == 106


def test_technical_role_classification(generator):
    assert generator.classify_role("Python Developer") == "technical"
    assert generator.classify_role("Data Analyst") == "technical"


def test_non_technical_role_classification(generator):
    assert (
        generator.classify_role("Accountant")
        == "non-technical"
    )
    assert (
        generator.classify_role("HR Executive")
        == "non-technical"
    )


def test_fresher_generation(generator):
    questions = generator.generate_questions(
        role="Data Analyst",
        experience_level="fresher",
    )

    assert questions
    assert all(
        question["role"] == "Data Analyst"
        for question in questions
    )
    assert all(
        question["experience_level"] == "fresher"
        for question in questions
    )


def test_experienced_generation(generator):
    questions = generator.generate_questions(
        role="Data Analyst",
        experience_level="experienced",
    )

    assert questions

    categories = [question["category"] for question in questions]

    assert "Experience" in categories
    assert "Skills" in categories


def test_malayalam_generation(generator):
    questions = generator.generate_questions(
        role="Accountant",
        experience_level="fresher",
        language="ml",
        limit=3,
    )

    assert len(questions) == 3
    assert all(question["question"] for question in questions)


def test_limit(generator):
    questions = generator.generate_questions(
        role="Python Developer",
        experience_level="experienced",
        limit=5,
    )

    assert len(questions) == 5


def test_invalid_experience_level(generator):
    with pytest.raises(ValueError):
        generator.generate_questions(
            role="Accountant",
            experience_level="intern",
        )


def test_invalid_language(generator):
    with pytest.raises(ValueError):
        generator.generate_questions(
            role="Accountant",
            experience_level="fresher",
            language="fr",
        )


def test_invalid_role(generator):
    with pytest.raises(ValueError):
        generator.generate_questions(
            role="Unknown Role",
            experience_level="fresher",
        )


def test_screening_set_structure(generator):
    result = generator.generate_screening_set(
        role="Python Developer",
        experience_level="experienced",
        limit=5,
    )

    assert result["role"] == "Python Developer"
    assert result["role_type"] == "technical"
    assert result["experience_level"] == "experienced"
    assert result["language"] == "en"
    assert result["question_count"] == 5
    assert len(result["questions"]) == 5


def test_fresher_and_experienced_receive_different_question_sets(generator):
    fresher = generator.generate_questions(
        role="Python Developer",
        experience_level="fresher",
        limit=8,
    )

    experienced = generator.generate_questions(
        role="Python Developer",
        experience_level="experienced",
        limit=8,
    )

    fresher_ids = {
        question["question_id"]
        for question in fresher
    }

    experienced_ids = {
        question["question_id"]
        for question in experienced
    }

    assert fresher_ids != experienced_ids


def test_technical_and_non_technical_profiles_are_classified(generator):
    technical = generator.generate_questions(
        role="Python Developer",
        experience_level="experienced",
        limit=8,
    )

    non_technical = generator.generate_questions(
        role="Accountant",
        experience_level="experienced",
        limit=8,
    )

    assert all(
        question["role_type"] == "technical"
        for question in technical
    )

    assert all(
        question["role_type"] == "non-technical"
        for question in non_technical
    )


def test_profile_metadata_is_attached_to_every_question(generator):
    questions = generator.generate_questions(
        role="Data Analyst",
        experience_level="fresher",
        limit=8,
    )

    assert questions

    for question in questions:
        assert question["role_type"] == "technical"
        assert question["experience_level"] == "fresher"
        assert question["question_id"]
        assert question["category"]


def test_fresher_prioritizes_education(generator):
    questions = generator.generate_questions(
        role="Data Analyst",
        experience_level="fresher",
        limit=8,
    )

    categories = [question["category"] for question in questions]

    assert "Education" in categories


def test_experienced_prioritizes_experience(generator):
    questions = generator.generate_questions(
        role="Data Analyst",
        experience_level="experienced",
        limit=8,
    )

    categories = [question["category"] for question in questions]

    assert "Experience" in categories