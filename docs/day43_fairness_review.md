# Day 43 — AI Scoring Fairness Review

## 1. Objective

Review candidate scoring logic for potential unfair effects caused by demographic attributes or communication-style proxies.

## 2. Demographic signal inspection

A text search was performed across the scoring source files for common demographic attributes, including gender, age, race, religion, caste, ethnicity, nationality, date of birth, and marital status.

No obvious direct demographic fields were identified in the searched scoring source files. This search is limited in scope and does not prove that demographic data is absent from the entire system.

## 3. Risks identified

The original communication scoring logic used:
- Average sentence length and sentence fragmentation.
- A fixed list of detectable grammar patterns.
- Lexical diversity as a vocabulary measure.
- Sentence length and response length as clarity indicators.
- Sentence count and transition words as structure indicators.
- Filler-word frequency as a communication-quality indicator. The current implementation still detects and reports filler words, but returns a neutral score of 70 for non-empty answers.

These features may reflect language background, disability, neurodiversity, speech patterns, or response style rather than job-related ability. Their actual impact on different candidate groups has not been measured.

## 4. Changes implemented

The following communication-scoring components were changed to use neutral interim values for non-empty answers:
- Fluency: 75
- Vocabulary range: 70
- Clarity: 70
- Answer structure: 70

Empty or missing answers continue to return zero for these components.

The component weights were adjusted to:
- Fluency: 10%
- Grammar quality: 10%
- Vocabulary range: 5%
- Clarity: 25%
- Filler words: 5%
- Answer structure: 45%

The weights total 100%. These weights and neutral values are provisional engineering choices, not empirically validated fairness settings.

## 5. Validation performed

The following tests passed after the changes:

Targeted validation: `python -m pytest tests/test_communication_scorer_fairness.py tests/test_hr_interview_scoring_engine.py -q` (18 passed); privacy and interview validation: `python -m pytest tests/test_interview_state_privacy.py tests/test_interview_engine.py tests/test_follow_up_engine.py -q` (30 passed); full suite: `python -m pytest -q` (115 passed).

The targeted scorer and HR scoring tests passed (18 passed in the latest targeted run). The privacy and interview tests passed (30 passed). The complete test suite passed (115 passed).

These tests verify basic scorer behavior and compatibility with selected HR interview components. They do not establish statistical fairness, legal compliance, or absence of disparate impact.

## 6. Remaining limitations and actions

1. The neutral values reduce the contribution of four unvalidated style-based components but also reduce the information available from those components.
2. Grammar scoring still influences the final communication score and requires further review. Filler-word detection remains available for analysis, but its constant score of 70 for non-empty answers does not distinguish candidates.
3. Review the role-specific necessity and job relevance of each scoring feature.
4. Evaluate scores across appropriate, lawfully collected and protected test groups where permitted, with suitable privacy safeguards and sufficient sample sizes.
5. Review scoring outcomes with qualified human reviewers and preserve documented reasons for hiring decisions.
6. Consent enforcement, consent withdrawal, and configurable in-memory retention cleanup have been implemented and tested. Integrate cleanup with the actual storage layer and verify deletion across persisted records, reports, logs, and backups.
7. Treat this review as an engineering assessment, not a legal compliance certification.

## 7. Conclusion

The review identified potential fairness risks and introduced provisional mitigations to reduce reliance on sentence style, vocabulary diversity, response length, and transition-word use. Further validation, review of remaining scoring features, and privacy-control implementation are required before claiming production readiness.
