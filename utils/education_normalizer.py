"""
Education Normalizer
--------------------
Normalizes degree names and certification names.
"""

DEGREE_MAPPING = {
    "B.Tech": "Bachelor of Technology",
    "B.E": "Bachelor of Engineering",
    "BCA": "Bachelor of Computer Applications",
    "B.Sc": "Bachelor of Science",
    "M.Tech": "Master of Technology",
    "M.E": "Master of Engineering",
    "MCA": "Master of Computer Applications",
    "M.Sc": "Master of Science",
    "PhD": "Doctor of Philosophy"
}


def normalize_degree(degree):
    """
    Returns standardized degree name.
    """
    return DEGREE_MAPPING.get(degree, degree)


def normalize_certification(certification):
    """
    Normalizes certification names.
    """
    return certification.strip().title()