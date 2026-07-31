"""
Structured Experience Object
----------------------------
Creates a standardized experience object from parsed experience data.
"""


class ExperienceObject:

    def build(self, experiences, total_experience):
        """
        Builds a structured experience object.
        """

        return {
            "total_experience": {
                "years": total_experience["years"],
                "months": total_experience["months"],
                "total_months": total_experience["total_months"],
            },
            "experience_count": len(experiences),
            "experiences": experiences,
        }


if __name__ == "__main__":

    experiences = [
        {
            "company": "ABC Technologies",
            "job_title": "Software Engineer",
            "start_date": "Jan 2021",
            "end_date": "Mar 2023",
        },
        {
            "company": "XYZ Solutions",
            "job_title": "Senior Software Engineer",
            "start_date": "Apr 2023",
            "end_date": "Present",
        },
    ]

    total_experience = {
        "years": 5,
        "months": 6,
        "total_months": 66,
    }

    builder = ExperienceObject()

    result = builder.build(
        experiences,
        total_experience,
    )

    from pprint import pprint

    print("Structured Experience Object:")
    pprint(result)