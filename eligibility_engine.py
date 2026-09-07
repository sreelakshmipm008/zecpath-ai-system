"""
Eligibility Decision Engine

Evaluates candidates against role-specific eligibility rules
and ATS score thresholds.
"""

from eligibility_config import ELIGIBILITY_RULES


class EligibilityEngine:
    """
    Determines whether a candidate is Eligible, Review, or Rejected.
    """

    def evaluate_candidate(self, candidate):
        """
        Evaluate a single candidate against the configured
        eligibility rules for the candidate's job role.
        """

        role = candidate.get("job_role")
        overall_score = candidate.get("overall_score", 0)

        rules = ELIGIBILITY_RULES.get(role)

        if rules is None:
            return {
                **candidate,
                "eligibility_status": "Review",
                "eligibility_reasons": [
                    "No eligibility rules configured for this role."
                ]
            }

        reasons = []

        if overall_score < rules["minimum_ats_score"]:
            reasons.append(
                f"ATS score {overall_score} is below the minimum "
                f"score of {rules['minimum_ats_score']}."
            )

        candidate_skills = {
            skill.strip().lower()
            for skill in candidate.get("skills", [])
        }

        missing_skills = [
            skill
            for skill in rules["mandatory_skills"]
            if skill.lower() not in candidate_skills
        ]

        if missing_skills:
            reasons.append(
                "Missing mandatory skills: "
                + ", ".join(missing_skills)
            )

        experience = candidate.get("experience_years")

        if experience is not None:
            if experience < rules["minimum_experience"]:
                reasons.append(
                    f"Experience {experience} years is below the "
                    f"minimum requirement of "
                    f"{rules['minimum_experience']} years."
                )

            maximum_experience = rules["maximum_experience"]

            if (
                maximum_experience is not None
                and experience > maximum_experience
            ):
                reasons.append(
                    f"Experience {experience} years exceeds the "
                    f"maximum requirement of "
                    f"{maximum_experience} years."
                )

        candidate_location = candidate.get("location")

        if (
            rules["location"] is not None
            and candidate_location is not None
            and candidate_location.strip().lower()
            != rules["location"].strip().lower()
        ):
            reasons.append(
                f"Location '{candidate_location}' does not match "
                f"the required location '{rules['location']}'."
            )

        required_availability = rules["availability"]
        candidate_availability = candidate.get("availability")

        if (
            required_availability is not None
            and candidate_availability != required_availability
        ):
            reasons.append(
                "Availability does not satisfy the configured requirement."
            )

        if overall_score < rules["minimum_ats_score"]:
            status = "Rejected"
        elif overall_score >= rules["eligible_ats_score"] and not reasons:
            status = "Eligible"
        else:
            status = "Review"

        return {
            **candidate,
            "eligibility_status": status,
            "eligibility_reasons": reasons
        }

    def evaluate_candidates(self, candidates):
        """
        Evaluate multiple candidates.
        """

        return [
            self.evaluate_candidate(candidate)
            for candidate in candidates
        ]