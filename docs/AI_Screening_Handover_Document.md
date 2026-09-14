
# AI Screening System - Handover Document

## 1. System Purpose

The AI Screening System evaluates candidate responses to role-specific screening questions and produces structured screening reports.

## 2. Processing Pipeline

Speech-to-Text
? Transcript Normalization
? Answer Understanding
? Intent Classification
? Screening Scoring
? AI Screening Report

## 3. Core Implementation Modules

- `stt/speech_to_text.py` - Speech-to-text processing.
- `stt/transcript_normalizer.py` - Transcript normalization.
- `answer_understanding/answer_understanding_engine.py` - Extracts and understands candidate answer information.
- `answer_understanding/intent_classifier.py` - Classifies answer intent and handles vague/off-topic responses.
- `scoring/screening_scoring_engine.py` - Calculates deterministic screening scores.
- `scoring/ai_screening_report_builder.py` - Generates structured screening reports.
- `utils/ai_error_handler.py` - Provides controlled AI screening error handling.

## 4. Data and Reports

Role-specific screening questions are stored under:

`data/hr_screening/`

Generated AI screening reports are stored under:

`data/ai_screening_reports/`

The current demo generates reports for 10 job roles.

## 5. Testing and Validation

The AI screening system has been validated through the existing automated test suite and end-to-end report generation.

The current generated reports were validated as valid JSON and contain screening evaluation scores.

## 6. API Status

The repository does not currently contain a deployed HTTP API.

The proposed API architecture is documented separately in:

`docs/AI_Screening_API_Design.md`

## 7. Important Architecture Boundary

The AI Screening System and ATS system are separate components.

AI Screening evaluates candidate screening responses.

ATS evaluates resume and job-description alignment, eligibility, and ranking.

## 8. Developer Handover Notes

Before modifying the screening pipeline:

1. Review the final system documentation.
2. Review the relevant module before making changes.
3. Run the existing tests after modifications.
4. Regenerate sample reports when report-generation logic changes.
5. Validate generated JSON reports.
6. Keep AI screening scoring deterministic and explainable unless the architecture is intentionally changed.

Related documentation:

- `docs/AI_Screening_Final_System_Documentation.md`
- `docs/AI_Screening_API_Design.md`
- `docs/day31_edge_case_handling.md`
