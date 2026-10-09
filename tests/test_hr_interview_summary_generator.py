
from scoring.hr_interview_summary_generator import (
    HRInterviewSummaryGenerator,
)


def test_generates_required_hr_summary_fields():
    generator = HRInterviewSummaryGenerator()

    responses = [
        {
            "question_id": "q1",
            "question": "Tell me about yourself.",
            "response": (
                "I am a data analyst interested in Python, SQL, "
                "Excel and solving business problems."
            ),
            "category": "self_introduction",
        },
        {
            "question_id": "q2",
            "question": "Describe your teamwork experience.",
            "response": (
                "I collaborate with team members, share ideas, "
                "listen to feedback and work toward shared goals."
            ),
            "category": "teamwork_culture_fit",
        },
        {
            "question_id": "q3",
            "question": "How much experience do you have?",
            "response": "I have 2 years of professional experience.",
            "category": "career_journey",
        },
        {
            "question_id": "q4",
            "question": "When can you join?",
            "response": "I am available to join immediately.",
            "category": "availability_commitment",
        },
    ]

    report = generator.generate_summary(
        responses=responses,
        candidate_name="Sample Candidate",
        job_role="Data Analyst",
    )

    assert report["report_title"] == "HR Interview Summary"
    assert report["candidate_information"]["candidate_name"] == (
        "Sample Candidate"
    )
    assert "overall_performance" in report
    assert "strengths" in report
    assert "weaknesses" in report
    assert "cultural_fit_indicators" in report
    assert "consistency_analysis" in report
    assert "risk_flags" in report
    assert isinstance(report["natural_language_report"], str)
    assert "Data Analyst" in report["natural_language_report"]


def test_empty_responses_produce_a_structured_summary():
    generator = HRInterviewSummaryGenerator()

    report = generator.generate_summary(responses=[])

    assert report["overall_performance"]["score"] == 0.0
    assert report["category_summaries"]
    assert report["risk_flags"] == []
    assert isinstance(report["natural_language_report"], str)
