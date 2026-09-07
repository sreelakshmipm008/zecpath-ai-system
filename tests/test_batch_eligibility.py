from scoring.batch_scorer import BatchScorer


def test_batch_scorer_returns_eligibility_result():
    scorer = BatchScorer()

    candidate = {
        "candidate_name": "Integration Test Candidate",
        "candidate_role": "Data Analyst",
        "skills": [
            "Python",
            "SQL",
            "Power BI",
            "Excel"
        ],
        "experience": [
            "Data Analyst with 2 years of experience"
        ],
        "education": [
            "Bachelor of Computer Applications"
        ],
        "projects": [
            "Data analysis project using Python and SQL"
        ],
        "certifications": [
            "Google Data Analytics"
        ],
        "location": "Hyderabad",
        "availability": None
    }

    jd = {
        "role": "Data Analyst",
        "required_skills": [
            "Python",
            "SQL",
            "Power BI",
            "Excel"
        ],
        "preferred_skills": [],
        "minimum_experience": 1,
        "education": [
            "Bachelor"
        ],
        "description": "Data Analyst role requiring Python, SQL, Power BI and Excel."
    }

    result = scorer.calculate_candidate_score(candidate, jd)

    assert "overall_score" in result
    assert "eligibility_status" in result
    assert "eligibility_reasons" in result

    assert result["job_role"] == "Data Analyst"