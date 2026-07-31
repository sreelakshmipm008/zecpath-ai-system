"""
Experience Parser
-----------------
Extracts work experience details from the resume Experience section.

Fields extracted:
- Company Name
- Job Title
- Employment Duration
"""

import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ExperienceParser:
    def __init__(self):
        # Month-Year patterns like:
        # Jan 2022 - Mar 2024
        # January 2022 – Present
        self.date_pattern = re.compile(
            r"((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\s*[-–]\s*(Present|Current|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})",
            re.IGNORECASE,
        )

    def parse(self, experience_text):
        """
        Parses the Experience section and returns structured records.
        """

        experiences = []

        lines = [
            line.strip()
            for line in experience_text.split("\n")
            if line.strip()
        ]

        i = 0

        while i < len(lines):

            line = lines[i]

            match = self.date_pattern.search(line)

            if match:
                start_date = match.group(1)
                end_date = match.group(3)

                job_title = ""
                company = ""

                # Expected format:
                # Job Title
                # Company Name
                # Date Range

                if i >= 1:
                    company = lines[i - 1]

                if i >= 2:
                    job_title = lines[i - 2]

                experiences.append(
                    {
                        "company": company,
                        "job_title": job_title,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                )

            i += 1

        return experiences

    def calculate_total_experience(self, experiences):
        """
        Calculates total professional experience in months and years.
        """

        total_months = 0

        for exp in experiences:

            start = datetime.strptime(exp["start_date"], "%b %Y")

            if exp["end_date"].lower() in ["present", "current"]:
                end = datetime.today()
            else:
                end = datetime.strptime(exp["end_date"], "%b %Y")

            diff = relativedelta(end, start)

            months = diff.years * 12 + diff.months

            total_months += months

        years = total_months // 12
        months = total_months % 12

        return {
            "total_months": total_months,
            "years": years,
            "months": months,
        }

    def detect_employment_gaps(self, experiences):
        """
        Detects employment gaps between consecutive jobs.
        Returns a list of gaps in months.
        """

        if len(experiences) < 2:
            return []

        # Sort by start date
        sorted_exp = sorted(
            experiences,
            key=lambda x: datetime.strptime(x["start_date"], "%b %Y")
        )

        gaps = []

        for i in range(1, len(sorted_exp)):
            previous_end = sorted_exp[i - 1]["end_date"]

            if previous_end.lower() in ["present", "current"]:
                continue

            previous_end_date = datetime.strptime(previous_end, "%b %Y")
            current_start_date = datetime.strptime(
                sorted_exp[i]["start_date"], "%b %Y"
            )

                        # Calculate month difference
            # Calculate month difference
            diff = relativedelta(current_start_date, previous_end_date)

            gap_months = diff.years * 12 + diff.months

            # Moving to the next month is considered continuous employment.
            # Only gaps greater than one month are treated as employment gaps.
            if gap_months > 1:
                gaps.append(
                    {
                        "from_company": sorted_exp[i - 1]["company"],
                        "to_company": sorted_exp[i]["company"],
                        "gap_months": gap_months - 1,
                    }
                )
                gaps.append(
                    {
                        "from_company": sorted_exp[i - 1]["company"],
                        "to_company": sorted_exp[i]["company"],
                        "gap_months": gap_months,
                    }
                )

        return gaps

    def detect_overlapping_roles(self, experiences):
        """
        Detects overlapping employment periods.
        Returns a list of overlapping jobs.
        """

        if len(experiences) < 2:
            return []

        # Sort by start date
        sorted_exp = sorted(
            experiences,
            key=lambda x: datetime.strptime(x["start_date"], "%b %Y")
        )

        overlaps = []

        for i in range(1, len(sorted_exp)):
            previous = sorted_exp[i - 1]
            current = sorted_exp[i]

            previous_end = previous["end_date"]

            if previous_end.lower() in ["present", "current"]:
                previous_end_date = datetime.today()
            else:
                previous_end_date = datetime.strptime(previous_end, "%b %Y")

            current_start_date = datetime.strptime(
                current["start_date"], "%b %Y"
            )

            # If the current job starts before the previous one ends,
            # the employment periods overlap.
            if current_start_date < previous_end_date:
                overlaps.append(
                    {
                        "company_1": previous["company"],
                        "company_2": current["company"],
                        "job_title_1": previous["job_title"],
                        "job_title_2": current["job_title"],
                    }
                )

        return overlaps


if __name__ == "__main__":
    sample = """
Software Engineer
ABC Technologies
Jan 2021 - Mar 2023

Senior Software Engineer
XYZ Solutions
Apr 2023 - Present
"""

    parser = ExperienceParser()

    # Parse experience details
    result = parser.parse(sample)

    from pprint import pprint

    print("Parsed Experience:")
    pprint(result)

    # Calculate total experience
    total = parser.calculate_total_experience(result)

    print("\nTotal Experience:")
    print(f"Years : {total['years']}")
    print(f"Months: {total['months']}")
    print(f"Total Months: {total['total_months']}")

    # Detect employment gaps
    gaps = parser.detect_employment_gaps(result)

    print("\nEmployment Gaps:")

    if gaps:
        pprint(gaps)
    else:
        print("No employment gaps detected.")

    # Detect overlapping roles
    overlaps = parser.detect_overlapping_roles(result)

    print("\nOverlapping Roles:")

    if overlaps:
        pprint(overlaps)
    else:
        print("No overlapping roles detected.")