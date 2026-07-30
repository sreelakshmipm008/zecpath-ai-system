import json
import os

from skill_dictionary import MASTER_SKILL_DICTIONARY
from synonym_mapper import map_skills


# ----------------------------------------
# Skill Stacks
# ----------------------------------------

SKILL_STACKS = {
    "MERN": ["MongoDB", "Express.js", "React", "Node.js"],
    "MEAN": ["MongoDB", "Express.js", "Angular", "Node.js"],
    "LAMP": ["Linux", "Apache", "MySQL", "PHP"],
    "XAMPP": ["Apache", "MySQL", "PHP"]
}


def load_resume(json_file):
    """
    Load segmented resume JSON.
    """
    with open(json_file, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_skills(resume_data):
    """
    Extract, normalize, deduplicate and categorize
    skills from the segmented resume.
    """

    extracted = {
        "technical": [],
        "business": [],
        "creative": []
    }

    resume_skills = resume_data.get("skills", [])

    # ----------------------------------------
    # Expand Skill Stacks
    # ----------------------------------------

    expanded_skills = []

    for skill in resume_skills:

        skill = skill.strip()

        if skill.upper() in SKILL_STACKS:
            expanded_skills.extend(SKILL_STACKS[skill.upper()])
        else:
            expanded_skills.append(skill)

    # ----------------------------------------
    # Normalize Skill Names
    # ----------------------------------------

    normalized_skills = map_skills(expanded_skills)

    # ----------------------------------------
    # Remove Duplicate Skills
    # ----------------------------------------

    normalized_skills = list(dict.fromkeys(normalized_skills))

    # Convert to lowercase for comparison

    normalized_lower = [
        skill.lower().strip()
        for skill in normalized_skills
    ]

    # ----------------------------------------
    # Match with Master Skill Dictionary
    # ----------------------------------------

    for category, skill_list in MASTER_SKILL_DICTIONARY.items():

        for master_skill in skill_list:

            if master_skill.lower() in normalized_lower:

                extracted[category].append(master_skill)

    return extracted


def process_resume(json_path):
    """
    Process one segmented resume.
    """

    resume = load_resume(json_path)

    return extract_skills(resume)


if __name__ == "__main__":

    sample = "data/segmented_resumes/test_column_resume.json"

    result = process_resume(sample)

    print(json.dumps(result, indent=4))