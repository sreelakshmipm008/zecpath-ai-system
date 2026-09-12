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
    "Accountant": {
        "Could you please introduce yourself and briefly describe your professional background?":
            "I am an accountant with experience handling financial records, bookkeeping, and accounting operations.",
        "What is your highest educational qualification?":
            "I completed my Bachelor's degree in Commerce.",
        "How many years of professional experience do you have in accounting?":
            "I have 3 years of professional experience in accounting.",
        "Do you have experience using Tally for accounting tasks?":
            "Yes, I have professional experience using Tally for accounting tasks.",
        "Do you have experience handling GST-related accounting work?":
            "Yes, I have experience handling GST-related accounting work.",
        "Do you have experience using Excel for accounting work?":
            "Yes, I regularly use Excel for accounting work.",
        "Are you familiar with accounting standards?":
            "Yes, I am familiar with accounting standards and basic financial reporting practices.",
        "Where are you currently located, and are you available to work from the required location?":
            "I am currently located in Kochi and can work from the required location.",
        "What are your current and expected salary requirements?":
            "My expected salary is 6 LPA.",
        "What is your current notice period, and when would you be available to join?":
            "I have a 30 days notice period.",
    },

    "AWS Cloud Engineer": {
        "Could you please introduce yourself and briefly describe your professional background?":
            "I am an AWS Cloud Engineer with experience managing cloud infrastructure, deployments, and automation.",
        "What is your highest educational qualification?":
            "I completed my Bachelor's degree in Computer Science.",
        "How many years of professional experience do you have in cloud engineering?":
            "I have 3 years of professional experience in cloud engineering.",
        "Do you have professional experience working with AWS?":
            "Yes, I have professional experience working with AWS cloud services.",
        "Do you have experience working with Linux systems?":
            "Yes, I have experience administering and working with Linux systems.",
        "Do you have experience using Docker?":
            "Yes, I have experience using Docker for application deployment and containerization.",
        "Do you have experience with Terraform?":
            "Yes, I have experience using Terraform for infrastructure automation.",
        "Do you have experience working with Kubernetes?":
            "Yes, I have experience working with Kubernetes for container orchestration.",
        "Where are you currently located, and are you available to work from the required location?":
            "I am currently located in Kochi and can work from the required location.",
        "What are your current and expected salary requirements?":
            "My expected salary is 9 LPA.",
        "What is your current notice period, and when would you be available to join?":
            "I have a 30 days notice period.",
    },

    "Cyber Security Analyst": {
        "Could you please introduce yourself and briefly describe your professional background?":
            "I am a Cyber Security Analyst with experience monitoring security events and supporting security operations.",
        "What is your highest educational qualification?":
            "I completed my Bachelor's degree in Computer Science.",
        "How many years of professional experience do you have in cybersecurity?":
            "I have 3 years of professional experience in cybersecurity.",
        "Do you have professional experience working with SIEM systems?":
            "Yes, I have professional experience working with SIEM systems for security monitoring.",
        "Do you have experience in network security?":
            "Yes, I have experience with network security monitoring and security controls.",
        "Do you have experience using Python for cybersecurity-related tasks?":
            "Yes, I have used Python for cybersecurity-related automation and analysis.",
        "Do you have experience with ethical hacking?":
            "Yes, I have experience with ethical hacking and basic penetration testing activities.",
        "Where are you currently located, and are you available to work from the required location?":
            "I am currently located in Kochi and can work from the required location.",
        "What are your current and expected salary requirements?":
            "My expected salary is 8 LPA.",
        "What is your current notice period, and when would you be available to join?":
            "I have a 30 days notice period.",
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

    "Digital Marketing Executive": {
        "Could you please introduce yourself and briefly describe your professional background?":
            "I am a digital marketing professional with experience in online campaigns, search marketing, and content promotion.",
        "What is your highest educational qualification?":
            "I completed my Bachelor's degree in Business Administration.",
        "How many years of professional experience do you have in digital marketing?":
            "I have 2 years of professional experience in digital marketing.",
        "Do you have professional experience with SEO?":
            "Yes, I have professional experience working with SEO strategies.",
        "Do you have experience working with SEM?":
            "Yes, I have experience working with SEM campaigns.",
        "Do you have experience using Google Analytics?":
            "Yes, I have experience using Google Analytics to track website and campaign performance.",
        "Do you have experience in content marketing?":
            "Yes, I have experience creating and managing content marketing campaigns.",
        "Where are you currently located, and are you available to work from the required location?":
            "I am currently located in Kochi and can work from the required location.",
        "What are your current and expected salary requirements?":
            "My expected salary is 6 LPA.",
        "What is your current notice period, and when would you be available to join?":
            "I have a 30 days notice period.",
    },

    "HR Executive": {
        "Could you please introduce yourself and briefly describe your professional background?":
            "I am an HR professional with experience supporting recruitment, employee records, and HR operations.",
        "What is your highest educational qualification?":
            "I completed my Bachelor's degree in Business Administration.",
        "How many years of professional experience do you have in human resources?":
            "I have 2 years of professional experience in human resources.",
        "Do you have professional experience in recruitment?":
            "Yes, I have professional experience in recruitment and candidate screening.",
        "Do you have experience working with HRMS systems?":
            "Yes, I have experience working with HRMS systems.",
        "Do you have experience using Excel for HR-related work?":
            "Yes, I use Excel for HR reporting and employee-related work.",
        "Would you consider communication one of your professional strengths?":
            "Yes, communication is one of my professional strengths.",
        "Where are you currently located, and are you available to work from the required location?":
            "I am currently located in Kochi and can work from the required location.",
        "What are your current and expected salary requirements?":
            "My expected salary is 6 LPA.",
        "What is your current notice period, and when would you be available to join?":
            "I have a 30 days notice period.",
    },

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

    "Sales Executive": {
        "Could you please introduce yourself and briefly describe your professional background?":
            "I am a sales professional with experience in customer acquisition, lead generation, and relationship management.",
        "What is your highest educational qualification?":
            "I completed my Bachelor's degree in Business Administration.",
        "How many years of professional experience do you have in sales?":
            "I have 3 years of professional experience in sales.",
        "Do you have professional experience using CRM systems?":
            "Yes, I have professional experience using CRM systems to manage customer interactions and leads.",
        "Do you have experience in negotiation?":
            "Yes, I have experience negotiating with customers and handling sales discussions.",
        "Do you have experience in lead generation?":
            "Yes, I have experience in lead generation through multiple sales channels.",
        "Do you have experience giving professional presentations?":
            "Yes, I have experience giving professional sales presentations.",
        "Where are you currently located, and are you available to work from the required location?":
            "I am currently located in Kochi and can work from the required location.",
        "What are your current and expected salary requirements?":
            "My expected salary is 6 LPA.",
        "What is your current notice period, and when would you be available to join?":
            "I have a 30 days notice period.",
    },

    "Staff Nurse": {
        "Could you please introduce yourself and briefly describe your professional background?":
            "I am a staff nurse with experience providing patient care and supporting clinical operations.",
        "What is your highest educational qualification?":
            "I completed my Bachelor of Science in Nursing.",
        "How many years of professional experience do you have in nursing?":
            "I have 3 years of professional experience in nursing.",
        "Do you have professional experience in patient care?":
            "Yes, I have professional experience providing patient care.",
        "Do you have experience working in an ICU environment?":
            "Yes, I have experience working in an ICU environment.",
        "Do you have experience providing emergency care?":
            "Yes, I have experience providing emergency care and supporting emergency procedures.",
        "Would you consider communication one of your professional strengths?":
            "Yes, communication is one of my professional strengths when working with patients and healthcare teams.",
        "Where are you currently located, and are you available to work from the required location?":
            "I am currently located in Kochi and can work from the required location.",
        "What are your current and expected salary requirements?":
            "My expected salary is 5 LPA.",
        "What is your current notice period, and when would you be available to join?":
            "I have a 30 days notice period.",
    },

    "UI/UX Designer": {
        "Could you please introduce yourself and briefly describe your professional background?":
            "I am a UI/UX designer with experience designing user interfaces and improving digital user experiences.",
        "What is your highest educational qualification?":
            "I completed my Bachelor's degree in Computer Science.",
        "How many years of professional experience do you have in UI/UX design?":
            "I have 2 years of professional experience in UI/UX design.",
        "Do you have professional experience using Figma?":
            "Yes, I have professional experience using Figma for interface design and prototyping.",
        "Do you have experience using Adobe XD?":
            "Yes, I have experience using Adobe XD for UI/UX design.",
        "Do you have experience creating wireframes?":
            "Yes, I have experience creating wireframes for web and mobile applications.",
        "Do you have experience working with HTML and CSS?":
            "Yes, I have basic experience working with HTML and CSS.",
        "Where are you currently located, and are you available to work from the required location?":
            "I am currently located in Kochi and can work from the required location.",
        "What are your current and expected salary requirements?":
            "My expected salary is 6 LPA.",
        "What is your current notice period, and when would you be available to join?":
            "I have a 30 days notice period.",
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
        candidate_name = f"Sample {role} Candidate"

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