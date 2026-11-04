# Day 47 – Technical Skill Scoring Model

## Objective
Develop an explainable technical interview scoring model that evaluates candidate answers across four dimensions and produces skill-wise results.

## Scoring Dimensions

| Dimension | Weight | Evaluation focus |
|---|---:|---|
| Accuracy | 40% | Technical correctness and expected points |
| Explanation Depth | 20% | Completeness and clarity |
| Logical Reasoning | 25% | Reasoning and justified steps |
| Real-World Application | 15% | Practical relevance and examples |

## Scoring Formula

Final Score = (Accuracy × 0.40) + (Explanation Depth × 0.20) + (Logical Reasoning × 0.25) + (Real-World Application × 0.15)

Each dimension is scored from 0 to 100.

## Question-Type Evaluation
- Conceptual: definitions, explanations, relationships, and examples.
- Practical: implementation approach, technical steps, and error handling.
- Scenario: diagnosis, prioritization, solutions, constraints, and validation.

## Difficulty Normalization
Basic, intermediate, and advanced questions use the same 0–100 scoring scale. Difficulty changes the expected depth and complexity, not the numerical scale.

## Assessor Score Bands

| Score | Interpretation |
|---|---|
| 0–39 | Shallow or mostly incorrect |
| 40–69 | Partially correct with limited explanation |
| 70–84 | Mostly accurate with clear explanation |
| 85–100 | Thorough, accurate, and well-reasoned |

## Skill-Wise Breakdown
The engine groups evaluated answers by technical skill domain and calculates the average score for each domain, along with the overall technical score.

## Explainability
Each scoring result includes dimension scores, configured weights, weighted contributions, expected answer points, rubric guidance, performance level, and optional assessor notes.

## Assessment Limitation
The current engine calculates scores from dimension ratings supplied by an assessor. It provides rubric guidance and structured results; it does not independently determine whether a candidate's technical answer is correct.

## Implementation Files
- `config.py`
- `scoring/technical_skill_scoring_engine.py`
- `scoring/technical_rubrics.py`
- `tests/test_technical_skill_scoring_engine.py`
- `data/technical_interview/technical_question_bank.json`
