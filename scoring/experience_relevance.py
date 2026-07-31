"""
Experience Relevance Scoring Module
-----------------------------------
Calculates how relevant a candidate's work experience is
to a given job requirement.
"""


class ExperienceRelevanceScorer:

    def score(self, experiences, required_skills):
        """
        Returns a relevance score based on matching job titles
        with required skills.
        """

        matched_roles = []

        for exp in experiences:

            title = exp["job_title"].lower()

            for skill in required_skills:

                if skill.lower() in title:
                    matched_roles.append(exp["job_title"])
                    break

        total_roles = len(experiences)

        if total_roles == 0:
            percentage = 0
        else:
            percentage = round(
                (len(matched_roles) / total_roles) * 100,
                2
            )

        return {
            "matched_roles": matched_roles,
            "relevance_score": percentage
        }


if __name__ == "__main__":

    experiences = [
        {
            "job_title": "Software Engineer"
        },
        {
            "job_title": "Senior Software Engineer"
        }
    ]

    required_skills = [
        "Software",
        "Python",
        "Developer"
    ]

    scorer = ExperienceRelevanceScorer()

    result = scorer.score(
        experiences,
        required_skills
    )

    from pprint import pprint

print("Experience Relevance Score:")
pprint(result)