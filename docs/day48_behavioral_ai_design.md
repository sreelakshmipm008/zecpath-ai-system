# Day 48 - Behavioral AI Design Document

## 1. Objective

Research and design a privacy-conscious framework for documenting observable behavioral signals during interview sessions.

The proposed framework considers eye movement, gaze direction, head movement, facial engagement, visible gestures, and camera-based observation quality.

This document describes a design proposal. It does not claim that visual behavioral analysis is currently implemented in Zecpath AI.

## 2. Research Scope

The research covers:

- Eye movement and gaze direction.
- Gaze stability and changes in screen-relative orientation.
- Head movement and orientation.
- Observable facial movement and engagement cues.
- Repeated visible movements or gestures.
- Camera visibility and observation quality.

## 3. Observable Signals

| Signal | Observable measurement | Limitation |
|---|---|---|
| Gaze direction | Approximate screen-relative gaze direction, if technically available | Does not establish attention or understanding |
| Gaze stability | Frequency and duration of changes in estimated gaze direction | Eye movement varies naturally and across individuals |
| Head movement | Frequency and duration of head-orientation changes | Movement may reflect communication style, disability, or environment |
| Facial movement | Detectable changes in visible facial landmarks | Facial movement cannot reliably establish emotion or engagement |
| Visible gestures | Frequency and duration of observable hand or body movements | Gestures have different cultural and individual meanings |
| Observation quality | Face visibility, lighting, occlusion, and camera availability | Poor visibility must not be treated as poor candidate performance |

## 4. Measurable Indicators

The proposed indicators are:

- Screen-relative gaze-on-screen duration.
- Off-screen orientation event frequency.
- Head-orientation change frequency.
- Repetitive visible movement frequency.
- Facial landmark observation availability.
- Camera visibility and data-quality rate.

These measurements describe observable events only. They must not be interpreted as direct measurements of focus, distraction, nervousness, honesty, confidence, or competence.

## 5. Proposed Processing Flow

1. Obtain explicit, informed consent before any optional visual capture.
2. Confirm that the candidate can decline without disadvantage.
3. Capture only the minimum necessary visual data.
4. Check image quality and whether observations are technically available.
5. Extract only approved observable measurements.
6. Attach timestamps and data-quality information.
7. Present neutral observations for optional human review.
8. Apply configured retention and deletion controls.

## 6. Non-Invasive Design Principles

- Visual analysis must be optional.
- No hidden or continuous recording.
- No emotion recognition or psychological diagnosis.
- No identity recognition or demographic classification.
- No inference of honesty, personality, confidence, or nervousness.
- No candidate ranking or hiring decisions based on visual indicators.
- Missing or poor-quality visual data must not reduce a candidate's score.
- Provide an accessible alternative interview method.

## 7. Privacy and Fairness

The existing InterviewState supports consent, consent withdrawal, response retention, and in-memory response purging.

Visual capture would require separate review of consent scope, storage, access control, retention, deletion, and audit logging before implementation.

Potential differences in disability, neurodiversity, culture, lighting, camera placement, and individual behavior must be considered.

## 8. Current Implementation Status

The existing project contains text-based communication analysis and behavioral reporting.

No visual signal extraction module was identified during the Day 48 repository inspection.

Therefore, this document is a research and design deliverable, not evidence of a working camera-based analysis feature.

## 9. Conclusion

The proposed design focuses on transparent observation, data quality, consent, privacy, fairness, and human oversight. Visual measurements are not suitable as independent evidence of candidate suitability and must not be used to automate hiring decisions.
