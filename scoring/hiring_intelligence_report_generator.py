import json
from copy import deepcopy
from datetime import datetime, timezone


class HiringIntelligenceReportGenerator:
    """Build an explainable, consolidated candidate hiring report."""

    @staticmethod
    def _as_dict(value, section_name):
        if value is None:
            return {
                "available": False,
                "status": "Not provided",
                "data": None,
            }
        if not isinstance(value, dict):
            raise TypeError(f"{section_name} must be a dictionary or None.")
        return {
            "available": True,
            "status": "Available",
            "data": deepcopy(value),
        }

    def generate_report(
        self,
        ats_eligibility_result=None,
        screening_report=None,
        hr_summary=None,
        technical_breakdown=None,
        behavioral_report=None,
        unified_score=None,
        final_recommendation=None,
    ):
        """Combine existing assessment outputs without recalculating scores."""

        sections = {
            "ats_and_eligibility": self._as_dict(
                ats_eligibility_result, "ats_eligibility_result"
            ),
            "ai_screening": self._as_dict(
                screening_report, "screening_report"
            ),
            "hr_interview": self._as_dict(hr_summary, "hr_summary"),
            "technical_interview": self._as_dict(
                technical_breakdown, "technical_breakdown"
            ),
            "behavioral_observations": self._as_dict(
                behavioral_report, "behavioral_report"
            ),
            "unified_scoring": self._as_dict(unified_score, "unified_score"),
            "final_recommendation": self._as_dict(
                final_recommendation, "final_recommendation"
            ),
        }

        ats_data = sections["ats_and_eligibility"]["data"] or {}
        recommendation_data = sections["final_recommendation"]["data"] or {}
        unified_data = sections["unified_scoring"]["data"] or {}

        candidate_name = (
            recommendation_data.get("candidate_name")
            or ats_data.get("candidate_name")
            or "Not provided"
        )
        candidate_id = (
            recommendation_data.get("candidate_id")
            or ats_data.get("candidate_id")
            or "Not provided"
        )
        job_role = (
            recommendation_data.get("job_role")
            or ats_data.get("job_role")
            or unified_data.get("job_role")
            or "Not provided"
        )

        available_sections = [
            name for name, section in sections.items()
            if section["available"]
        ]
        missing_sections = [
            name for name, section in sections.items()
            if not section["available"]
        ]

        return {
            "report_title": "Hiring Intelligence Report",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "candidate_information": {
                "candidate_id": candidate_id,
                "candidate_name": candidate_name,
                "job_role": job_role,
            },
            "executive_summary": {
                "final_recommendation": recommendation_data.get(
                    "decision_category"
                ),
                "unified_score": (
                    unified_data.get("hiring_fit_percentage")
                    if unified_data
                    else recommendation_data.get("unified_score")
                ),
                "eligibility_status": (
                    recommendation_data.get("eligibility_status")
                    or ats_data.get("eligibility_status")
                ),
                "human_review_required": recommendation_data.get(
                    "review_required", True
                ),
                "decision_authority": recommendation_data.get(
                    "final_decision_authority", "Human recruiter"
                ),
            },
            "assessment_sections": sections,
            "report_completeness": {
                "available_section_count": len(available_sections),
                "total_section_count": len(sections),
                "available_sections": available_sections,
                "missing_sections": missing_sections,
            },
            "interpretation_notes": [
                "This report consolidates existing assessment outputs; it does not independently recalculate their scores.",
                "Unavailable assessment sections are identified rather than filled with invented information.",
                "Behavioral observations are informational and must not independently determine candidate suitability.",
                "Evidence completeness is not a probability that a recommendation is correct.",
                "The final hiring decision remains with the human recruiter.",
            ],
        }

    @staticmethod
    def export_json(report, indent=2):
        """Return the report as a JSON string."""
        if not isinstance(report, dict):
            raise TypeError("report must be a dictionary.")
        return json.dumps(report, indent=indent, ensure_ascii=False, default=str)

    @staticmethod
    def export_markdown(report):
        """Return a recruiter-friendly Markdown representation."""
        if not isinstance(report, dict):
            raise TypeError("report must be a dictionary.")

        candidate = report.get("candidate_information", {})
        summary = report.get("executive_summary", {})
        completeness = report.get("report_completeness", {})

        lines = [
            f"# {report.get('report_title', 'Hiring Intelligence Report')}",
            "",
            f"**Generated:** {report.get('generated_at_utc', 'Not provided')}",
            "",
            "## Candidate Information",
            f"- **Candidate:** {candidate.get('candidate_name', 'Not provided')}",
            f"- **Candidate ID:** {candidate.get('candidate_id', 'Not provided')}",
            f"- **Role:** {candidate.get('job_role', 'Not provided')}",
            "",
            "## Executive Summary",
            f"- **Recommendation:** {summary.get('final_recommendation') or 'Not available'}",
            f"- **Unified Score:** {summary.get('unified_score') if summary.get('unified_score') is not None else 'Not available'}",
            f"- **Eligibility:** {summary.get('eligibility_status') or 'Not available'}",
            f"- **Human Review Required:** {summary.get('human_review_required', True)}",
            f"- **Decision Authority:** {summary.get('decision_authority', 'Human recruiter')}",
            "",
            "## Report Completeness",
            f"- **Available sections:** {completeness.get('available_section_count', 0)} of {completeness.get('total_section_count', 0)}",
            f"- **Missing sections:** {', '.join(completeness.get('missing_sections', [])) or 'None'}",
            "",
            "## Assessment Details",
        ]

        for name, section in report.get("assessment_sections", {}).items():
            lines.extend([
                "",
                f"### {name.replace('_', ' ').title()}",
                f"**Status:** {section.get('status', 'Not provided')}",
            ])
            data = section.get("data")
            if data is not None:
                lines.extend([
                    "",
                    "```json",
                    json.dumps(data, indent=2, ensure_ascii=False, default=str),
                    "```",
                ])

        lines.extend(["", "## Interpretation Notes"])
        for note in report.get("interpretation_notes", []):
            lines.append(f"- {note}")

        return "\n".join(lines) + "\n"
