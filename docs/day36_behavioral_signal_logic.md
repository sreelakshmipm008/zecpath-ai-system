# Behavioral Signal Logic

## 1. Purpose

This document describes the observable behavioral signal logic used to analyze candidate interview responses.

The analysis focuses on communication patterns such as hesitation, uncertainty, contradictions, sentiment, stress-related indicators, and behavioral confidence.

The system evaluates observable response signals and does not attempt to determine a candidate's psychological or medical state.

---

## 2. Hesitation Pattern Detection

The confidence analyzer detects the following hesitation patterns:

### 2.1 Repeated Words

Repeated consecutive words are identified from the normalized response tokens.

Example:

```text
"I worked worked on the project."