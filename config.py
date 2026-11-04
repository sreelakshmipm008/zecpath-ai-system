"""
Configuration settings for the ATS Scoring Engine.
"""

SCORING_WEIGHTS = {
    "Data Analyst": {
        "skill": 0.40,
        "experience": 0.25,
        "education": 0.15,
        "semantic": 0.20,
    },
    "Data Scientist": {
        "skill": 0.35,
        "experience": 0.30,
        "education": 0.15,
        "semantic": 0.20,
    },
    "Software Engineer": {
        "skill": 0.45,
        "experience": 0.25,
        "education": 0.10,
        "semantic": 0.20,
    },
    "default": {
        "skill": 0.40,
        "experience": 0.25,
        "education": 0.15,
        "semantic": 0.20,
    },
}


# HR Interview Scoring Weights
HR_SCORING_WEIGHTS = {
    "answer_relevance": 0.25,
    "communication_score": 0.25,
    "confidence_score": 0.25,
    "consistency": 0.25,
}

# Technical Interview Scoring Weights
TECHNICAL_SCORING_WEIGHTS = {
    "accuracy": 0.40,
    "explanation_depth": 0.20,
    "logical_reasoning": 0.25,
    "real_world_application": 0.15,
}
