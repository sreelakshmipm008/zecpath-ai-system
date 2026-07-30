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
    "Python Programming": "Python",
    "JS": "JavaScript",
    "ReactJS": "React",
    "React.js": "React",
    "NodeJS": "Node.js",
    "PowerBI": "Power BI",
    "Microsoft Power BI": "Power BI",
    "Google Analytics 4": "Google Analytics",
    "REST API": "REST APIs",
    # Spelling / formatting variations
    "Javascript": "JavaScript",
    "Java Script": "JavaScript",

    "Power Bi": "Power BI",

    "My SQL": "MySQL",

    "Postgres": "PostgreSQL",

    "React Js": "React",

    "Node Js": "Node.js",

    "Mongo DB": "MongoDB",

    "Tensor Flow": "TensorFlow",

    "Scikit Learn": "Scikit-learn",

    "Num Py": "NumPy",

    "Mat Plot Lib": "Matplotlib",

    "Sea Born": "Seaborn",

    "Github": "GitHub",

    "Aws": "AWS",

    "Html": "HTML",

    "Css": "CSS"
    
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