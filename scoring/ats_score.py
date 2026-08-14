"""
ATS Scoring Engine
------------------
Combines all scoring modules to generate
an overall ATS score with an explainable breakdown.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SCORING_WEIGHTS

from scoring.skill_matching import SkillMatcher
from scoring.experience_relevance import ExperienceRelevanceScorer
from scoring.education_relevance import education_relevance

try:
    from scoring.semantic_matching import SemanticMatching
except ImportError:
    class SemanticMatching:
        def __init__(self):
            self.model = None

        def similarity(self, text1, text2):
            return 0.0

        def compare(self, resume_profile, jd_profile):
            return {
                "skills_similarity": 0,
                "experience_similarity": 0,
                "project_similarity": 0,
                "overall_similarity": 0,
                "match_level": "Unavailable"
            }


class ATSScorer:
    """
    ATS Scoring Engine
    """

    def __init__(self):
        self.skill_matcher = SkillMatcher()
        self.experience_scorer = ExperienceRelevanceScorer()
        self.semantic_matcher = SemanticMatching()

    def calculate_score(
        self,
        role,
        skill_score,
        experience_score,
        education_score,
        semantic_score
    ):
        """
        Calculate the weighted ATS score.
        """

        skill_score = skill_score or 0
        experience_score = experience_score or 0
        education_score = education_score or 0
        semantic_score = semantic_score or 0

        skill_score = max(0, min(100, skill_score))
        experience_score = max(0, min(100, experience_score))
        education_score = max(0, min(100, education_score))
        semantic_score = max(0, min(100, semantic_score))

        weights = SCORING_WEIGHTS.get(
            role,
            SCORING_WEIGHTS["default"]
        )

        overall_score = round(
            (skill_score * weights["skill"]) +
            (experience_score * weights["experience"]) +
            (education_score * weights["education"]) +
            (semantic_score * weights["semantic"]),
            2
        )

        return overall_score

    def generate_breakdown(
        self,
        role,
        skill_score,
        experience_score,
        education_score,
        semantic_score
    ):
        """
        Generate an explainable ATS score breakdown.
        """

        weights = SCORING_WEIGHTS.get(
            role,
            SCORING_WEIGHTS["default"]
        )

        overall_score = self.calculate_score(
            role,
            skill_score,
            experience_score,
            education_score,
            semantic_score
        )

        return {
            "job_role": role,
            "overall_score": overall_score,
            "breakdown": {
                "skills": {
                    "score": skill_score,
                    "weight": weights["skill"] * 100,
                    "contribution": round(skill_score * weights["skill"], 2)
                },
                "experience": {
                    "score": experience_score,
                    "weight": weights["experience"] * 100,
                    "contribution": round(experience_score * weights["experience"], 2)
                },
                "education": {
                    "score": education_score,
                    "weight": weights["education"] * 100,
                    "contribution": round(education_score * weights["education"], 2)
                },
                "semantic": {
                    "score": semantic_score,
                    "weight": weights["semantic"] * 100,
                    "contribution": round(semantic_score * weights["semantic"], 2)
                }
            }
        }


if __name__ == "__main__":
    scorer = ATSScorer()

    result = scorer.generate_breakdown(
        role="Data Analyst",
        skill_score=90,
        experience_score=80,
        education_score=100,
        semantic_score=75
    )

    from pprint import pprint
    pprint(result)