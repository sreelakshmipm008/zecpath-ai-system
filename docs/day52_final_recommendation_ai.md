# Day 52 – Final Recommendation AI

## 1. Objective

Develop an explainable recommendation engine that combines candidate evaluation scores, eligibility findings, HR interview risks, and integrity review items to produce one of three recommendation categories:

- Selected
- Hold / Review
- Rejected

The engine is a decision-support component. It does not make the final employment decision.

## 2. Implementation

Main implementation:

`scoring/final_recommendation_engine.py`

Tests:

`tests/test_final_recommendation_engine.py`

The engine is implemented as `FinalRecommendationEngine`.

Its main method is:

`generate_recommendation(candidate_score, eligibility_result, hr_summary=None, behavioral_report=None, integrity_alerts=None)`

It accepts the unified candidate score, eligibility result, optional HR summary, optional behavioral observations, and optional integrity alerts.

## 3. Recommendation categories

### Selected

A candidate receives the Selected recommendation when:

- The unified candidate score meets the configured selected threshold.
- All five evaluation stages have scores.
- The unified score reports complete evidence.
- Eligibility is marked Eligible.
- There are no unresolved HR risk flags.
- There are no unresolved integrity alerts.

The default selected threshold is 80.

### Hold / Review

The engine uses Hold / Review when:

- The candidate score or eligibility evaluation is unavailable.
- One or more evaluation stages are missing.
- Eligibility is marked Review.
- HR risk flags require recruiter attention.
- Integrity alerts require separate investigation.
- The score falls between the configured thresholds.
- The available evidence does not meet the Selected or Rejected recommendation rules.

Unresolved HR risk findings or integrity alerts take priority over an eligibility rejection recommendation. Such cases remain Hold / Review.

### Rejected

The engine can return a Rejected recommendation when:

- Eligibility evaluation returns Rejected; or
- The score is below the configured rejection threshold, evidence is complete, eligibility is Eligible, and there are no unresolved HR risk flags or integrity alerts.

The default rejection threshold is 60.

A Rejected recommendation is not a final employment decision. The recruiter remains responsible for reviewing the evidence.

## 4. Evidence completeness indicator

The engine calculates an evidence-completeness indicator using:

- Five evaluation stages: ATS, Screening, HR Interview, Technical Interview, and Machine Test.
- Eligibility evaluation availability.

The five stages contribute up to 80 points in total. An available eligibility evaluation contributes 20 points.

The indicator ranges from 0 to 100 and is labelled:

- Complete
- Partial
- Insufficient

This value measures evidence coverage only. It is not a statistical probability that the recommendation is correct and is not a calibrated prediction confidence.

## 5. Explainability and output

The recommendation output includes:

- Candidate ID, name, and job role when available.
- Recommendation category.
- Unified candidate score.
- Eligibility status and findings.
- Evidence-completeness indicator.
- Available and missing evaluation stages.
- Reasons supporting the recommendation.
- HR risk findings.
- Integrity review items.
- Behavioral observations.
- Review items for the recruiter.
- Human recruiter as the final decision authority.

## 6. Risk and governance safeguards

- Every recommendation sets `review_required` to True.
- The final decision authority is identified as Human recruiter.
- Behavioral observations are retained as informational context and do not independently determine candidate suitability.
- HR interview risk findings and integrity alerts are kept separate.
- Integrity alerts are not treated as proof of misconduct.
- Unresolved HR or integrity findings require review rather than automatic selection or rejection.
- Missing evaluation evidence is not silently treated as a zero score.
- Existing ranking and eligibility APIs are not replaced by this new recommendation component.
- Default thresholds are configurable implementation defaults, not validated or company-approved hiring standards.

## 7. Validation and tests

Test file:

`tests/test_final_recommendation_engine.py`

The dedicated test suite covers:

1. Selected recommendation for a complete eligible candidate.
2. Hold / Review for missing evaluation evidence.
3. Hold / Review for eligibility requiring review.
4. Rejected eligibility result with recruiter review required.
5. HR risk flags requiring review.
6. Integrity alerts requiring separate review.
7. Behavioral observations not independently changing the recommendation.
8. Evidence-completeness indicator meaning.
9. Invalid score handling.
10. Invalid threshold handling.
11. Unresolved risks taking priority over rejection.

Recorded test results:

- Dedicated Day 52 tests: 11 passed.
- Full project test suite after the final safety refinement: 193 passed in 16.80 seconds.

These are repository test results, not evidence of production hiring accuracy or fairness.

## 8. Limitations

- Recommendation thresholds have not been statistically validated.
- Evidence completeness does not establish recommendation correctness.
- No production accuracy, fairness, or bias-reduction improvement is claimed.
- Integrity alerts require a separate evidence review process.
- The component does not replace recruiter judgment or the organization's hiring policies.

## 9. Day 52 outcome

The Final Recommendation AI component was added with explainable recommendation categories, evidence-completeness reporting, risk-aware review handling, and explicit human decision authority.

The implementation passed all 11 dedicated tests and the full project suite of 193 tests.
