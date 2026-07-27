"""
jd_parser.py

Main Job Description Parser.

Responsibilities:
1. Read Job Description PDF files
2. Extract text
3. Normalize text
4. Extract Role
5. Extract Skills
6. Extract Experience
7. Extract Education
8. Build Job Requirement Object
9. Save normalized text
10. Save structured JD as JSON

Further parsing steps (synonym mapping,
profile generation) will be added later.
"""

import json
from pathlib import Path

from extractors.pdf_reader import extract_pdf_text
from parsers.normalizer import normalize_text
from parsers.synonym_mapper import map_skills, map_role


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FOLDER = BASE_DIR / "data" / "job_description"
OUTPUT_FOLDER = BASE_DIR / "data" / "normalized_jd"
STRUCTURED_OUTPUT_FOLDER = BASE_DIR / "data" / "structured_jd"

# Create output folders if they don't exist
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
STRUCTURED_OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Extraction Functions
# --------------------------------------------------

def extract_role(text):
    """
    Extract the job role from the Job Description.
    Assumes the first non-empty line is the job role.
    """

    for line in text.splitlines():
        line = line.strip()

        if line:
            return line

    return "Not Found"


def extract_skills(text):
    """
    Extract required and preferred skills.
    """

    skills = []

    for line in text.splitlines():

        line = line.strip()

        if line.startswith("Required Skills:"):
            value = line.replace("Required Skills:", "").strip()

            skills.extend(
                [skill.strip() for skill in value.split(",") if skill.strip()]
            )

        elif line.startswith("Preferred Skills:"):
            value = line.replace("Preferred Skills:", "").strip()

            skills.extend(
                [skill.strip() for skill in value.split(",") if skill.strip()]
            )

    # Remove duplicates while preserving order
    return list(dict.fromkeys(skills))


def extract_experience(text):
    """
    Extract experience requirement.
    """

    for line in text.splitlines():

        line = line.strip()

        if line.startswith("Experience:"):
            return line.replace("Experience:", "").strip()

    return "Not Found"


def extract_education(text):
    """
    Extract education requirement.
    """

    for line in text.splitlines():

        line = line.strip()

        if line.startswith("Education:"):
            return line.replace("Education:", "").strip()

    return "Not Found"


# --------------------------------------------------
# Main Processing Function
# --------------------------------------------------

def process_job_descriptions():
    """
    Read all Job Description PDFs,
    normalize their text,
    extract required information,
    build the job requirement object,
    save the normalized text,
    and save the structured output as JSON.
    """

    pdf_files = list(INPUT_FOLDER.glob("*.pdf"))

    if not pdf_files:
        print("No Job Description PDFs found.")
        return

    for pdf_file in pdf_files:

        print(f"\nProcessing: {pdf_file.name}")

        # Extract text
        raw_text = extract_pdf_text(pdf_file)

        # Normalize text
        normalized_text = normalize_text(raw_text)

        # Extract information
        role = map_role(extract_role(normalized_text))
        skills = map_skills(extract_skills(normalized_text))
        experience = extract_experience(normalized_text)
        education = extract_education(normalized_text)

        # Build Job Requirement Object
        job_requirement = {
            "role": role,
            "skills": skills,
            "experience": experience,
            "education": education
        }

        # Display extracted information
        print(f"Role       : {role}")
        print(f"Skills     : {skills}")
        print(f"Experience : {experience}")
        print(f"Education  : {education}")

        # Save structured JSON
        json_file = STRUCTURED_OUTPUT_FOLDER / f"{pdf_file.stem}.json"

        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(job_requirement, file, indent=4)

        print(f"Structured JD Saved: {json_file.name}")

        # Save normalized text
        output_file = OUTPUT_FOLDER / f"{pdf_file.stem}.txt"

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(normalized_text)

        print(f"Normalized JD Saved: {output_file.name}")

    print("\nAll Job Descriptions processed successfully.")


if __name__ == "__main__":
    process_job_descriptions()