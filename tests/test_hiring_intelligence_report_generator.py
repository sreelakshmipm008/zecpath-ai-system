import json
import pytest

from scoring.hiring_intelligence_report_generator import (
    HiringIntelligenceReportGenerator,
)


@pytest.fixture
def generator():
    return HiringIntelligenceReportGenerator()


def test_generate_report_preserves_existing_assessment_data(generator):
    ats = {
        "candidate_name": "Test Candidate",
        "job_role": "Python Developer",
        "overall_score": 85,
        "eligibility_status": "Eligible",
    }
    screening = {"screening_evaluation": {"final_screening_score": 80}}
    hr = {"overall_performance": {"score": 82}}
    technical = {"overall_technical_score": 88}
    behavioral = {"communication_strength": "Strong"}
    unified = {
        "candidate_id": "C001",
        "candidate_name": "Test Candidate",
        "job_role": "Python Developer",
        "hiring_fit_percentage": 84.5,
        "unified_score": 84.5,
    }
    recommendation = {
        "candidate_id": "C001",
        "candidate_name": "Test Candidate",
        "job_role": "Python Developer",
        "decision_category": "Selected",
        "unified_score": 84.5,
        "review_required": True,
        "final_decision_authority": "Human recruiter",
    }

    report = generator.generate_report(
        ats_eligibility_result=ats,
        screening_report=screening,
        hr_summary=hr,
        technical_breakdown=technical,
        behavioral_report=behavioral,
        unified_score=unified,
        final_recommendation=recommendation,
    )

    assert report["candidate_information"]["candidate_name"] == "Test Candidate"
    assert report["candidate_information"]["job_role"] == "Python Developer"
    assert report["executive_summary"]["unified_score"] == 84.5
    assert report["executive_summary"]["final_recommendation"] == "Selected"
    assert report["assessment_sections"]["hr_interview"]["data"] == hr
    assert report["assessment_sections"]["ai_screening"]["data"] == screening
    assert report["assessment_sections"]["technical_interview"]["data"] == technical
    assert report["assessment_sections"]["behavioral_observations"]["data"] == behavioral


def test_missing_sections_are_not_filled_with_zero(generator):
    report = generator.generate_report()

    assert report["report_completeness"]["available_section_count"] == 0
    assert report["report_completeness"]["total_section_count"] == 7
    assert report["assessment_sections"]["ai_screening"]["data"] is None
    assert "ai_screening" in report["report_completeness"]["missing_sections"]


def test_json_export_is_valid(generator):
    report = generator.generate_report(
        final_recommendation={"decision_category": "Review"}
    )

    exported = generator.export_json(report)
    parsed = json.loads(exported)

    assert parsed["executive_summary"]["final_recommendation"] == "Review"


def test_markdown_export_contains_candidate_and_recommendation(generator):
    report = generator.generate_report(
        ats_eligibility_result={
            "candidate_name": "Anu",
            "job_role": "Data Analyst",
        },
        final_recommendation={"decision_category": "Hold / Review"},
    )

    exported = generator.export_markdown(report)

    assert "# Hiring Intelligence Report" in exported
    assert "Anu" in exported
    assert "Data Analyst" in exported
    assert "Hold / Review" in exported
    assert "Interpretation Notes" in exported


def test_behavioral_observations_do_not_change_recommendation(generator):
    recommendation = {"decision_category": "Review", "unified_score": 75}

    report = generator.generate_report(
        behavioral_report={"communication_strength": "Strong"},
        final_recommendation=recommendation,
    )

    assert report["executive_summary"]["final_recommendation"] == "Review"
    assert report["assessment_sections"]["behavioral_observations"]["data"] == {
        "communication_strength": "Strong"
    }


def test_invalid_section_type_is_rejected(generator):
    with pytest.raises(TypeError):
        generator.generate_report(screening_report="not a dictionary")

def test_candidate_ai_profile_contains_candidate_history_and_findings(generator):
    report = generator.generate_report(
        ats_eligibility_result={
            "candidate_name": "Anu",
            "job_role": "Data Analyst",
            "strengths": ["SQL knowledge"],
        },
        hr_summary={
            "weaknesses": ["Communication needs improvement"],
            "risk_flags": ["Inconsistent answers"],
        },
        final_recommendation={"decision_category": "Review"},
    )

    profile = report["candidate_ai_profile"]

    assert profile["candidate_information"]["candidate_name"] == "Anu"
    assert len(profile["assessment_history"]) == 7
    assert "SQL knowledge" in profile["strengths"]
    assert "Communication needs improvement" in profile["weaknesses"]
    assert "Inconsistent answers" in profile["risk_indicators"]
    assert profile["final_recommendation"]["decision_category"] == "Review"


def test_candidate_profile_does_not_invent_findings(generator):
    report = generator.generate_report()
    profile = report["candidate_ai_profile"]

    assert profile["strengths"] == []
    assert profile["weaknesses"] == []
    assert profile["risk_indicators"] == []

def test_markdown_export_includes_full_candidate_profile(generator):
    report = generator.generate_report(
        ats_eligibility_result={
            "candidate_name": "Anu",
            "strengths": ["SQL knowledge"],
        }
    )

    exported = generator.export_markdown(report)

    assert "Full Candidate AI Profile" in exported
    assert "SQL knowledge" in exported
    assert "assessment_history" in exported
