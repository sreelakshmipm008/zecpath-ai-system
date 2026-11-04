# Day 51 – Cross-Round Aggregation Engine

## Objective
Combine all evaluation stages into a unified hiring intelligence score.

## Deliverables

### 1. Hiring Fit Calculator
Calculates a candidate's Hiring Fit Score (%) by combining evaluation scores from:
- ATS
- Screening
- HR Interview
- Technical Interview
- Machine Test

Implementation:
`scoring/unified_scoring_engine.py`

### 2. Cross-Round Aggregation Engine
Aggregates evaluation scores across all five hiring stages using configurable role-based weights.

Features:
- Five-stage score aggregation.
- Role-based weighting.
- Score normalization across available stages.
- Missing-stage detection.
- Evidence completeness tracking.

Implementation:
`scoring/unified_scoring_engine.py`

### 3. Unified Candidate Score Object
Creates a structured candidate score object containing:
- Candidate information.
- Individual evaluation-stage scores.
- Unified hiring fit score.
- Applied weights.
- Missing evaluation stages.
- Evidence completeness information.
- Human review requirement.

Implementation:
`scoring/unified_scoring_engine.py`

## Test File
`tests/test_unified_scoring_engine.py`

## Technical Documentation
`docs/day51_cross_round_aggregation_engine.md`

## Validation
The full project test suite passed with 182 tests after Day 51 implementation.
