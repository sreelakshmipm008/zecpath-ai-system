# Day 59 – Zecpath AI Integration Document

## 1. Objective

This document explains how the existing Zecpath AI modules can connect with backend services, databases and external systems.

**Status:** This is a proposed integration design. The repository contains Python modules, but the HTTP API is not yet deployed.

## 2. Main AI Modules

| Module | Existing files | Responsibility |
|---|---|---|
| Resume Parsing | parsers/ | Extract structured information from resumes |
| ATS Scoring | scoring/ats_score.py | Calculate candidate-job matching scores |
| Screening AI | scoring/screening_scoring_engine.py | Evaluate candidate answers |
| Interview AI | interview_ai/ | Manage interview sessions and responses |
| Decision AI | scoring/final_recommendation_engine.py | Generate explainable hiring recommendations |

## 3. Proposed Integration Flow

1. Candidate submits a resume or interview response.
2. Backend receives and validates the request.
3. Backend sends the data to the appropriate AI module.
4. AI module processes the information.
5. Results are returned to the backend.
6. Backend stores permitted results in the database.
7. Recruiter or candidate receives the appropriate response.

## 4. Integration Details

### A. Resume Parsing

- Receive the candidate's resume.
- Validate the uploaded file.
- Extract relevant information using resume parsing modules.
- Return a structured candidate profile.

Note: The exact parser output must be confirmed before implementing the API.

### B. ATS Scoring

The existing ATSScorer uses:

- Skill score
- Experience score
- Education score
- Semantic score

It calculates an overall ATS score and provides an explainable breakdown.

### C. Screening AI

The screening scoring engine evaluates:

- Answer clarity
- Answer relevance
- Completeness
- Consistency

It returns question-level scores and a final screening score.

### D. Interview AI

The interview modules manage:

- Interview sessions
- Interview phases
- Candidate responses
- Consent management
- Response retention

### E. Decision AI

The FinalRecommendationEngine evaluates candidate scores, eligibility, HR summaries and other evidence.

It generates a recommendation with reasons and review items. The final hiring decision remains with the human recruiter.

## 5. Backend and Database Integration

The proposed backend should manage:

- Candidate information
- Job information
- Resume profiles
- ATS scores
- Screening results
- Interview sessions
- Decision recommendations

The existing screening interaction schema contains candidate ID, job ID, question ID, timestamp, speaker, transcript text and speech-to-text confidence.

These are proposed logical data records, not confirmation of a deployed database.

## 6. API Processing Approach

| Operation | Proposed processing |
|---|---|
| Resume upload | Asynchronous |
| ATS scoring | After required scores are available |
| Text answer evaluation | Synchronous |
| Audio transcription | Asynchronous |
| Interview phase update | Synchronous |
| Final recommendation | After evaluation evidence is available |

## 7. Security Requirements

- Use HTTPS.
- Authenticate API requests.
- Apply role-based access control.
- Validate uploaded files and request data.
- Protect candidate information.
- Store credentials securely.
- Obtain consent before recording interview responses.
- Apply data retention and deletion policies.
- Avoid exposing internal errors.

## 8. Error Handling

The proposed API should handle:

- Invalid requests
- Missing candidate information
- Unsupported file formats
- Audio processing failures
- Invalid interview transitions
- Missing evaluation data
- Temporary service failures

Use controlled error responses and retry only temporary failures.

## 9. External Integrations

Potential integrations include:

- Candidate and recruiter applications
- Database services
- File storage
- Speech-to-text services
- Notification services

These are proposed integrations, not confirmed active connections.

## 10. Implementation Roadmap

1. Finalize API request and response formats.
2. Develop backend API endpoints.
3. Integrate resume parsing.
4. Connect ATS and screening modules.
5. Integrate interview management.
6. Connect the decision recommendation engine.
7. Add database persistence, security and testing.

## 11. Conclusion

The existing Zecpath AI repository provides Python modules for resume processing, scoring, screening, interview management and decision support. This document proposes how these modules can be connected through a backend API architecture.
