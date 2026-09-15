"""
Day 33 - HR Interview Categories.

Defines the six HR interview categories specified for the
AI HR Interview Engine.
"""

from enum import Enum
from typing import List


class HRInterviewCategory(str, Enum):
    """Official Day 33 HR interview categories."""

    SELF_INTRODUCTION = "self_introduction"
    CAREER_JOURNEY = "career_journey"
    STRENGTHS_WEAKNESSES = "strengths_weaknesses"
    TEAMWORK_CULTURE_FIT = "teamwork_culture_fit"
    CAREER_GOALS = "career_goals"
    AVAILABILITY_COMMITMENT = "availability_commitment"


HR_INTERVIEW_CATEGORY_ORDER: List[HRInterviewCategory] = [
    HRInterviewCategory.SELF_INTRODUCTION,
    HRInterviewCategory.CAREER_JOURNEY,
    HRInterviewCategory.STRENGTHS_WEAKNESSES,
    HRInterviewCategory.TEAMWORK_CULTURE_FIT,
    HRInterviewCategory.CAREER_GOALS,
    HRInterviewCategory.AVAILABILITY_COMMITMENT,
]


HR_INTERVIEW_CATEGORY_DESCRIPTIONS = {
    HRInterviewCategory.SELF_INTRODUCTION:
        "Candidate introduction and professional background.",

    HRInterviewCategory.CAREER_JOURNEY:
        "Candidate's career progression, education, experience and key transitions.",

    HRInterviewCategory.STRENGTHS_WEAKNESSES:
        "Candidate's strengths, weaknesses and self-awareness.",

    HRInterviewCategory.TEAMWORK_CULTURE_FIT:
        "Teamwork, collaboration, communication and organizational culture fit.",

    HRInterviewCategory.CAREER_GOALS:
        "Short-term and long-term career goals, motivation and aspirations.",

    HRInterviewCategory.AVAILABILITY_COMMITMENT:
        "Availability, joining timeline, work commitment and role expectations.",
}


def get_hr_interview_categories() -> List[str]:
    """Return the official categories in interview order."""
    return [category.value for category in HR_INTERVIEW_CATEGORY_ORDER]


def get_category_description(category: HRInterviewCategory) -> str:
    """Return the description for an HR interview category."""
    return HR_INTERVIEW_CATEGORY_DESCRIPTIONS[category]