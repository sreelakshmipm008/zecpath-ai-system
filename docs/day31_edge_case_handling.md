# Day 31 — AI Flow Edge-Case Handling

## Objective

Ensure AI screening flow stability under real-world input conditions by handling common audio, language, response, and processing edge cases safely.

## Implemented Edge Cases

### 1. Poor Audio Quality

Poor audio input is handled through the AI error-handling framework.

When an audio-quality issue is detected:

- The candidate is asked to record the answer again.
- Retry is allowed within the configured retry limit.
- If the issue persists after the allowed retries, the system uses a safe fallback.

Handler status:

`audio_issue`

Primary recovery action:

`retry`

---

### 2. Language Mixing

The speech-to-text service no longer forces English when no language is explicitly supplied.

The transcription method accepts:

`language: str | None = None`

When no language is provided, the underlying Faster-Whisper model can perform automatic language detection.

Explicit language values can still be supplied when required.

---

### 3. Missing Answers

Empty candidate answers are detected before semantic extraction.

The system returns:

- `intent = missing`
- clarification message
- retry permission

If the configured retry limit is reached, the system returns a fallback response and disables further retries.

Handler status:

`missing`

Primary recovery action:

`clarify`

---

### 4. Background Noise

The speech-to-text module includes background-noise detection based on audio energy.

The error-handling framework responds to detected background noise by:

- asking the candidate to move to a quieter environment,
- allowing a retry,
- using a safe fallback when the retry limit is reached.

Handler status:

`background_noise`

Primary recovery action:

`retry`

> Note: The current detector uses an RMS-energy threshold. It should be treated as an audio-quality heuristic rather than a definitive classifier of speech versus environmental noise.

---

### 5. Retry and Clarification Logic

A unified error handler routes known edge cases to their appropriate recovery behavior.

| Status | Action | Retry Allowed |
|---|---|---|
| `missing` | `clarify` | Yes |
| `audio_issue` | `retry` | Yes |
| `background_noise` | `retry` | Yes |
| unknown status | `continue` | No |
| `unexpected_error` | `fallback` | No |

The retry limit is centrally configured in `AIErrorHandler`.

---

### 6. Unexpected Processing Errors

Unexpected AI-flow errors are handled through a safety fallback.

The system does not expose the underlying exception to the candidate.

Instead, it returns a controlled message asking the candidate to try again later.

Handler status:

`unexpected_error`

Primary recovery action:

`fallback`

---

## Safety Principles

The Day 31 error-handling framework follows these principles:

1. Prefer recovery when the issue is potentially temporary.
2. Ask for clarification when a candidate response is missing.
3. Avoid exposing internal exceptions or implementation details.
4. Stop retrying after the configured retry limit.
5. Continue safely when an unknown status does not require recovery.
6. Preserve existing AI screening behavior when no edge case is detected.

## Testing

A dedicated test suite was added:

`tests/test_ai_error_handler.py`

The Day 31 error-handling tests cover:

- missing-answer clarification,
- audio-quality retry,
- background-noise retry,
- safe continuation for unknown status,
- unexpected-error fallback,
- retry-limit fallback.

Result:

**6/6 Day 31 error-handling tests passed.**

## Regression Test Status

The full project test suite currently contains 30 tests.

Result:

- 29 passed
- 1 failed

The single failure is an existing Day 24 silence-audio fixture path issue:

`day24/silence_speech.wav`

This fixture is not currently available at the path referenced by the existing test.

The failure is unrelated to the Day 31 error-handling implementation.