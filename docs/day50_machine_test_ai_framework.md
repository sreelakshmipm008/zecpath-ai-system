\# Day 50 – Machine Test AI Framework



\## 1. Objective

Design a framework for evaluating candidates through practical, real-world technical tasks rather than interview answers alone.



\## 2. Machine Test Categories



\### 2.1 Coding Problems

Candidates write code to solve defined programming problems. Evaluation considers correctness, execution results, efficiency, and code quality.



\### 2.2 Debugging Tasks

Candidates inspect faulty code, identify defects, implement corrections, and verify the solution using regression tests.



\### 2.3 File-Based Tasks

Candidates process supplied files such as CSV, JSON, or text files and generate outputs that satisfy specified requirements.



\### 2.4 Mini System Design

Candidates prepare a small technical design containing components, data flow, interfaces, assumptions, and relevant trade-offs. Subjective evaluation requires human review.



\## 3. Framework Architecture



1\. Task Definition Layer – stores task instructions, requirements, difficulty, allowed languages, test cases, and time limits.

2\. Submission Layer – receives candidate files, code, and design artifacts.

3\. Snapshot Layer – records explicit submission checkpoints and final submission versions.

4\. Execution Layer – runs executable submissions in an isolated sandbox with defined resource limits.

5\. Evaluation Layer – evaluates correctness, efficiency, code quality, and problem-solving evidence.

6\. Time Management Layer – records task start, submission, elapsed time, and deadline status.

7\. Scoring Layer – calculates weighted scores and produces a metric breakdown.

8\. Reporting Layer – generates an evaluation report for authorized reviewers.



\## 4. Input Capture



Capture only information required for assessment:



\- Candidate and task reference IDs.

\- Task instructions and task version.

\- Submitted source files and final submission.

\- Explicit code snapshots at submission checkpoints.

\- Execution results, test outcomes, and error output.

\- Submission timestamps and elapsed duration.



Avoid unnecessary keystroke surveillance and unrelated personal or device information.



\## 5. Output Capture



The system should retain:



\- Submission version and file references.

\- Test cases passed and failed.

\- Execution status and runtime.

\- Relevant error messages.

\- Resource usage where available.

\- Metric-wise scores and evaluation evidence.



\## 6. Security and Fairness



\- Execute untrusted code only in an isolated sandbox.

\- Apply CPU, memory, file-system, and execution-time limits.

\- Prevent access to host secrets and unrelated files.

\- Use consistent task versions and evaluation conditions.

\- Account for platform failures and approved accommodations.

\- Require human review for subjective system-design assessments.

\- Keep integrity flags separate from performance scores.



\## 7. Integration Boundaries



The machine-test framework is separate from the existing technical interview scoring engine, HR scoring, and ATS scoring. Results may be presented together in a broader candidate assessment report, but their scores must remain distinguishable.



\## 8. Implementation Status



This document defines the proposed framework. It does not claim that sandbox execution, monitoring, or machine-test capture has already been implemented in the repository.

