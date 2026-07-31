"""
Role Similarity Module
----------------------
Compares candidate job titles with a target job role.
"""


class RoleSimilarity:

    def __init__(self):
        self.role_map = {
            "Software Engineer": [
                "Software Engineer",
                "Senior Software Engineer",
                "Backend Developer",
                "Full Stack Developer",
                "Python Developer",
            ],
            "Data Scientist": [
                "Data Scientist",
                "Machine Learning Engineer",
                "AI Engineer",
                "Data Analyst",
            ],
            "Frontend Developer": [
                "Frontend Developer",
                "UI Developer",
                "React Developer",
            ],
        }

    def find_similar_roles(self, candidate_roles, target_role):
        """
        Finds candidate roles that are similar to the target role.
        Returns matching roles and a similarity score.
        """

        valid_roles = self.role_map.get(target_role, [])

        matches = []

        for role in candidate_roles:
            if role in valid_roles:
                matches.append(role)

        similarity_score = round(
            (len(matches) / max(len(candidate_roles), 1)) * 100,
            2,
        )

        return {
            "target_role": target_role,
            "similar_roles": matches,
            "similarity_score": similarity_score,
        }


if __name__ == "__main__":

    candidate_roles = [
        "Software Engineer",
        "Senior Software Engineer",
    ]

    target_role = "Software Engineer"

    similarity = RoleSimilarity()

    result = similarity.find_similar_roles(
        candidate_roles,
        target_role,
    )

    from pprint import pprint

    print("Role Similarity Result:")
    pprint(result)