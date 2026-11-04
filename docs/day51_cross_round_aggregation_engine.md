# Day 51 – Cross-Round Aggregation Engine

## 1. Objective

Develop a unified scoring capability that combines evaluation results from five hiring stages into a transparent candidate hiring-fit score.

The five stages are:
- ATS
- Screening
- HR Interview
- Technical Interview
- Machine Test

## 2. Existing System Compatibility

The existing three-stage scoring API is preserved:
- calculate_hiring_fit()
- build_candidate_score()

The new five-stage functionality is provided separately through:
- calculate_five_stage_hiring_fit()
- build_full_candidate_score()

This maintains compatibility with existing modules and tests.

## 3. Five-Stage Weight Configuration

The implementation uses configurable default weights:

| Evaluation Stage | Default Weight |
|---|---:|
| ATS | 20% |
| Screening | 20% |
| HR Interview | 20% |
| Technical Interview | 20% |
| Machine Test | 20% |

These are provisional implementation defaults. They are not company-prescribed, empirically validated, or approved hiring criteria. Role-specific five-stage weight configurations can be supplied through five_stage_role_weights.

## 4. Hiring-Fit Calculation

Each available stage contributes to the final score according to its configured weight.

The engine:
1. Validates each supplied score.
2. Identifies unavailable stages.
3. Retrieves the applicable role weights.
4. Normalizes weights across available stages.
5. Calculates weighted contributions.
6. Produces the hiring-fit percentage.

The resulting calculation is transparent because the output includes the original scores, configured weights, applied weights, and weighted contributions.

## 5. Missing-Score Handling

A missing score is represented by None and is not treated as zero.

The engine:
- Excludes unavailable stages from the calculation.
- Normalizes the weights of available stages.
- Lists missing stages in the result.
- Sets evidence_complete to false when one or more stages are missing.
- Sets human_review_required to true when evidence is incomplete.

A score of zero remains a valid score and is not confused with missing evidence.

## 6. Unified Candidate Score Object

The five-stage candidate score object contains:
- Candidate ID
- Candidate name
- Job role
- Scores from all five stages
- Configured weights
- Applied normalized weights
- Weighted contributions
- Available stages
- Missing stages
- Evidence completeness
- Human-review requirement
- Hiring-fit percentage

## 7. Machine Test Integration Boundary

The aggregation engine accepts a separately supplied Machine Test score. It does not implement task execution, sandboxing, monitoring, or automatic Machine Test evaluation.

This preserves the Day 50 design boundary between the Machine Test framework and the other evaluation stages.

## 8. Validation and Testing

The existing three-stage tests were preserved.

Additional tests cover:
- Five-stage calculation.
- Missing-score handling.
- Zero as a valid score.
- Weight normalization.
- Invalid score rejection.
- Boolean score rejection.
- Empty input rejection.
- Custom role-based weights.
- Full candidate score object.

Test results:
- Original unified scoring tests: 12 passed.
- Unified scoring tests after extension: 21 passed.
- Complete repository test suite: 182 passed.

## 9. Limitations and Governance

The configured five-stage weights are provisional and require validation before operational hiring use.

The hiring-fit percentage is decision-support information. It must not independently determine employment outcomes.

Incomplete evidence requires human review. Machine Test results must be supplied by a separately implemented and verified evaluation process.

## 10. Conclusion

Day 51 extends the existing unified scoring engine to support five evaluation stages while preserving its original three-stage API.

The implementation provides configurable weighting, missing-score handling, transparent contributions, candidate score objects, and explicit human-review indicators.

