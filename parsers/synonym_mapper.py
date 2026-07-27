"""
synonym_mapper.py

Standardizes skills and role names by mapping
different variations to a common format.
"""


# ----------------------------------------
# Skill Synonyms
# ----------------------------------------

SKILL_SYNONYMS = {
    "Structured Query Language": "SQL",
    "MS Excel": "Excel",
    "Microsoft Excel": "Excel",
    "Amazon Web Services": "AWS",
    "HyperText Markup Language": "HTML",
    "Cascading Style Sheets": "CSS",
    "Py": "Python",
    "Google Analytics 4": "Google Analytics",
    "REST API": "REST APIs"
}


# ----------------------------------------
# Role Synonyms
# ----------------------------------------

ROLE_SYNONYMS = {
    "Python Engineer": "Python Developer",
    "Cloud Engineer": "AWS Cloud Engineer",
    "HR Recruiter": "HR Executive",
    "UI UX Designer": "UI/UX Designer",
    "Digital Marketing Specialist": "Digital Marketing Executive"
}


# ----------------------------------------
# Mapping Functions
# ----------------------------------------

def map_skills(skills):
    """
    Replace skill variations with standardized names.
    """

    standardized = []

    for skill in skills:
        standardized.append(SKILL_SYNONYMS.get(skill, skill))

    return standardized


def map_role(role):
    """
    Replace role variations with standardized role names.
    """

    return ROLE_SYNONYMS.get(role, role)