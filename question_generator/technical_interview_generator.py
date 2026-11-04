import json
import re
from pathlib import Path


class TechnicalInterviewGenerator:
    """Generate technical interview questions based on role and experience."""

    DEFAULT_BANK = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "technical_interview"
        / "technical_question_bank.json"
    )

    EXPERIENCE_BANDS = ("0-2", "3-5", "5+")
    QUESTION_TYPES = ("conceptual", "practical", "scenario")

    def __init__(self, bank_path=None):
        self.bank_path = Path(bank_path) if bank_path else self.DEFAULT_BANK
        self.bank = self._load_bank()

    def _load_bank(self):
        try:
            with self.bank_path.open("r", encoding="utf-8-sig") as file:
                bank = json.load(file)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"Technical question bank not found: {self.bank_path}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid question bank JSON: {exc}") from exc

        if not isinstance(bank, dict) or not isinstance(bank.get("roles"), dict):
            raise ValueError("Question bank must contain a roles object.")

        for role, role_data in bank["roles"].items():
            if not isinstance(role_data, dict):
                raise ValueError(f"Invalid role structure: {role}")

            bands = role_data.get("questions")
            if not isinstance(bands, dict):
                raise ValueError(f"Missing questions for role: {role}")

            for band in self.EXPERIENCE_BANDS:
                questions = bands.get(band)
                if not isinstance(questions, list):
                    raise ValueError(
                        f"Expected a question list for {role}, experience {band}."
                    )

                for question in questions:
                    if not isinstance(question, dict):
                        raise ValueError(f"Invalid question entry for {role}, {band}.")
                    if not question.get("question"):
                        raise ValueError(f"Question text missing for {role}, {band}.")
                    if question.get("type") not in self.QUESTION_TYPES:
                        raise ValueError(
                            f"Invalid question type for {role}, {band}: "
                            f"{question.get('type')}"
                        )

        return bank

    @staticmethod
    def _normalize_role(role):
        return re.sub(r"[^a-z0-9]+", " ", str(role).lower()).strip()

    def _find_role(self, requested_role):
        normalized = self._normalize_role(requested_role)

        for role in self.bank["roles"]:
            if self._normalize_role(role) == normalized:
                return role

        available = ", ".join(self.bank["roles"])
        raise ValueError(
            f"Unknown role '{requested_role}'. Available roles: {available}"
        )

    @staticmethod
    def _experience_band(years):
        if isinstance(years, bool) or not isinstance(years, (int, float)):
            raise ValueError("Experience must be a non-negative number of years.")
        if years < 0:
            raise ValueError("Experience cannot be negative.")
        if years <= 2:
            return "0-2"
        if years <= 5:
            return "3-5"
        return "5+"

    def generate_interview(
        self, role, experience_years, question_count=None, skill_domains=None
    ):
        selected_role = self._find_role(role)
        band = self._experience_band(experience_years)

        if question_count is not None:
            if (
                isinstance(question_count, bool)
                or not isinstance(question_count, int)
                or question_count < 1
            ):
                raise ValueError("question_count must be a positive integer.")

        questions = self.bank["roles"][selected_role]["questions"][band]

        if skill_domains:
            domains = {str(domain).strip().lower() for domain in skill_domains}
            questions = [
                q for q in questions
                if str(q.get("domain", "")).lower() in domains
            ]
            if not questions:
                raise ValueError("No questions found for the requested skill domains.")

        # Keep a predictable progression: conceptual, practical, scenario.
        ordered_questions = []
        for question_type in self.QUESTION_TYPES:
            ordered_questions.extend(
                q for q in questions if q["type"] == question_type
            )

        if question_count is not None:
            ordered_questions = ordered_questions[:question_count]

        if not ordered_questions:
            raise ValueError("No questions are available for this interview.")

        return {
            "role": selected_role,
            "experience_years": experience_years,
            "experience_band": band,
            "question_count": len(ordered_questions),
            "question_hierarchy": list(self.QUESTION_TYPES),
            "questions": [dict(q) for q in ordered_questions],
        }


if __name__ == "__main__":
    generator = TechnicalInterviewGenerator()
    result = generator.generate_interview("Python Developer", 2)
    print(json.dumps(result, indent=2))
