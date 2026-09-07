"""
Eligibility Rule Configuration

Defines role-specific eligibility rules for the
Eligibility Decision Engine.
"""

ELIGIBILITY_RULES = {

    "Accountant": {
        "minimum_ats_score": 60,
        "eligible_ats_score": 80,
        "mandatory_skills": [
            "Tally",
            "GST",
            "Excel"
        ],
        "minimum_experience": 2,
        "maximum_experience": None,
        "location": "Thrissur",
        "availability": None
    },

    "AWS Cloud Engineer": {
        "minimum_ats_score": 60,
        "eligible_ats_score": 80,
        "mandatory_skills": [
            "AWS",
            "Linux",
            "Docker",
            "Terraform"
        ],
        "minimum_experience": 3,
        "maximum_experience": None,
        "location": "Bengaluru",
        "availability": None
    },

    "Cyber Security Analyst": {
        "minimum_ats_score": 60,
        "eligible_ats_score": 80,   
        "mandatory_skills": [
            "SIEM",
            "Network Security",
            "Python"
        ],
        "minimum_experience": 2,
        "maximum_experience": None,
        "location": "Chennai",
        "availability": None
    },

    "Data Analyst": {
    "minimum_ats_score": 60,
    "eligible_ats_score": 80,
    "mandatory_skills": ["Python", 
                         "SQL", 
                         "Power BI", 
                         "Excel"],

        "minimum_experience": 1,
        "maximum_experience": None,
        "location": "Hyderabad",
        "availability": None
    },

    "Digital Marketing Executive": {
        "minimum_ats_score": 60,
        "eligible_ats_score": 80,
        "mandatory_skills": [
            "SEO",
            "SEM",
            "Google Analytics"
        ],
        "minimum_experience": 2,
        "maximum_experience": None,
        "location": "Kochi",
        "availability": None
    },

    "HR Executive": {
        "minimum_ats_score": 60,
        "eligible_ats_score": 80,
        "mandatory_skills": [
            "Recruitment",
            "HRMS",
            "Excel"
        ],
        "minimum_experience": 1,
        "maximum_experience": None,
        "location": "Coimbatore",
        "availability": None
    },

    "Python Developer": {
        "minimum_ats_score": 60,
        "eligible_ats_score": 80,
        "mandatory_skills": [
            "Python",
            "Django",
            "Flask",
            "SQL",
            "Git"
        ],
        "minimum_experience": 2,
        "maximum_experience": None,
        "location": "Bengaluru",
        "availability": None
    },

    "Sales Executive": {
        "minimum_ats_score": 60,
        "eligible_ats_score": 80,
        "mandatory_skills": [
            "CRM",
            "Negotiation",
            "Lead Generation"
        ],
        "minimum_experience": 2,
        "maximum_experience": None,
        "location": "Ernakulam",
        "availability": None
    },

    "Staff Nurse": {
        "minimum_ats_score": 60,
        "eligible_ats_score": 80,
        "mandatory_skills": [
            "Patient Care",
            "ICU",
            "Emergency Care"
        ],
        "minimum_experience": 2,
        "maximum_experience": None,
        "location": "Kozhikode",
        "availability": None
    },

    "UI/UX Designer": {
        "minimum_ats_score": 60,
        "eligible_ats_score": 80,
        "mandatory_skills": [
            "Figma",
            "Adobe XD",
            "Wireframing"
        ],
        "minimum_experience": 2,
        "maximum_experience": None,
        "location": "Pune",
        "availability": None
    }
}