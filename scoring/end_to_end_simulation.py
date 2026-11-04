from pathlib import Path
import json
import time

from scoring.ats_score import ATSScorer
from scoring.screening_scoring_engine import ScreeningScoringEngine
from scoring.hr_interview_scoring_engine import HRInterviewScoringEngine
from scoring.technical_skill_scoring_engine import TechnicalSkillScoringEngine
from scoring.unified_scoring_engine import UnifiedScoringEngine
from scoring.final_recommendation_engine import FinalRecommendationEngine


def run_simulation():
    candidates = [
        {
            "id": "SIM001", "name": "Candidate A",
            "ats": [90, 85, 90, 88],
            "screening": [
                {"question": "Explain your Python experience",
                 "answer": "I use Python and pandas for data analysis and automation."},
                {"question": "How do you use SQL?",
                 "answer": "I use SQL joins and queries to extract and analyze business data."}
            ],
            "hr": [
                {"question": "Tell me about yourself",
                 "response": "I am an analytical professional with experience in Python and SQL.",
                 "category": "self_introduction"},
                {"question": "Describe your career goals",
                 "response": "I want to grow in analytics and solve business problems using data.",
                 "category": "career_goals"}
            ],
            "technical": [85, 85, 80, 90],
            "machine": 88, "human": "Selected"
        },
        {
            "id": "SIM002", "name": "Candidate B",
            "ats": [72, 65, 80, 70],
            "screening": [
                {"question": "Explain your Python experience",
                 "answer": "I have basic Python knowledge and I am learning."},
                {"question": "How do you use SQL?",
                 "answer": "I know basic SQL queries."}
            ],
            "hr": [
                {"question": "Tell me about yourself",
                 "response": "I am a recent graduate learning data analysis.",
                 "category": "self_introduction"},
                {"question": "Describe your career goals",
                 "response": "I want to improve my technical skills and work in analytics.",
                 "category": "career_goals"}
            ],
            "technical": [60, 55, 60, 65],
            "machine": 58, "human": "Hold / Review"
        },
        {
            "id": "SIM003", "name": "Candidate C",
            "ats": [45, 50, 70, 48],
            "screening": [
                {"question": "Explain your Python experience",
                 "answer": "I have not worked with Python."},
                {"question": "How do you use SQL?",
                 "answer": "I do not have SQL experience."}
            ],
            "hr": [
                {"question": "Tell me about yourself",
                 "response": "I am exploring different career opportunities.",
                 "category": "self_introduction"},
                {"question": "Describe your career goals",
                 "response": "I am not sure about my career direction yet.",
                 "category": "career_goals"}
            ],
            "technical": [35, 40, 35, 40],
            "machine": 38, "human": "Rejected"
        }
    ]

    ats_engine = ATSScorer()
    screening_engine = ScreeningScoringEngine()
    hr_engine = HRInterviewScoringEngine()
    technical_engine = TechnicalSkillScoringEngine()
    unified_engine = UnifiedScoringEngine()
    recommendation_engine = FinalRecommendationEngine()

    results = []
    started = time.perf_counter()

    for candidate in candidates:
        ats = ats_engine.calculate_score(
            "default", *candidate["ats"]
        )
        screening = screening_engine.score_screening(
            candidate["screening"]
        )["final_screening_score"]
        hr = hr_engine.score_interview(candidate["hr"])["overall_score"]

        dimensions = {
            "accuracy": candidate["technical"][0],
            "explanation_depth": candidate["technical"][1],
            "logical_reasoning": candidate["technical"][2],
            "real_world_application": candidate["technical"][3],
        }
        question = {
            "id": "SIM-TECH-01", "type": "conceptual",
            "difficulty": "intermediate", "domain": "General",
            "expected_points": ["Correct concept", "Clear explanation"]
        }
        technical_result = technical_engine.score_answer(
            question, "Synthetic assessor-evaluated answer.", dimensions
        )
        technical = technical_result["technical_score"]

        machine = candidate["machine"]

        full_score = unified_engine.build_full_candidate_score(
            candidate_id=candidate["id"],
            candidate_name=candidate["name"],
            role="default",
            ats_score=ats,
            screening_score=screening,
            hr_interview_score=hr,
            technical_interview_score=technical,
            machine_test_score=machine,
        )

        recommendation = recommendation_engine.generate_recommendation(
            candidate_score=full_score,
            eligibility_result={
                "eligibility_status": "Eligible",
                "eligibility_reasons": []
            }
        )

        ai_decision = recommendation["decision_category"]
        human_decision = candidate["human"]
        results.append({
            "candidate_id": candidate["id"],
            "candidate_name": candidate["name"],
            "stage_scores": {
                "ats": ats,
                "screening": screening,
                "hr_interview": hr,
                "technical_interview": technical,
                "machine_test": machine,
            },
            "unified_score": full_score["hiring_fit_percentage"],
            "evidence_complete": full_score["evidence_complete"],
            "ai_decision": ai_decision,
            "simulated_human_reference": human_decision,
            "decision_match": ai_decision == human_decision,
            "recommendation": recommendation,
        })

    elapsed = round(time.perf_counter() - started, 4)
    matches = sum(item["decision_match"] for item in results)
    comparison_rate = round(matches / len(results) * 100, 2)

    return {
        "simulation_type": "Synthetic end-to-end hiring simulation",
        "candidate_count": len(results),
        "execution_seconds": elapsed,
        "decision_matches": matches,
        "decision_mismatches": len(results) - matches,
        "reference_agreement_percentage": comparison_rate,
        "candidates": results,
        "limitations": [
            "Candidate data is synthetic.",
            "Human reference decisions are predefined simulation labels, not actual recruiter decisions.",
            "Technical rubric ratings are simulated assessor inputs.",
            "Execution time is a local sample, not a production benchmark."
        ]
    }


def write_reports(report):
    docs = Path("docs")
    docs.mkdir(exist_ok=True)

    rows = []
    for item in report["candidates"]:
        rows.append(
            f"| {item['candidate_id']} | {item['unified_score']} | "
            f"{item['ai_decision']} | {item['simulated_human_reference']} | "
            f"{'Match' if item['decision_match'] else 'Mismatch'} |"
        )

    comparison = "\n".join(rows)
    common = (
        f"Candidates simulated: {report['candidate_count']}\n\n"
        f"Execution time: {report['execution_seconds']} seconds\n\n"
        f"Reference agreement: {report['reference_agreement_percentage']}%\n\n"
        f"Matches: {report['decision_matches']}; "
        f"Mismatches: {report['decision_mismatches']}\n"
    )

    (docs / "day56_end_to_end_ai_test_report.md").write_text(
        "# Day 56 – End-to-End AI Test Report\n\n"
        "## Scope\n\n"
        "Synthetic hiring journey using existing ATS, screening, HR, "
        "technical scoring, five-stage aggregation and recommendation modules.\n\n"
        "## Candidate results\n\n"
        "| Candidate | Unified score | AI recommendation | Human reference | Comparison |\n"
        "|---|---:|---|---|---|\n"
        + comparison + "\n\n## Execution summary\n\n" + common
        + "\n## Limitations\n\n"
        + "\n".join("- " + x for x in report["limitations"]) + "\n",
        encoding="utf-8"
    )

    (docs / "day56_system_performance_analysis.md").write_text(
        "# Day 56 – System Performance Analysis\n\n"
        "## Measured simulation results\n\n" + common
        + "\nThe execution time measures this local synthetic run only. "
        "It is not a throughput, latency, load, or production benchmark.\n\n"
        "## Pipeline stages\n\n"
        "1. Resume/ATS scoring\n2. Screening response scoring\n"
        "3. HR interview scoring\n4. Technical rubric scoring\n"
        "5. Machine-test score input\n6. Five-stage aggregation\n"
        "7. Explainable recommendation\n",
        encoding="utf-8"
    )

    (docs / "day56_improvement_recommendations.md").write_text(
        "# Day 56 – Improvement Recommendations\n\n"
        "1. Validate the pipeline using consented, anonymized real evaluation data.\n"
        "2. Obtain independent recruiter labels before calculating meaningful agreement.\n"
        "3. Measure precision, recall, confusion matrix and per-group error rates "
        "when a sufficiently sized labelled dataset is available.\n"
        "4. Add integration tests for missing stages, invalid inputs and service failures.\n"
        "5. Record stage-level latency and run load tests before production claims.\n"
        "6. Keep human review mandatory for incomplete evidence, risk flags and "
        "final employment decisions.\n"
        "7. Review scoring weights and thresholds only with validated outcome data.\n",
        encoding="utf-8"
    )

    (docs / "day56_simulation_results.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    result = run_simulation()
    write_reports(result)
    print(json.dumps({
        "candidates": result["candidate_count"],
        "execution_seconds": result["execution_seconds"],
        "reference_agreement_percentage": result["reference_agreement_percentage"],
        "reports_created": [
            "docs/day56_end_to_end_ai_test_report.md",
            "docs/day56_system_performance_analysis.md",
            "docs/day56_improvement_recommendations.md",
            "docs/day56_simulation_results.json"
        ]
    }, indent=2))
