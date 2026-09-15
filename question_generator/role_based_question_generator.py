"""
Day 33 - Role-Based HR Screening Question Generator.

Generates interview questions from the existing HR screening question bank
based on:
    - role
    - candidate experience level
    - technical/non-technical role classification
    - requested language

The generator intentionally reuses the existing Day 22 question bank.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_QUESTION_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "hr_screening"
    / "ai_screening_questions.json"
)


TECHNICAL_ROLES = {
    "AWS_Cloud_Engineer",
    "Cyber_Security_Analyst",
    "Data_Analyst",
    "Python_Developer",
}

NON_TECHNICAL_ROLES = {
    "Accountant",
    "Digital_Marketing_Executive",
    "HR_Executive",
    "Sales_Executive",
    "Staff_Nurse",
    "UI_UX_Designer",
}


class RoleBasedQuestionGenerator:
    """Generate profile-aware, role-specific HR screening questions."""

    VALID_EXPERIENCE_LEVELS = {"fresher", "experienced"}
    VALID_LANGUAGES = {"en", "ml"}

    # Maximum number of questions in a generated interview set.
    DEFAULT_QUESTION_LIMIT = 8

    def __init__(
        self,
        question_file: Optional[str | Path] = None,
    ) -> None:
        self.question_file = Path(question_file or DEFAULT_QUESTION_FILE)
        self.questions = self._load_questions()

    def _load_questions(self) -> List[Dict[str, Any]]:
        """Load and validate the question bank."""
        if not self.question_file.exists():
            raise FileNotFoundError(
                f"Question bank not found: {self.question_file}"
            )

        with self.question_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Question bank must contain a JSON list.")

        return data

    @staticmethod
    def normalize_role(role: str) -> str:
        """Normalize a role name for matching."""
        return role.strip().replace("-", "_").replace("/", "_").replace(" ", "_")

    @staticmethod
    def _display_role(role: str) -> str:
        """Return the role name used by the question dataset."""
        normalized = RoleBasedQuestionGenerator.normalize_role(role)

        mapping = {
            "AWS_Cloud_Engineer": "AWS Cloud Engineer",
            "Cyber_Security_Analyst": "Cyber Security Analyst",
            "Data_Analyst": "Data Analyst",
            "Digital_Marketing_Executive": "Digital Marketing Executive",
            "HR_Executive": "HR Executive",
            "Python_Developer": "Python Developer",
            "Sales_Executive": "Sales Executive",
            "Staff_Nurse": "Staff Nurse",
            "UI_UX_Designer": "UI/UX Designer",
        }

        return mapping.get(normalized, role.strip())

    def classify_role(self, role: str) -> str:
        """Classify a role as technical or non-technical."""
        normalized = self.normalize_role(role)

        if normalized in TECHNICAL_ROLES:
            return "technical"

        if normalized in NON_TECHNICAL_ROLES:
            return "non-technical"

        raise ValueError(f"Unsupported role: {role}")

    def _filter_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Return questions belonging to the requested role."""
        dataset_role = self._display_role(role)

        matches = [
            question
            for question in self.questions
            if str(question.get("role", "")).strip().lower()
            == dataset_role.lower()
        ]

        if not matches:
            raise ValueError(f"No questions found for role: {role}")

        return matches

    @staticmethod
    def _profile_category_order(
        experience_level: str,
        role_type: str,
    ) -> List[str]:
        """
        Return category priority based on candidate profile.

        The ordering combines experience level and role type so that
        candidate profiles receive different question priorities.
        """

        if experience_level == "fresher":
            if role_type == "technical":
                return [
                    "Introduction",
                    "Education",
                    "Skills",
                    "Experience",
                    "Location",
                    "Notice Period",
                    "Salary",
                ]

            return [
                "Introduction",
                "Education",
                "Skills",
                "Location",
                "Career Goals",
                "Notice Period",
                "Salary",
                "Experience",
            ]

        # Experienced candidate
        if role_type == "technical":
            return [
                "Introduction",
                "Experience",
                "Skills",
                "Education",
                "Location",
                "Notice Period",
                "Salary",
            ]

        return [
            "Introduction",
            "Experience",
            "Skills",
            "Location",
            "Salary",
            "Notice Period",
            "Education",
        ]

    @staticmethod
    def _question_priority(
        question: Dict[str, Any],
        experience_level: str,
        role_type: str,
    ) -> tuple:
        """
        Score a question for profile-aware selection.

        Higher-priority questions are selected first within each category.
        """

        category = str(question.get("category", ""))
        importance = str(
            question.get("scoring_importance", "")
        ).lower()

        importance_score = {
            "high": 3,
            "medium": 2,
            "low": 1,
        }.get(importance, 0)

        mandatory_score = 1 if question.get("mandatory") else 0

        # Experience-level preferences.
        experience_bonus = 0

        if experience_level == "fresher":
            if category == "Education":
                experience_bonus += 3
            elif category == "Experience":
                experience_bonus -= 2

        elif experience_level == "experienced":
            if category == "Experience":
                experience_bonus += 3
            elif category == "Education":
                experience_bonus -= 1

        # Role-type preferences.
        role_bonus = 0

        if role_type == "technical":
            if category == "Skills":
                role_bonus += 3
        else:
            if category in {
                "Experience",
                "Location",
                "Salary",
                "Notice Period",
            }:
                role_bonus += 1

        return (
            mandatory_score,
            importance_score,
            experience_bonus,
            role_bonus,
        )

    def _select_profile_questions(
        self,
        role_questions: List[Dict[str, Any]],
        experience_level: str,
        role_type: str,
        limit: int,
    ) -> List[Dict[str, Any]]:
        """
        Select a profile-specific subset of questions.

        Experience level and role type both influence the actual questions
        selected, not just their ordering.
        """

        def sort_key(question: Dict[str, Any]) -> tuple:
            category = str(question.get("category", ""))

            # Profile-specific category priority.
            if experience_level == "fresher":
                experience_priority = {
                    "Education": 0,
                    "Skills": 1,
                    "Introduction": 2,
                    "Location": 3,
                    "Notice Period": 4,
                    "Salary": 5,
                    "Experience": 6,
                }
            else:
                experience_priority = {
                    "Experience": 0,
                    "Skills": 1,
                    "Introduction": 2,
                    "Location": 3,
                    "Notice Period": 4,
                    "Salary": 5,
                    "Education": 6,
                }

            # Technical/non-technical role preference.
            if role_type == "technical":
                role_priority = {
                    "Skills": 0,
                    "Experience": 1,
                    "Education": 2,
                    "Introduction": 3,
                    "Location": 4,
                    "Notice Period": 5,
                    "Salary": 6,
                }
            else:
                role_priority = {
                    "Experience": 0,
                    "Location": 1,
                    "Salary": 2,
                    "Notice Period": 3,
                    "Skills": 4,
                    "Education": 5,
                    "Introduction": 6,
                }

            priority = self._question_priority(
                question,
                experience_level,
                role_type,
            )

            return (
                experience_priority.get(category, 99),
                role_priority.get(category, 99),
                -priority[0],  # mandatory
                -priority[1],  # scoring importance
                -priority[2],  # experience bonus
                -priority[3],  # role bonus
                str(question.get("question_id", "")),
            )

        sorted_questions = sorted(
            role_questions,
            key=sort_key,
        )

        # Select the profile-specific set.
        selected = sorted_questions[:limit]

        return selected

    def generate_questions(
        self,
        role: str,
        experience_level: str,
        language: str = "en",
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate a profile-aware role-based question set.

        Args:
            role: Job role.
            experience_level: "fresher" or "experienced".
            language: "en" or "ml".
            limit: Maximum number of questions. Defaults to 8.

        Returns:
            Ordered list of selected questions with screening metadata.
        """

        experience_level = experience_level.strip().lower()
        language = language.strip().lower()

        if experience_level not in self.VALID_EXPERIENCE_LEVELS:
            raise ValueError(
                "experience_level must be 'fresher' or 'experienced'."
            )

        if language not in self.VALID_LANGUAGES:
            raise ValueError("language must be 'en' or 'ml'.")

        role_type = self.classify_role(role)
        role_questions = self._filter_by_role(role)

        if limit is None:
            limit = self.DEFAULT_QUESTION_LIMIT

        if limit <= 0:
            raise ValueError("limit must be greater than zero.")

        selected_questions = self._select_profile_questions(
            role_questions=role_questions,
            experience_level=experience_level,
            role_type=role_type,
            limit=limit,
        )

        generated: List[Dict[str, Any]] = []

        for question in selected_questions:
            question_text = question.get("question", {})

            if isinstance(question_text, dict):
                text = question_text.get(language)

                if not text:
                    text = question_text.get("en")
            else:
                text = str(question_text)

            generated.append(
                {
                    "question_id": question.get("question_id"),
                    "role": question.get("role"),
                    "role_type": role_type,
                    "experience_level": experience_level,
                    "category": question.get("category"),
                    "question": text,
                    "question_en": (
                        question_text.get("en")
                        if isinstance(question_text, dict)
                        else str(question_text)
                    ),
                    "question_ml": (
                        question_text.get("ml")
                        if isinstance(question_text, dict)
                        else None
                    ),
                    "expected_answer_type": question.get(
                        "expected_answer_type"
                    ),
                    "mandatory": bool(
                        question.get("mandatory", False)
                    ),
                    "scoring_importance": question.get(
                        "scoring_importance"
                    ),
                    "template_id": question.get("template_id"),
                }
            )

        return generated

    def generate_screening_set(
        self,
        role: str,
        experience_level: str,
        language: str = "en",
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Return a complete profile-aware screening configuration."""

        questions = self.generate_questions(
            role=role,
            experience_level=experience_level,
            language=language,
            limit=limit,
        )

        return {
            "role": self._display_role(role),
            "role_type": self.classify_role(role),
            "experience_level": experience_level.lower(),
            "language": language.lower(),
            "question_count": len(questions),
            "questions": questions,
        }


if __name__ == "__main__":
    generator = RoleBasedQuestionGenerator()

    screening = generator.generate_screening_set(
        role="Python Developer",
        experience_level="experienced",
        language="en",
    )

    print(
        json.dumps(
            screening,
            indent=2,
            ensure_ascii=False,
        )
    )