# Day 48 - Signal-to-Score Mapping Model

## 1. Objective

Define a transparent mapping between observable visual signals, measurable indicators, and normalized observation values.

The model is a research proposal. It is not an implemented visual-analysis engine or a candidate evaluation score.

## 2. Signal Mapping

| Signal | Measurable indicator | Proposed measurement | Interpretation boundary |
|---|---|---|---|
| Eye movement | Gaze direction changes | Number of detected changes per observation period | Does not measure attention |
| Gaze stability | Direction variation | Variation in estimated screen-relative gaze direction | Does not measure focus or confidence |
| Head movement | Orientation changes | Number and duration of detected orientation changes | Does not establish nervousness |
| Facial movement | Landmark movement availability | Percentage of frames with usable landmark observations | Does not measure emotion |
| Visible gestures | Repeated movement events | Event count and duration | Does not establish personality |
| Camera quality | Usable observation frames | Usable frames divided by total sampled frames | Measures technical quality only |

## 3. Normalized Measurement Scale

Where a numerical measurement is technically available, it may be normalized to a 0–100 scale for display.

Example:

Normalized observation availability =
(Usable observation frames / Total sampled frames) * 100

This value represents technical observation availability only.

It must not be described as a candidate's focus, engagement, confidence, or performance score.

## 4. Signal-to-Score Mapping

| Indicator | Output | Allowed use |
|---|---|---|
| Gaze direction variation | Event count or duration | Descriptive observation |
| Head orientation changes | Event count or duration | Descriptive observation |
| Facial landmark availability | Observation availability percentage | Technical quality check |
| Gesture frequency | Event count or duration | Descriptive observation |
| Camera visibility | Quality percentage or unavailable status | Technical quality check |
| Missing visual data | Unavailable | No penalty or negative inference |

## 5. Proposed Data Quality Levels

| Quality level | Availability | System handling |
|---|---|---|
| High | 80–100% | Measurements may be displayed with limitations |
| Moderate | 50–79% | Display with a quality warning |
| Low | Below 50% | Mark observations as unreliable |
| Unavailable | No usable observations | Do not calculate measurements |

These thresholds are provisional design values and require technical validation before implementation.

## 6. Mapping Rules

1. Preserve the original measurement and its timestamp.
2. Record the measurement method and observation quality.
3. Do not replace missing measurements with assumed values.
4. Do not convert gaze or facial movements into psychological labels.
5. Do not combine visual measurements into a candidate suitability score.
6. Do not use visual measurements for candidate ranking or hiring decisions.
7. Allow human reviewers to disregard unreliable observations.

## 7. Example

Suppose a hypothetical observation session contains 100 sampled frames and 85 frames meet the technical visibility requirements.

Observation availability = (85 / 100) * 100 = 85%.

The report may state:

"Technical observation availability: 85%."

It must not state:

"Candidate focus score: 85%."

The two statements represent fundamentally different concepts.

## 8. Integration with Existing Zecpath AI

The current system contains text-based communication analysis and behavioral reporting.

The proposed visual mapping model should remain a separate optional component. It must not change existing HR scoring weights or technical skill scores.

Any future integration requires explicit consent, privacy review, accessibility review, and validation.

## 9. Conclusion

This mapping model provides measurable and explainable visual observation outputs while separating technical observation quality from candidate assessment. It does not establish psychological traits or suitability for employment.
