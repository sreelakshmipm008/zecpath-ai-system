# Day 49 - Integrity Detection Framework

## 1. Objective

Design a transparent, privacy-conscious framework to identify and review potentially unusual events during online interviews.

The framework covers:
- Tab switching frequency.
- Loss of screen or browser focus.
- Possible external voice events.
- Repeated observable gaze-direction changes.
- Event patterns that may require human review.

This is a research and design deliverable. It does not represent an implemented browser-monitoring, microphone-monitoring, or visual-detection system.

## 2. Design Principles

1. Record observable events rather than making assumptions about intent.
2. Require separate, informed consent for each optional monitoring capability.
3. Provide a meaningful alternative when monitoring is declined.
4. Treat technical interruptions separately from potentially concerning events.
5. Use configurable thresholds and explainable rules.
6. Never automatically accuse, reject, rank, or penalize a candidate.
7. Keep integrity observations separate from HR and technical scoring.
8. Collect only necessary event metadata.
9. Provide human review and an opportunity for the candidate to explain an event.

## 3. Integrity Signal Categories

| Signal | Observable event | Required interpretation boundary |
|---|---|---|
| Tab switching | Browser visibility changes or permitted tab-change events | Does not prove external assistance |
| Screen focus loss | Window loses focus and later regains focus | May result from notifications or operating-system activity |
| External voice | Possible additional voice detected in permitted audio input | Does not establish who spoke or why |
| Looking away | Repeated changes in estimated gaze direction | Does not prove reading, cheating, or distraction |
| Repeated event patterns | Multiple events within a configured time window | Requires contextual human review |

## 4. Proposed Architecture

The proposed framework contains six stages:

1. Consent and monitoring authorization.
2. Event collection through permitted sources.
3. Event validation and normalization.
4. Threshold and pattern analysis.
5. Explainable risk flag generation.
6. Human review and documented resolution.

### 4.1 Consent and Authorization

Before monitoring begins, the candidate must receive a clear explanation of:
- Which signals may be collected.
- Why each signal is collected.
- How events are processed.
- Who can access the results.
- How long event metadata is retained.
- How consent can be withdrawn.

Consent to record interview answers must not automatically authorize browser, microphone, or camera monitoring.

### 4.2 Event Collection

Each permitted event should include:
- Session reference.
- Event type.
- Event timestamp.
- Event duration, where applicable.
- Collection source.
- Technical quality or validation status.
- Monitoring consent reference.

Raw audio and video should not be retained by default.

### 4.3 Event Validation

The system should reject malformed events, validate timestamps, identify duplicate events, and distinguish missing data from a confirmed absence of an event.

Technical failures must be recorded separately from candidate-related observations.

### 4.4 Analysis

The analysis layer should apply configurable thresholds and event-pattern rules.

A single event must not automatically produce a misconduct conclusion. Repeated events may create a review flag, but the flag must retain its underlying evidence and limitations.

### 4.5 Reporting

Reports should include:
- Session reference.
- Monitoring consent status.
- Event type and timestamp.
- Event count and duration.
- Triggered rule and configured threshold.
- Technical limitations.
- Risk-review priority.
- Human reviewer notes.
- Final review status.

## 5. Integration with Day 48

Day 48 defines optional visual observations such as gaze variation, head movement, facial landmark availability, and gesture frequency.

Day 49 may reference permitted visual observation events as separate evidence.

However:
- Gaze variation must not be interpreted as dishonesty.
- Looking away must not automatically trigger a misconduct conclusion.
- Missing visual observations must not create a negative flag.
- Visual observations must not be combined into a candidate suitability score.

## 6. Integration with Existing Zecpath AI

Existing components reviewed:
- `interview_ai/interview_state.py`
- `scoring/behavioral_indicators_report.py`
- `scoring/hr_interview_summary_generator.py`

The existing interview state supports consent for response recording and response-retention controls.

Additional monitoring consent must be designed separately. Existing HR `risk_flags` describe interview-evaluation findings and must not be reused as integrity alerts.

The proposed integrity framework must remain independent of:
- HR interview scores.
- Technical skill scores.
- Communication scores.
- Candidate ranking and hiring recommendations.

No existing scoring engine should be modified as part of this design.

## 7. Privacy and Accessibility

The design must provide:
- Purpose limitation.
- Data minimization.
- Access restrictions.
- Defined retention and deletion procedures.
- Consent withdrawal handling.
- An accessible non-monitoring alternative.
- Consideration of assistive technologies and device limitations.
- Review of false positives and technical interruptions.

Persistent deletion from databases, logs, and backups must be verified before any future production deployment.

## 8. Human Oversight

Every integrity flag is a request for review, not a verdict.

The reviewer must:
1. Examine the original event evidence.
2. Check technical and environmental explanations.
3. Consider the candidate's explanation.
4. Determine whether the event is relevant.
5. Record the review outcome.
6. Avoid unsupported conclusions.

The candidate must not be automatically disqualified based on an event count or risk level.

## 9. Validation Requirements

Before implementation, the proposed framework requires:
- Event-detection accuracy testing.
- False-positive and false-negative evaluation.
- Device and browser compatibility testing.
- Audio-event reliability assessment.
- Accessibility testing.
- Consent and withdrawal testing.
- Security and retention verification.
- Human-review workflow testing.

No production accuracy or fairness claim is made.

## 10. Current Implementation Status

The inspected repository contains existing interview-state privacy controls and behavioral reporting.

No dedicated browser tab-monitoring, screen-focus monitoring, external voice detection, or integrity risk engine was identified during the Day 49 repository inspection.

This document describes a proposed framework only.

## 11. Conclusion

The Integrity Detection Framework provides a structured approach to observing and reviewing potentially unusual interview events. It emphasizes consent, evidence, explainability, technical validation, accessibility, and human oversight. It does not equate unusual behavior with cheating or make automated employment decisions.
