\# Day 50 – Real-World Task Scoring Model



\## 1. Objective

Define a weighted scoring model for assessing candidates' performance in practical machine tests.



The model evaluates correctness, efficiency, code quality, problem-solving approach, and time management.



\## 2. Proposed Scoring Weights



| Evaluation Metric | Weight |

|---|---:|

| Correctness | 40% |

| Efficiency | 20% |

| Code Quality | 15% |

| Problem-Solving Approach | 15% |

| Time Management | 10% |

| Total | 100% |



These are proposed design weights, not experimentally validated production thresholds.



\## 3. Metric Definitions



\### 3.1 Correctness – 40%

Measures whether the solution meets the task requirements.



Evidence:

\- Passed test cases.

\- Expected output validation.

\- Required functionality.



Proposed calculation:



Correctness Score = (Passed Test Cases / Total Valid Test Cases) × 100



If test cases cannot run because of a platform failure, correctness should be marked unavailable until evaluation can be repeated.



\### 3.2 Efficiency – 20%

Measures execution and resource efficiency.



Evidence:

\- Runtime.

\- Memory consumption.

\- Algorithmic complexity.

\- Database or file-processing efficiency where applicable.



Scores should use task-specific performance thresholds and consistent execution limits.



\### 3.3 Code Quality – 15%

Measures maintainability and implementation quality.



Assessment criteria:

\- Readability.

\- Naming conventions.

\- Modular structure.

\- Error handling.

\- Testing practices.



Use a documented rubric with consistent scoring levels.



\### 3.4 Problem-Solving Approach – 15%

Measures the candidate's demonstrated reasoning and solution approach.



Assessment criteria:

\- Problem decomposition.

\- Identification of requirements.

\- Selection of an appropriate solution.

\- Handling of edge cases.

\- Explanation of technical decisions.



Use submitted explanations, design artifacts, and documented solution evidence. Do not treat keystroke monitoring as proof of reasoning ability.



\### 3.5 Time Management – 10%

Measures task completion against the assigned time limit.



Evidence:

\- Task start timestamp.

\- Submission timestamp.

\- Elapsed time.

\- Deadline status.



Proposed scoring approach:

\- Full time-management score when completed within the target time.

\- Gradually reduce the score between the target time and the deadline.

\- Zero time-management points when submitted after the deadline, subject to documented exceptions.

\- Do not penalize candidates for verified platform or infrastructure failures.



The target time and deadline must be configured for each task.



\## 4. Final Score Calculation



For a task with all five metrics available:



Final Score =

(Correctness × 0.40) +

(Efficiency × 0.20) +

(Code Quality × 0.15) +

(Problem-Solving Approach × 0.15) +

(Time Management × 0.10)



Each metric is scored from 0 to 100.



Example:



| Metric | Score | Weight | Weighted Score |

|---|---:|---:|---:|

| Correctness | 90 | 0.40 | 36.0 |

| Efficiency | 80 | 0.20 | 16.0 |

| Code Quality | 85 | 0.15 | 12.75 |

| Problem-Solving | 80 | 0.15 | 12.0 |

| Time Management | 90 | 0.10 | 9.0 |

| Total | | | 85.75 |



Example final score: 85.75/100.



This example illustrates the formula; it is not a real candidate result.



\## 5. Missing Metric Handling



\- Do not silently assign zero when a metric cannot be measured.

\- Mark unavailable metrics as N/A and record the reason.

\- If the final score must be calculated, normalize the available metric weights to their remaining total.

\- If essential evidence is missing, mark the assessment incomplete and request review.



\## 6. Score Interpretation



| Score Range | Proposed Interpretation |

|---|---|

| 85–100 | Strong performance |

| 70–84 | Good performance |

| 50–69 | Needs improvement |

| Below 50 | Limited task performance |



These ranges are provisional and should be validated against real assessment data before production use.



\## 7. Scoring Safeguards



\- Use the same evaluation criteria for equivalent tasks.

\- Apply consistent sandbox resource limits.

\- Keep test results and subjective rubric assessments distinguishable.

\- Require human review for subjective system-design scoring.

\- Record the evidence supporting each metric.

\- Keep integrity or malpractice flags separate from performance scores.

\- Do not use the score as the sole basis for an employment decision.



\## 8. Integration with Zecpath AI



The machine-test score should remain a separate assessment component.



It may be presented alongside:

\- Technical interview score.

\- Behavioral assessment.

\- HR assessment.

\- Other authorized evaluation results.



Do not directly modify existing ATS, HR, or technical interview scoring weights.



\## 9. Implementation Status



This document defines a proposed scoring model. The weights, score bands, and evaluation thresholds require validation before production deployment. This document does not claim that a machine-test scoring engine has been implemented.

