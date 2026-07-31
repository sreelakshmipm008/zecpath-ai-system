"""
Education Relevance Logic
-------------------------
Assigns relevance categories to education
and certifications based on target job role.
"""

TECH_DEGREES = {
    "Bachelor of Technology",
    "Bachelor of Engineering",
    "Bachelor of Computer Applications",
    "Master of Technology",
    "Master of Computer Applications",
    "Master of Science",
    "B.Tech",
    "B.E",
    "BCA",
    "M.Tech",
    "MCA",
    "M.Sc"
}

TECH_CERTIFICATIONS = {
    "Google Data Analytics Professional Certificate",
    "Microsoft Azure Fundamentals",
    "AWS Certified Cloud Practitioner",
    "IBM Data Science Professional Certificate"
}


def education_relevance(profile):
    """
    Tags education and certifications with relevance categories.
    """

    result = {
        "education": [],
        "certifications": []
    }

    # Process education
    for edu in profile.get("education", []):

        degree = edu.get("degree", "")

        if degree in TECH_DEGREES:
            relevance = "Relevant"
        else:
            relevance = "General"

        record = edu.copy()
        record["relevance"] = relevance

        result["education"].append(record)

    # Process certifications
    for cert in profile.get("certifications", []):

        if cert in TECH_CERTIFICATIONS:
            relevance = "Relevant"
        else:
            relevance = "General"

        result["certifications"].append(
            {
                "name": cert,
                "relevance": relevance
            }
        )

    return result


if __name__ == "__main__":

    sample = {
        "education": [
            {
                "degree": "Bachelor of Technology",
                "field": "Computer Science",
                "institution": "ABC University",
                "graduation_year": "2024"
            },
            {
                "degree": "MCA",
                "field": "Data Science",
                "institution": "XYZ College",
                "graduation_year": "2026"
            }
        ],
        "certifications": [
            "Google Data Analytics Professional Certificate",
            "Coursera Project Management"
        ]
    }

    from pprint import pprint

    print("Education Relevance:")
    pprint(education_relevance(sample))