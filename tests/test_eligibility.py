from eligibility_engine import EligibilityEngine


def test_candidate_below_minimum_score():
    engine = EligibilityEngine()

    candidate = {
        "candidate_name": "Low Score Candidate",
        "job_role": "Data Analyst",
        "overall_score": 50,
        "skills": [
            "Python",
            "SQL",
            "Power BI",
            "Excel"
        ],
        "experience_years": 2,
        "location": "Hyderabad",
        "availability": None
    }

    result = engine.evaluate_candidate(candidate)

    assert result["eligibility_status"] == "Rejected"
    assert result["eligibility_reasons"]


def test_candidate_missing_mandatory_skill():
    engine = EligibilityEngine()

    candidate = {
        "candidate_name": "Missing Skill Candidate",
        "job_role": "Data Analyst",
        "overall_score": 85,
        "skills": [
            "Python",
            "SQL",
            "Excel"
        ],
        "experience_years": 2,
        "location": "Hyderabad",
        "availability": None
    }

    result = engine.evaluate_candidate(candidate)

    assert result["eligibility_status"] == "Review"
    assert result["eligibility_reasons"]


def test_candidate_wrong_location():
    engine = EligibilityEngine()

    candidate = {
        "candidate_name": "Wrong Location Candidate",
        "job_role": "Data Analyst",
        "overall_score": 85,
        "skills": [
            "Python",
            "SQL",
            "Power BI",
            "Excel"
        ],
        "experience_years": 2,
        "location": "Mumbai",
        "availability": None
    }

    result = engine.evaluate_candidate(candidate)

    assert result["eligibility_status"] == "Review"
    assert result["eligibility_reasons"]


def test_eligible_candidate():
    engine = EligibilityEngine()

    candidate = {
        "candidate_name": "Eligible Candidate",
        "job_role": "Data Analyst",
        "overall_score": 85,
        "skills": [
            "Python",
            "SQL",
            "Power BI",
            "Excel"
        ],
        "experience_years": 2,
        "location": "Hyderabad",
        "availability": None
    }

    result = engine.evaluate_candidate(candidate)

    assert result["eligibility_status"] == "Eligible"
    assert result["eligibility_reasons"] == []