"""
profile_builder.py

Build AI-friendly Job Description profiles
from structured Job Requirement Objects.
"""

import json
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FOLDER = BASE_DIR / "data" / "structured_jd"
OUTPUT_FOLDER = BASE_DIR / "data" / "ai_profiles"

# Create output folder
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


def build_ai_profile(job_requirement):
    """
    Convert a structured Job Requirement Object
    into an AI-friendly profile.
    """

    return {
        "job_profile": {
            "role": job_requirement.get("role"),
            "required_skills": job_requirement.get("skills"),
            "minimum_experience": job_requirement.get("experience"),
            "preferred_education": job_requirement.get("education")
        }
    }


def generate_profiles():
    """
    Generate AI-friendly profiles
    for all structured job descriptions.
    """

    json_files = list(INPUT_FOLDER.glob("*.json"))

    if not json_files:
        print("No structured Job Description files found.")
        return

    for json_file in json_files:

        print(f"\nProcessing: {json_file.name}")

        with open(json_file, "r", encoding="utf-8") as file:
            job_requirement = json.load(file)

        ai_profile = build_ai_profile(job_requirement)

        output_file = OUTPUT_FOLDER / json_file.name

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(ai_profile, file, indent=4)

        print(f"AI Profile Saved: {output_file.name}")

    print("\nAll AI-friendly Job Description profiles generated successfully.")


if __name__ == "__main__":
    generate_profiles()