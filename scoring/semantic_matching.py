"""Cached semantic similarity for resume and job-description matching."""

from collections import OrderedDict

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatching:
    def __init__(self, cache_size=512):
        if isinstance(cache_size, bool) or not isinstance(cache_size, int) or cache_size < 1:
            raise ValueError("cache_size must be a positive integer.")

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.cache_size = cache_size
        self._embedding_cache = OrderedDict()

    def _get_embedding(self, text):
        key = str(text)
        if key in self._embedding_cache:
            self._embedding_cache.move_to_end(key)
            return self._embedding_cache[key]

        embedding = np.asarray(
            self.model.encode([key])[0],
            dtype=float,
        )
        self._embedding_cache[key] = embedding
        if len(self._embedding_cache) > self.cache_size:
            self._embedding_cache.popitem(last=False)
        return embedding

    def similarity(self, text1, text2):
        """Return semantic similarity as a percentage from 0 to 100."""
        if not text1 or not text2:
            return 0.0

        embedding1 = self._get_embedding(text1)
        embedding2 = self._get_embedding(text2)
        score = cosine_similarity(
            embedding1.reshape(1, -1),
            embedding2.reshape(1, -1),
        )[0][0]
        return round(float(score) * 100, 2)

    def compare(self, resume_profile, jd_profile):
        """Compare resume and job-description sections."""
        result = {
            "skills_similarity": 0,
            "experience_similarity": 0,
            "project_similarity": 0,
            "overall_similarity": 0,
            "match_level": "",
        }

        scores = {
            "skills_similarity": self.similarity(
                resume_profile.get("skills", ""),
                jd_profile.get("skills", ""),
            ),
            "experience_similarity": self.similarity(
                resume_profile.get("experience", ""),
                jd_profile.get("experience", ""),
            ),
            "project_similarity": self.similarity(
                resume_profile.get("projects", ""),
                jd_profile.get("projects", ""),
            ),
        }

        overall = round(sum(scores.values()) / 3, 2)
        match_level = (
            "Excellent Match" if overall >= 85
            else "Good Match" if overall >= 70
            else "Partial Match" if overall >= 50
            else "Poor Match"
        )

        result.update(scores)
        result["overall_similarity"] = overall
        result["match_level"] = match_level
        return result


if __name__ == "__main__":
    resume = {
        "skills": "Python SQL Machine Learning",
        "experience": "Developed AI applications",
        "projects": "Customer Churn Prediction",
    }
    jobs = [
        {
            "role": "Data Analyst",
            "skills": "Python SQL Power BI",
            "experience": "Data analysis and reporting",
            "projects": "Sales Dashboard",
        },
        {
            "role": "Python Developer",
            "skills": "Python Django REST API",
            "experience": "Backend application development",
            "projects": "Web Application",
        },
        {
            "role": "Machine Learning Engineer",
            "skills": "Python Machine Learning Deep Learning",
            "experience": "Built AI models",
            "projects": "Customer Churn Prediction",
        },
    ]

    from pprint import pprint

    matcher = SemanticMatching()
    for job in jobs:
        print(f"\nJob Role: {job['role']}")
        pprint(matcher.compare(resume, job))
