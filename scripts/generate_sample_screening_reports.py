from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from scoring.ai_screening_report_builder import (
    AIScreeningReportBuilder,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

QUESTION_FILE = (
    PROJECT_ROOT
    / "data"
    / "hr_screening"
    / "ai_screening_questions.json"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "ai_screening_reports"
)


SAMPLE_ANSWERS = {
    "Python Developer": {
        "Could you please introduce yourself and briefly describe your professional background?":
            "I am a Python developer with experience building backend applications and APIs.",
        "What is your highest educational qualification?":
            "I completed my Bachelor's degree in Computer Science.",
        "How many years of professional experience do you have in Python development?":
            "I have 3 years of professional experience in Python development.",
        "Do you have professional experience with Python?":
            "Yes, I have professional experience with Python.",
        "Do you have experience working with Django?":
            "Yes, I have experience working with Django.",
        "Do you have experience working with Flask?":
            "Yes, I have experience working with Flask.",
        "Do you have experience working with SQL?":
            "Yes, I have experience working with SQL.",
        "Do you have experience using Git?":
            "Yes, I use Git regularly.",
        "Do you have experience developing or working with REST APIs?":
            "Yes, I have experience developing REST APIs.",
        "Do you have experience using Docker?":
            "Yes, I have experience using Docker.",
        "What are your current and expected salary requirements?":
            "My expected salary is 8 LPA.",
        "What is your current notice period, and when would you be available to join?":
            "I can join immediately.",
        "Where are you currently located, and are you available to work from the required location?":
            "I am currently located in Kochi and can work from the required location.",
    },
    "Data Analyst": {
        "Could you please introduce yourself and briefly describe your professional background?":
            "I am a data analyst with experience working on reporting and business analysis.",
        "What is your highest educational qualification?":
            "I completed my Bachelor's degree in Statistics.",
        "How many years of professional experience do you have in data analysis?":
            "I have 2 years of professional experience in data analysis.",
        "Do you have professional experience using Python for data analysis?":
            "Yes, I use Python for data analysis.",
        "Do you have experience working with SQL?":
            "Yes, I have experience working with SQL.",
        "Do you have experience using Power BI?":
            "Yes, I have experience creating dashboards using Power BI.",
        "Do you have experience using Excel for data analysis?":
            "Yes, I have experience using Excel for data analysis.",
        "Do you have experience using Pandas for data analysis?":
            "Yes, I have experience using Pandas.",
        "Do you have knowledge of statistics for data analysis?":
            "Yes, I have a good understanding of statistics.",
        "What are your current and expected salary requirements?":
            "My expected salary is 7 LPA.",
        "What is your current notice period, and when would you be available to join?":
            "I have a 30 days notice period.",
        "Where are you currently located, and are you available to work from the required location?":
            "I am currently located in Kochi and am available to work from the required location.",
    },
}


def load_questions() -> list[dict]:
    """Load the existing AI screening question dataset."""

    with QUESTION_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def build_sample_inputs(
    questions: list[dict],
) -> dict[str, list[dict[str, str]]]:
    """Build sample question-answer inputs from existing questions."""

    samples = {}

    for role, answers in SAMPLE_ANSWERS.items():
        role_questions = [
            item
            for item in questions
            if item["role"] == role
        ]

        questions_and_answers = []

        for item in role_questions:
            question = item["question"]["en"]

            questions_and_answers.append(
                {
                    "question": question,
                    "answer": answers.get(question, ""),
                }
            )

        samples[role] = questions_and_answers

    return samples


def main() -> None:
    """Generate sample reports."""

    questions = load_questions()

    samples = build_sample_inputs(questions)

    builder = AIScreeningReportBuilder()

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for role, questions_and_answers in samples.items():
        candidate_name = (
            "Sample Python Candidate"
            if role == "Python Developer"
            else "Sample Data Analyst"
        )

        report = builder.build_report(
            candidate_name=candidate_name,
            job_role=role,
            questions_and_answers=questions_and_answers,
        )

        output_file = (
            OUTPUT_DIR
            / f"{role.replace('/', '_').replace(' ', '_')}_report.json"
        )

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                report,
                file,
                indent=2,
                ensure_ascii=False,
            )

        print(f"Generated: {output_file}")


if __name__ == "__main__":
    main()