"""
Skill Matching Module
---------------------
Calculates how well a candidate's skills
match the required skills in a job description.
"""

from rapidfuzz import fuzz


class SkillMatcher:

    def score(self, resume_skills, jd_skills):
        """
        Returns matched skills, missing skills,
        and a skill match score (0–100).

        Uses exact matching first and fuzzy matching
        for reasonable skill-name variations.
        """

        # Handle missing data
        if not jd_skills:
            return {
                "matched_skills": [],
                "missing_skills": [],
                "skill_score": 0
            }

        # Normalize skills
        resume_skills = [
            str(skill).lower().strip()
            for skill in resume_skills
            if str(skill).strip()
        ]

        jd_skills = [
            str(skill).lower().strip()
            for skill in jd_skills
            if str(skill).strip()
        ]

        # Remove duplicates while preserving values
        resume_set = set(resume_skills)
        jd_set = set(jd_skills)

        matched = set()
        missing = set()

        # ---------------------------------
        # Exact matching
        # ---------------------------------

        for jd_skill in jd_set:

            if jd_skill in resume_set:
                matched.add(jd_skill)
                continue

            # ---------------------------------
            # Fuzzy skill-name matching
            # ---------------------------------

            best_similarity = 0

            for resume_skill in resume_set:
                similarity = fuzz.token_set_ratio(
                    jd_skill,
                    resume_skill
                )

                if similarity > best_similarity:
                    best_similarity = similarity

            if best_similarity >= 85:
                matched.add(jd_skill)
            else:
                missing.add(jd_skill)

        # Calculate score
        skill_score = round(
            (len(matched) / len(jd_set)) * 100,
            2
        )

        return {
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing),
            "skill_score": skill_score
        }


if __name__ == "__main__":

    resume_skills = [
        "Python",
        "SQL",
        "Pandas",
        "Excel"
    ]

    jd_skills = [
        "Python",
        "SQL",
        "Power BI",
        "Excel",
        "Tableau"
    ]

    matcher = SkillMatcher()

    result = matcher.score(
        resume_skills,
        jd_skills
    )

    from pprint import pprint
    print("Skill Match Result:")
    pprint(result)