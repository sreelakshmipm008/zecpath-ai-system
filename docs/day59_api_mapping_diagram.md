# Day 59 – Zecpath AI API Mapping Diagram

## 1. Purpose

This document presents the proposed API integration between the five major AI modules and backend services.

**Status:** Proposed architecture. These API connections are not yet deployed.

## 2. Overall API Mapping

```mermaid
flowchart TD
    A[Candidate / Recruiter] --> B[Backend API]
    B --> C[Resume Parsing API]
    C --> D[Structured Candidate Profile]
    D --> E[ATS Scoring API]
    E --> F[ATS Score and Breakdown]
    F --> G[Screening AI API]
    G --> H[Screening Results]
    H --> I[Interview AI API]
    I --> J[Interview Session and Responses]
    J --> K[Decision AI API]
    K --> L[Recommendation and Review Items]
    D --> M[(Database)]
    F --> M
    H --> M
    J --> M
    L --> M
    L --> N[Recruiter Review]


**Line 2:** Close the text and save the file:

```powershell

## 3. Module-to-Backend Mapping

| Module | Proposed endpoint | Main input | Main output |
|---|---|---|---|
| Resume Parsing | POST /api/v1/resumes/parse | Resume file | Candidate profile |
| ATS Scoring | POST /api/v1/ats/score | Candidate and job data | ATS score breakdown |
| Screening AI | POST /api/v1/screening/evaluate | Questions and answers | Screening scores |
| Interview AI | POST /api/v1/interviews | Candidate and interview details | Interview session |
| Decision AI | POST /api/v1/decisions/recommend | Evaluation evidence | Recommendation |

**Note:** These endpoint paths are proposed mappings, not existing deployed endpoints.

## 4. Integration Responsibilities

- **Backend:** Request routing, authentication, validation and coordination.
- **Resume Parsing:** Resume information extraction.
- **ATS Scoring:** Candidate-job matching evaluation.
- **Screening AI:** Candidate answer evaluation.
- **Interview AI:** Interview session and response management.
- **Decision AI:** Evidence-based recommendation generation.
- **Database:** Storage of permitted records.


## 5. Request Processing Sequence

1. Candidate submits a resume through the application.
2. Backend sends the resume for parsing.
3. The candidate profile is passed to ATS scoring.
4. Screening AI evaluates candidate answers.
5. Interview AI manages the interview session.
6. Decision AI generates a recommendation using available evaluation evidence.
7. Backend stores permitted results and makes them available for recruiter review.

## 6. Important Design Considerations

- Validate every API request.
- Use consistent candidate and job identifiers.
- Handle module failures without exposing internal errors.
- Protect candidate information.
- Maintain interview consent and retention requirements.
- Keep final hiring authority with the human recruiter.

## 7. Conclusion

The proposed mapping connects the five AI modules through a central backend API. It provides a structured integration plan while keeping the current Python modules separate from future deployed API services.

