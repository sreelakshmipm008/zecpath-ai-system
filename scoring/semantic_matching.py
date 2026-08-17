"""
Semantic Matching Engine
------------------------
Computes semantic similarity between resume
and job description sections.
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatching:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def similarity(self, text1, text2):
        """
        Returns similarity score (0–100)
        between two text strings.
        """

        if not text1 or not text2:
            return 0.0

        embeddings = self.model.encode([text1, text2])

        embedding1 = embeddings[0:1]
        embedding2 = embeddings[1:2]

        score = cosine_similarity(
            embedding1,
            embedding2
        )[0][0]

        return round(float(score) * 100, 2)

    def compare(self, resume_profile, jd_profile):
        """
        Compare resume and JD sections.
        """

        result = {
            "skills_similarity": 0,
            "experience_similarity": 0,
            "project_similarity": 0,
            "overall_similarity": 0,
            "match_level": ""
        }

        skills_score = self.similarity(
            resume_profile.get("skills", ""),
            jd_profile.get("skills", "")
        )

        experience_score = self.similarity(
            resume_profile.get("experience", ""),
            jd_profile.get("experience", "")
        )

        project_score = self.similarity(
            resume_profile.get("projects", ""),
            jd_profile.get("projects", "")
        )

        overall = round(
            (
                skills_score +
                experience_score +
                project_score
            ) / 3,
            2,
        )

        if overall >= 85:
            match_level = "Excellent Match"
        elif overall >= 70:
            match_level = "Good Match"
        elif overall >= 50:
            match_level = "Partial Match"
        else:
            match_level = "Poor Match"

        result["skills_similarity"] = skills_score
        result["experience_similarity"] = experience_score
        result["project_similarity"] = project_score
        result["overall_similarity"] = overall
        result["match_level"] = match_level

        return result


if __name__ == "__main__":

    resume = {
        "skills": "Python SQL Machine Learning",
        "experience": "Developed AI applications",
        "projects": "Customer Churn Prediction"
    }

    jobs = [
        {
            "role": "Data Analyst",
            "skills": "Python SQL Power BI",
            "experience": "Data analysis and reporting",
            "projects": "Sales Dashboard"
        },
        {
            "role": "Python Developer",
            "skills": "Python Django REST API",
            "experience": "Backend application development",
            "projects": "Web Application"
        },
        {
            "role": "Machine Learning Engineer",
            "skills": "Python Machine Learning Deep Learning",
            "experience": "Built AI models",
            "projects": "Customer Churn Prediction"
        }
    ]

    matcher = SemanticMatching()

    from pprint import pprint

    for job in jobs:
        print(f"\nJob Role: {job['role']}")
        pprint(matcher.compare(resume, job))