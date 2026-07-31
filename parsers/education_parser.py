"""
Education Parser
----------------
Extracts education and certification details
from the resume Education section.

Fields extracted:
- Degree Type
- Field of Study
- Institution
- Graduation Year
- Certifications
"""

import re


class EducationParser:
    def __init__(self):

        self.year_pattern = re.compile(r"(19|20)\d{2}")

        self.degree_keywords = [
            "Bachelor",
            "Master",
            "B.Tech",
            "M.Tech",
            "B.E",
            "M.E",
            "BCA",
            "MCA",
            "B.Sc",
            "M.Sc",
            "PhD",
            "Diploma"
        ]

    def parse(self, education_text):
        """
        Parse the Education section and return
        structured education and certification data.
        """

        profile = {
            "education": [],
            "certifications": []
        }

        lines = [
            line.strip()
            for line in education_text.split("\n")
            if line.strip()
        ]

        for line in lines:

            degree = ""
            institution = ""
            year = ""
            field = ""

            # Degree detection
            for keyword in self.degree_keywords:
                if keyword.lower() in line.lower():
                    degree = keyword
                    break

            # Graduation year
            year_match = self.year_pattern.search(line)
            if year_match:
                year = year_match.group()

            # Split using commas
            parts = [p.strip() for p in line.split(",")]

            if len(parts) >= 2:
                institution = parts[-1]

            if len(parts) >= 3:
                field = parts[1]

            if degree:
                profile["education"].append(
                    {
                        "degree": degree,
                        "field": field,
                        "institution": institution,
                        "graduation_year": year
                    }
                )
            else:
                profile["certifications"].append(line)

        return profile


if __name__ == "__main__":

    sample = """
B.Tech, Computer Science, ABC University, 2024
MCA, Data Science, XYZ College, 2026
Google Data Analytics Professional Certificate
Microsoft Azure Fundamentals
"""

    parser = EducationParser()

    result = parser.parse(sample)

    from pprint import pprint

    pprint(result)