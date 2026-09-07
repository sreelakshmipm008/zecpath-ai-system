"""
Batch Candidate Scoring Module

Reads candidate profiles and their corresponding job descriptions,
calculates component scores using the existing scoring modules,
and generates an overall ATS score for each candidate.
"""

import json
import os
import re

from scoring.ats_score import ATSScorer
from scoring.skill_matching import SkillMatcher
from scoring.experience_relevance import ExperienceRelevanceScorer
from scoring.education_relevance import education_relevance
from scoring.semantic_matching import SemanticMatching
from eligibility_engine import EligibilityEngine


class BatchScorer:

    def __init__(self):
        self.skill_matcher = SkillMatcher()
        self.experience_scorer = ExperienceRelevanceScorer()
        self.semantic_matcher = SemanticMatching()
        self.ats_scorer = ATSScorer()
        self.eligibility_engine = EligibilityEngine()

    def load_json(self, file_path):
        """Load a JSON file."""

        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def calculate_education_score(self, education_result):
        """
        Convert education relevance into a numeric score.

        Relevant -> 100
        General  -> 50
        No education -> 0
        """

        education_records = education_result.get("education", [])

        if not education_records:
            return 0

        relevant_count = sum(
            1
            for education in education_records
            if education.get("relevance") == "Relevant"
        )

        general_count = sum(
            1
            for education in education_records
            if education.get("relevance") == "General"
        )

        total = relevant_count + general_count

        if total == 0:
            return 0

        return round(
            ((relevant_count * 100) + (general_count * 50)) / total,
            2
        )

    def calculate_education_match_score(self, candidate_education, jd_education):
        """
        Compare candidate education with the education requirement
        specified in the job description.

        Returns:
            100 -> candidate satisfies the JD education requirement
            0   -> candidate does not satisfy the requirement
        """

        if not candidate_education or not jd_education:
            return 0

        # Convert candidate education values to normalized strings
        candidate_degrees = {
            str(education).strip().lower()
            for education in candidate_education
        }

        # JD requirements are separated by "/"
        required_degrees = {
            degree.strip().lower()
            for degree in str(jd_education).split("/")
        }

        # Check whether any candidate degree satisfies
        # any accepted JD degree.
        if candidate_degrees & required_degrees:
            return 100

        return 0

    def normalize_candidate(self, candidate, jd):
        """
        Normalize candidate information from the existing segmented
        resume structure before scoring.
        """

        def normalize_list(values):
            """Convert a field into a clean, duplicate-free list."""
            if values is None:
                return []

            if not isinstance(values, list):
                values = [values]

            result = []
            seen = set()

            for value in values:
                text = " ".join(str(value).strip().split())

                if not text:
                    continue

                key = text.lower()

                if key not in seen:
                    seen.add(key)
                    result.append(text)

            return result

        # ---------------------------------
        # Candidate identity information
        # ---------------------------------

        header = candidate.get("header", [])

        if isinstance(header, list) and len(header) >= 2:
            candidate_name = " ".join(
                str(header[0]).strip().split()
            )
            candidate_role = " ".join(
                str(header[1]).strip().split()
            )
        else:
            candidate_name = "Unknown"
            candidate_role = jd.get("role", "default")

        # ---------------------------------
        # Collect all candidate text
        # ---------------------------------

        candidate_text = []

        for field in [
            "summary",
            "experience",
            "skills",
            "projects",
            "education",
            "certifications"
        ]:
            values = candidate.get(field, [])

            if isinstance(values, list):
                candidate_text.extend(
                    str(value) for value in values
                )
            elif values:
                candidate_text.append(str(values))

        full_text = " ".join(candidate_text).lower()

        # ---------------------------------
        # Normalize skills
        # ---------------------------------

        skills = normalize_list(
            candidate.get("skills", [])
        )

        jd_skills = normalize_list(
            jd.get("skills", [])
        )

        existing_skill_keys = {
            skill.lower()
            for skill in skills
        }

        # Preserve existing behavior:
        # recover JD-required skills found anywhere
        # in the candidate resume.
        for skill in jd_skills:
            if skill.lower() in full_text:
                if skill.lower() not in existing_skill_keys:
                    skills.append(skill)
                    existing_skill_keys.add(skill.lower())

        # ---------------------------------
        # Normalize education
        # ---------------------------------

        education = normalize_list(
            candidate.get("education", [])
        )

        jd_education = str(
            jd.get("education", "")
        ).lower()

        required_degrees = [
            degree.strip()
            for degree in jd_education.split("/")
            if degree.strip()
        ]

        education_keys = {
            item.lower()
            for item in education
        }

        # Preserve existing behavior:
        # recover required degree terms found
        # anywhere in candidate information.
        for degree in required_degrees:
            if degree.lower() in full_text:
                if degree.lower() not in education_keys:
                    education.append(degree)
                    education_keys.add(degree.lower())

        # ---------------------------------
        # Normalize experience
        # ---------------------------------

        experience = normalize_list(
            candidate.get("experience", [])
        )

        # If experience is empty, search candidate
        # fields for role and duration information.
        if not experience:

            for field_values in [
                skills,
                candidate.get("certifications", []),
                education,
                candidate.get("summary", [])
            ]:
                values = (
                    field_values
                    if isinstance(field_values, list)
                    else [field_values]
                )

                for value in values:

                    text = str(value)

                    if (
                        " at " in text.lower()
                        or "duration:" in text.lower()
                    ):
                        if text not in experience:
                            experience.append(text)

        # ---------------------------------
        # Normalize remaining fields
        # ---------------------------------

        projects = normalize_list(
            candidate.get("projects", [])
        )

        certifications = normalize_list(
            candidate.get("certifications", [])
        )

        return {
            "candidate_name": candidate_name,
            "candidate_role": candidate_role,
            "skills": skills,
            "experience": experience,
            "education": education,
            "projects": projects,
            "certifications": certifications,
            "location": candidate.get("location"),
            "availability": candidate.get("availability")
        }

    def _extract_experience_years(self, experience):
        """
        Extract the highest experience duration in years
        from the candidate experience entries.
        """

        highest_years = 0.0

        for item in experience:
            if not isinstance(item, str):
                continue

            match = re.search(
                r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
                item,
                re.IGNORECASE
            )

            if match:
                years = float(match.group(1))
                highest_years = max(highest_years, years)

        return highest_years

    def calculate_experience_match_score(self, candidate, jd):
        """
        Compare candidate experience with the JD role and
        required experience duration.

        Role relevance contributes 50 points.
        Duration match contributes 50 points.
        """

        candidate_role = ""
        candidate_years = 0.0

        # Extract candidate role and duration from experience
        # or from skills when experience is empty.
        experience_data = candidate.get("experience", [])

        if not experience_data:
            experience_data = candidate.get("skills", [])

        for item in experience_data:

            if not isinstance(item, str):
                continue

            text = item.strip()

            # Extract role from strings such as:
            # "Data Analyst at ABC Solutions"
            if " at " in text.lower():
                candidate_role = text.split(" at ", 1)[0].strip()

            # Extract duration from strings such as:
            # "Duration: 2 Years"
            duration_match = re.search(
                r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
                text,
                re.IGNORECASE
            )

            if duration_match:
                candidate_years = float(duration_match.group(1))

        # Fallback to the candidate header role
        if not candidate_role:
            header = candidate.get("header", [])

            if isinstance(header, list) and len(header) >= 2:
                candidate_role = str(header[1]).strip()

        # Extract JD role
        jd_role = str(jd.get("role", "")).strip()

        # Role match
        role_match = (
            candidate_role.lower() == jd_role.lower()
            if candidate_role and jd_role
            else False
        )

        # Extract required years from JD
        jd_experience = str(jd.get("experience", ""))

        required_match = re.search(
            r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
            jd_experience,
            re.IGNORECASE
        )

        required_years = (
            float(required_match.group(1))
            if required_match
            else 0.0
        )

        duration_match = (
            candidate_years >= required_years
            if required_years > 0
            else False
        )

        # Calculate score
        score = 0

        if role_match:
            score += 50

        if duration_match:
            score += 50

        return score

    def calculate_candidate_score(self, candidate, jd):
        """Calculate the ATS score for one candidate."""

        candidate = self.normalize_candidate(
            candidate,
            jd
        )

        # Preserve candidate identity for recruiter output only.
        candidate_name = candidate.get(
            "candidate_name",
            "Unknown"
        )

        role = candidate.get(
            "candidate_role",
            jd.get("role", "default")
        )

        # Create a separate scoring copy.
        # Non-essential identity information is excluded
        # from the evaluation process.
        scoring_candidate = candidate.copy()
        scoring_candidate.pop("candidate_name", None)

        # Skill score
        skill_result = self.skill_matcher.score(
            scoring_candidate.get("skills", []),
            jd.get("skills", [])
        )

        skill_score = skill_result["skill_score"]

        # Experience score
        experience_score = self.calculate_experience_match_score(
            scoring_candidate,
            jd
        )

        # Education score
        education_score = self.calculate_education_match_score(
            scoring_candidate.get("education", []),
            jd.get("education", "")
        )

        # Semantic score
        resume_profile = {
            "skills": " ".join(
                scoring_candidate.get("skills", [])
            ),
            "experience": " ".join(
                str(item)
                for item in scoring_candidate.get(
                    "experience",
                    []
                )
            ),
            "projects": " ".join(
                str(item)
                for item in scoring_candidate.get(
                    "projects",
                    []
                )
            )
        }

        jd_profile = {
            "skills": " ".join(
                jd.get("skills", [])
            ),
            "experience": str(
                jd.get("experience", "")
            ),
            "projects": str(
                jd.get("projects", "")
            )
        }

        semantic_scores = []

        if (
            jd_profile["skills"]
            and resume_profile["skills"]
        ):
            semantic_scores.append(
                self.semantic_matcher.similarity(
                    resume_profile["skills"],
                    jd_profile["skills"]
                )
            )

        if (
            jd_profile["experience"]
            and resume_profile["experience"]
        ):
            semantic_scores.append(
                self.semantic_matcher.similarity(
                    resume_profile["experience"],
                    jd_profile["experience"]
                )
            )

        if (
            jd_profile["projects"]
            and resume_profile["projects"]
        ):
            semantic_scores.append(
                self.semantic_matcher.similarity(
                    resume_profile["projects"],
                    jd_profile["projects"]
                )
            )

        if semantic_scores:
            semantic_score = round(
                sum(semantic_scores) / len(semantic_scores),
                2
            )
        else:
            semantic_score = 0

        # Overall ATS score
        overall_score = self.ats_scorer.calculate_score(
            role,
            skill_score,
            experience_score,
            education_score,
            semantic_score
        )

        ats_result = {
    "candidate_name": candidate_name,
    "job_role": role,
    "overall_score": overall_score,

    # Candidate information required by EligibilityEngine
    "skills": scoring_candidate.get("skills", []),
    "experience_years": self._extract_experience_years(
        scoring_candidate.get("experience", [])
    ),
    "location": scoring_candidate.get("location"),
    "availability": scoring_candidate.get("availability"),

    "breakdown": {
        "skills": skill_score,
        "experience": experience_score,
        "education": education_score,
        "semantic": semantic_score
    }
}

        eligibility_result = self.eligibility_engine.evaluate_candidate(
            ats_result
        )

        return eligibility_result

    def score_all_candidates(self, candidate_dir, jd_dir):
        """
        Score all candidate JSON files against their corresponding JD JSON files.
        """

        results = []

        candidate_files = [
            "1.Accountant.json",
            "2.AWS_Cloud_Engineer.json",
            "3.Cyber_Security_Analyst.json",
            "4.Data_Analyst.json",
            "5.Digital_Marketing_Executive.json",
            "6.HR_Executive.json",
            "7.Python_Developer.json",
            "8.Sales_Executive.json",
            "9.Staff_Nurse.json",
            "10.UI-UX_Designer.json"
        ]

        for filename in candidate_files:

            candidate_path = os.path.join(
                candidate_dir,
                filename
            )

            # Remove the numeric prefix from candidate filename
            jd_filename = filename.split(".", 1)[1]

            jd_path = os.path.join(
                jd_dir,
                jd_filename
            )

            if not os.path.exists(candidate_path):
                print(f"Candidate file not found: {filename}")
                continue

            if not os.path.exists(jd_path):
                print(f"JD file not found: {jd_filename}")
                continue

            result = self.score_candidate_file(
                candidate_path,
                jd_path
            )

            results.append(result)

        return results

    def rank_candidates_by_role(self, candidates):
        """
        Group candidates by job role and rank candidates
        within their respective roles using the existing
        RankingEngine.
        """

        from scoring.ranking_engine import RankingEngine

        ranking_engine = RankingEngine()

        candidates_by_role = {}

        for candidate in candidates:
            role = candidate.get("job_role", "Unknown")

            if role not in candidates_by_role:
                candidates_by_role[role] = []

            candidates_by_role[role].append(candidate)

        ranked_results = []

        for role, role_candidates in candidates_by_role.items():

            ranked_candidates = ranking_engine.rank_candidates(
                role_candidates
            )

            ranked_results.extend(ranked_candidates)

        return ranked_results

    def save_ranked_output(self, ranked_candidates, output_path):
        """
        Save ranked candidate results as a JSON file.
        """

        output = []

        for candidate in ranked_candidates:
            output.append({
                "candidate_name": candidate.get("candidate_name", "Unknown"),
                "job_role": candidate.get("job_role", "Unknown"),
                "overall_score": candidate.get("overall_score", 0),
                "rank": candidate.get("rank", 0),
                "status": candidate.get("status", "Unknown"),
                "breakdown": candidate.get("breakdown", {})
            })

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4)

        return output_path

    def generate_recruiter_output(self, ranked_candidates):
        """
        Generate a recruiter-friendly summary of ranked candidates.
        """

        recruiter_output = {
            "shortlisted": [],
            "review": [],
            "auto_rejected": []
        }

        for candidate in ranked_candidates:
            candidate_summary = {
                "candidate_name": candidate.get(
                    "candidate_name", "Unknown"
                ),
                "job_role": candidate.get(
                    "job_role", "Unknown"
                ),
                "overall_score": candidate.get(
                    "overall_score", 0
                ),
                "rank": candidate.get(
                    "rank", 0
                ),
                "status": candidate.get(
                    "status", "Unknown"
                )
            }

            status = candidate.get("status", "").lower()

            if status == "shortlisted":
                recruiter_output["shortlisted"].append(
                    candidate_summary
                )

            elif status == "review":
                recruiter_output["review"].append(
                    candidate_summary
                )

            elif status == "auto-rejected":
                recruiter_output["auto_rejected"].append(
                    candidate_summary
                )

        return recruiter_output

    def score_candidate_file(self, candidate_path, jd_path):
        """Score one candidate against one job description."""

        candidate = self.load_json(candidate_path)
        jd = self.load_json(jd_path)

        return self.calculate_candidate_score(candidate, jd)