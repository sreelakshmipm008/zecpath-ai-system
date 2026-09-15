from interview_ai.hr_interview_categories import (
    HRInterviewCategory,
    HR_INTERVIEW_CATEGORY_ORDER,
    get_category_description,
    get_hr_interview_categories,
)


def test_day33_has_six_hr_categories():
    categories = get_hr_interview_categories()

    assert len(categories) == 6


def test_day33_category_order():
    categories = get_hr_interview_categories()

    assert categories == [
        "self_introduction",
        "career_journey",
        "strengths_weaknesses",
        "teamwork_culture_fit",
        "career_goals",
        "availability_commitment",
    ]


def test_all_categories_have_descriptions():
    for category in HR_INTERVIEW_CATEGORY_ORDER:
        description = get_category_description(category)

        assert description
        assert isinstance(description, str)


def test_category_enum_values():
    assert HRInterviewCategory.SELF_INTRODUCTION.value == "self_introduction"
    assert HRInterviewCategory.CAREER_JOURNEY.value == "career_journey"
    assert (
        HRInterviewCategory.STRENGTHS_WEAKNESSES.value
        == "strengths_weaknesses"
    )
    assert (
        HRInterviewCategory.TEAMWORK_CULTURE_FIT.value
        == "teamwork_culture_fit"
    )
    assert HRInterviewCategory.CAREER_GOALS.value == "career_goals"
    assert (
        HRInterviewCategory.AVAILABILITY_COMMITMENT.value
        == "availability_commitment"
    )