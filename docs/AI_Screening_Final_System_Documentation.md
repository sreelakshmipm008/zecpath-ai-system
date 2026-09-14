# AI Screening System - Final System Documentation

## 1. System Overview

The AI Screening System is a structured candidate screening pipeline designed to evaluate candidate responses to role-specific screening questions. The system processes screening responses through speech-to-text, transcript normalization, answer understanding, intent classification, rule-based scoring, error handling, and structured report generation.

The system is designed to support multiple job roles and multilingual screening questions while maintaining explainable and deterministic evaluation logic.

The AI screening pipeline is separate from the ATS eligibility and ranking system. AI screening evaluates the quality and characteristics of candidate screening responses, while the ATS evaluates resume and job-description alignment.

## 2. System Objectives

The main objectives of the AI Screening System are:

- Provide structured role-specific screening questions.
- Support English and Malayalam question variants.
- Convert candidate speech into text.
- Normalize and clean screening transcripts.
- Understand basic characteristics of candidate answers.
- Detect missing, vague, off-topic, and on-topic responses.
- Extract relevant skills, experience, availability, and salary information.
- Score candidate responses using explainable rules.
- Handle audio, language, response, and processing edge cases safely.
- Generate structured screening reports.
- Provide consistent outputs for recruiter review.

## 3. End-to-End Architecture

The current AI screening flow is:

Candidate Audio
    |
    v
Speech-to-Text
    |
    v
Transcript Cleaning and Normalization
    |
    v
Answer Understanding
    |
    v
Intent Classification
    |
    v
Screening Scoring Engine
    |
    v
AI Screening Report Builder
    |
    v
Structured Screening Report

Supporting components include:

- HR screening question bank
- Multilingual question templates
- Screening interaction data structure
- AI error handling and recovery
- Test fixtures and regression tests

## 4. Project Structure

Important AI screening components include:

### answer_understanding/

Contains the answer understanding and intent classification logic.

- `answer_understanding_engine.py`
- `intent_classifier.py`

### stt/

Contains speech-to-text and transcript processing components.

- `speech_to_text.py`
- `transcript_normalizer.py`
- `clean_transcript_processor.py`

### scoring/

Contains screening evaluation and report-generation logic.

- `screening_scoring_engine.py`
- `ai_screening_report_builder.py`

### utils/

Contains shared AI screening error-handling functionality.

- `ai_error_handler.py`

### data/hr_screening/

Contains the screening question datasets and reusable templates.

- `hr_screening_questions.csv`
- `question_templates.json`
- `ai_screening_questions.json`

### data/transcript_architecture/

Contains the structured AI screening transcript data definition.

- `ai_screening_data_structure.json`

### data/ai_screening_reports/

Contains generated screening reports for the supported sample roles.

### tests/

Contains automated tests for the screening and supporting components.

## 5. Screening Question System

The screening question system provides structured questions for supported job roles.

The question dataset contains:

- Role
- Question identifier
- Question category
- English question
- Malayalam question
- Expected answer type
- Mandatory or optional status
- Scoring importance
- Template identifier

Reusable question templates are maintained separately to support consistent question construction.

The AI-ready question dataset provides structured question objects used by the screening report-generation workflow.

## 6. Speech-to-Text Pipeline

The speech-to-text component converts candidate audio responses into text.

The STT implementation supports:

- Speech transcription
- Language handling
- Confidence information
- Audio-related error handling
- Detection and recovery from problematic audio conditions

The system can allow automatic language detection when an explicit language is not supplied.

STT output is passed to the transcript processing stage before answer evaluation.

## 7. Transcript Normalization

Transcript normalization prepares raw speech-to-text output for downstream processing.

The normalization process addresses:

- Text cleanup
- Whitespace normalization
- Case normalization
- Punctuation handling
- Filler-word handling
- Speaker identification
- Timestamp preservation
- Confidence preservation
- Technical terminology
- Missing or unclear speech
- Question association
- Identifier preservation

Normalization is intended to improve consistency without losing important screening information.

## 8. Answer Understanding

The answer understanding engine analyzes each candidate response and produces structured information for screening evaluation.

The system can identify:

- Whether an answer is missing
- Whether an answer is vague
- Whether an answer is off-topic
- Whether an answer is on-topic
- Skills mentioned in the response
- Experience information
- Availability information
- Salary expectations

The implementation uses predefined patterns and rule-based extraction rather than an external large-language-model scoring service.

## 9. Intent Classification

The intent classifier categorizes candidate answers into the following main states:

- `missing`
- `vague`
- `off_topic`
- `on_topic`

The classifier also considers question context when evaluating relevance.

Examples of vague response patterns include statements such as uncertainty, lack of knowledge, or extremely short generic answers.

The purpose of intent classification is to provide a consistent signal to the scoring engine and error-handling workflow.

## 10. Screening Scoring Engine

The screening scoring engine evaluates each answer using four primary parameters:

- Clarity
- Relevance
- Completeness
- Consistency

Each parameter contributes equally to the overall question score.

### Parameter Weight

Each parameter has a weight of:

`0.25`

### Clarity

Clarity considers response length and basic textual characteristics.

Very short responses receive lower scores, while sufficiently detailed responses receive higher scores. Basic punctuation and spacing characteristics are also considered.

### Relevance

Relevance considers the detected intent and relationship between the answer and the screening question.

Missing, vague, and off-topic responses receive lower relevance scores.

### Completeness

Completeness considers response detail and the presence of useful information such as:

- Skills
- Experience
- Availability
- Salary information

### Consistency

Consistency evaluates whether the response contains internally conflicting information, such as contradictory experience or availability statements.

### Overall Question Score

The four parameter scores are combined using equal weighting:

`Overall Question Score = (Clarity + Relevance + Completeness + Consistency) / 4`

The final screening score is calculated from the evaluated screening questions.

## 11. AI Screening Report Generation

The AI screening report builder combines answer understanding and scoring results into a structured candidate report.

Generated reports contain the following major sections:

- `report_title`
- `candidate_information`
- `screening_summary`
- `screening_highlights`
- `screening_evaluation`

The report can include:

- Key answers
- Strengths
- Risks
- Missing data
- Salary expectation
- Availability
- Skill confirmations
- Total questions
- Answered questions
- Final screening score

## 12. Error and Edge-Case Handling

The AI screening system includes dedicated handling for common screening failures.

Supported edge cases include:

### Poor Audio Quality

The system can identify an audio issue and request a retry rather than continuing with unreliable input.

### Language Mixing

The speech-to-text flow can use automatic language detection when language information is not explicitly supplied.

### Missing Answers

Missing responses are identified and can trigger a clarification flow.

### Background Noise

Audio conditions that affect transcription can result in a retry response.

### Retry and Clarification

Temporary problems can be retried while maintaining a controlled recovery flow.

### Unexpected Processing Errors

Unexpected internal errors are handled through a controlled fallback rather than exposing internal exception details to the screening user.

The system also applies retry limits and safe continuation behavior.

## 13. Screening Data Architecture

Screening interaction data connects the candidate, job, question, transcript, timestamp, confidence information, and speaker information.

Core interaction fields include:

| Field | Purpose |
|---|---|
| candidate_id | Identifies the candidate |
| job_id | Identifies the job |
| question_id | Identifies the screening question |
| timestamp | Identifies the transcript timing |
| confidence_level | Stores speech-to-text confidence |
| speaker | Identifies the speaker |
| transcript_text | Stores normalized transcript content |

These fields provide the foundation for structured screening interaction records.

## 14. Generated Screening Reports

The current sample screening workflow generates reports for 10 supported roles:

1. Accountant
2. AWS Cloud Engineer
3. Cyber Security Analyst
4. Data Analyst
5. Digital Marketing Executive
6. HR Executive
7. Python Developer
8. Sales Executive
9. Staff Nurse
10. UI/UX Designer

All 10 generated reports were validated as valid JSON objects.

## 15. Current Validation Results

The sample report generation workflow was executed successfully for all 10 supported roles.

The generated reports were individually validated as valid JSON.

The complete automated regression suite was also executed successfully:

`30 passed`

The transcript normalizer test suite required a fixture-path correction because the referenced audio fixture was located under the actual Day 24 `sample audio` directory.

After the correction, the complete regression suite passed successfully.

## 16. Human-AI Comparison

A separate Human-AI Comparison Report evaluates the AI screening outputs against simulated human reference evaluations.

The comparison uses:

- Candidate answers
- Skills
- Experience
- Location
- Availability
- Overall suitability

The comparison demonstrated that AI screening scores and ATS eligibility decisions evaluate different aspects of a candidate.

The comparison also identified that AI-generated screening summaries may not always expose every skill stated in candidate answers, even when the underlying skill extraction can detect those skills.

## 17. Relationship with the ATS

The AI Screening System and ATS are complementary components.

### ATS

The ATS primarily evaluates:

- Resume information
- Job-description requirements
- Skills
- Experience
- Education
- Semantic similarity
- Candidate ranking
- Eligibility/classification

### AI Screening

AI screening primarily evaluates:

- Candidate screening responses
- Clarity
- Relevance
- Completeness
- Consistency
- Detected skills
- Experience information
- Availability
- Salary expectations
- Screening interaction quality

AI screening scores should therefore not be treated as a replacement for ATS eligibility scoring.

## 18. API Status

The current repository does not contain a production HTTP API implementation such as FastAPI or Flask.

Therefore, the current system should be considered a modular Python processing pipeline rather than a deployed API service.

API design and endpoint planning can be defined separately as an architectural design task without incorrectly representing the current repository as having a live API.

## 19. Known Limitations

The current AI screening implementation is primarily rule-based and deterministic.

Important limitations include:

- Answer understanding relies on predefined patterns.
- Skill extraction relies on a predefined skill vocabulary and matching logic.
- Semantic understanding is limited compared with a full language-model-based evaluator.
- Human-AI comparison uses simulated human reference evaluations.
- No production HTTP API is currently implemented.
- AI screening eligibility should not be confused with ATS eligibility.
- Generated sample reports are demonstration outputs rather than live candidate screening records.

## 20. Testing

The project contains automated tests covering the implemented screening and supporting functionality.

The final regression validation completed successfully with:

`30 passed`

The test suite includes coverage for AI error handling and transcript normalization in addition to the existing project tests.

## 21. Developer Maintenance Guidance

When modifying the AI screening system:

1. Preserve the existing data structures unless a schema change is intentional.
2. Update tests when changing screening logic.
3. Validate transcript processing after STT changes.
4. Validate answer-understanding behavior after modifying intent or extraction rules.
5. Regenerate sample reports after scoring or extraction changes.
6. Validate all generated reports as JSON.
7. Run the complete regression test suite before committing changes.
8. Keep AI screening scoring separate from ATS eligibility logic.
9. Avoid exposing internal processing exceptions to screening users.
10. Document new edge cases and recovery behavior.

## 22. Final System Status

The AI Screening System currently provides a structured and tested screening pipeline covering:

- Role-specific screening questions
- Multilingual question support
- Speech-to-text processing
- Transcript normalization
- Answer understanding
- Intent classification
- Skill and candidate-information extraction
- Explainable screening scoring
- Edge-case and error handling
- Structured report generation
- Automated regression testing

The system has been validated using the available sample screening workflow and is suitable as the current development-stage AI screening implementation.

A production API, deployment layer, and advanced model-based semantic evaluation are not currently part of the implemented repository and should be treated as future extensions rather than existing capabilities.

## 23. Related Documentation

The following documents provide detailed information about individual components:

- `day31_edge_case_handling.md`
- `Screening_System_Human_AI_Comparison_Report.md`
- `STT_Accuracy_Test_Report.md`
- `transcript_normalization_rules.md`
- `screening_interaction_database_schema.md`
- `metadata_standards.md`
- `ATS_Technical_Documentation.md`
- `Developer_Guide.md`

## 24. Conclusion

The AI Screening System provides an end-to-end, structured foundation for candidate screening. Its modular architecture separates speech processing, transcript preparation, answer understanding, scoring, error handling, and report generation.

The current implementation prioritizes deterministic behavior, explainability, structured outputs, and safe handling of screening edge cases. The existing test suite and sample reports provide validation of the implemented functionality, while the documented limitations clearly distinguish the current development-stage system from future production API and advanced AI capabilities.
