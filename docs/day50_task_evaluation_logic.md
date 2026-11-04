\# Day 50 – Task Evaluation Logic



\## 1. Objective

Define how the Machine Test AI framework evaluates practical technical tasks using measurable results and structured assessment criteria.



\## 2. Evaluation by Task Type



\### 2.1 Coding Problems

\- Compare program output against expected results.

\- Execute public and hidden test cases.

\- Record passed and failed test cases.

\- Evaluate runtime and memory usage.

\- Review code readability and maintainability.



\### 2.2 Debugging Tasks

\- Check whether the identified defects are corrected.

\- Execute regression tests.

\- Verify that existing functionality is preserved.

\- Evaluate the correctness and quality of the changes.



\### 2.3 File-Based Tasks

\- Validate input-file handling.

\- Check output format and required fields.

\- Compare generated results against expected data.

\- Evaluate missing-value handling and error management.



\### 2.4 Mini System Design

\- Evaluate component selection and architecture.

\- Review data flow and interface definitions.

\- Assess scalability, reliability, and security considerations.

\- Review assumptions and technical trade-offs.



Subjective design criteria should be reviewed by a human assessor, with AI assistance where appropriate.



\## 3. Evaluation Metrics



\### Correctness

Measures whether the submitted solution satisfies the task requirements.



Evidence:

\- Test cases passed.

\- Expected output matches.

\- Required functionality is present.



\### Efficiency

Measures resource usage and solution performance.



Evidence:

\- Execution time.

\- Memory consumption.

\- Algorithmic or query efficiency where measurable.



\### Code Quality

Measures maintainability and implementation quality.



Evidence:

\- Readability and naming.

\- Modularity and organization.

\- Error handling.

\- Appropriate testing practices.



\### Problem-Solving Approach

Measures the quality of the candidate's demonstrated solution process.



Evidence:

\- Task decomposition.

\- Reasonable assumptions.

\- Choice of approach.

\- Explanation of important decisions.

\- Debugging rationale where submitted.



Do not infer problem-solving ability from keystroke patterns or unverified behavioral signals.



\### Time Management

Measures completion relative to the assigned time limit.



Evidence:

\- Task start time.

\- Submission time.

\- Elapsed duration.

\- Completion status at the deadline.



\## 4. Evaluation Pipeline



1\. Load the task definition and evaluation criteria.

2\. Validate the submitted files and required format.

3\. Save the final submission snapshot.

4\. Execute eligible code in an isolated sandbox.

5\. Collect test results and execution measurements.

6\. Evaluate code quality and problem-solving evidence.

7\. Calculate the metric-wise scores.

8\. Apply the scoring model.

9\. Generate a report with scores and supporting evidence.



\## 5. Input and Output Records



\### Input Records

\- Task ID and task version.

\- Candidate submission reference.

\- Submitted files and source code.

\- Submission timestamps.

\- Evaluation configuration.



\### Output Records

\- Test-case results.

\- Execution status and runtime.

\- Error and validation details.

\- Metric-wise scores.

\- Final weighted score.

\- Reviewer comments where applicable.



\## 6. Failure Handling



\- Invalid submissions should receive clear validation feedback.

\- Execution timeouts should be recorded separately from ordinary test failures.

\- Sandbox or platform failures should not automatically be treated as candidate errors.

\- Missing evaluation evidence should be marked unavailable rather than assigned an invented score.

\- Subjective assessments should be escalated for human review.



\## 7. Fairness and Reliability



\- Use consistent task instructions and test cases.

\- Apply equivalent execution limits to candidates.

\- Document language and environment restrictions.

\- Support approved accommodations.

\- Use deterministic test cases where possible.

\- Keep performance scores separate from integrity flags.



\## 8. Implementation Status



This document specifies proposed evaluation logic. Actual sandbox execution, automated capture, and production evaluation are not claimed to exist unless separately implemented and tested.

