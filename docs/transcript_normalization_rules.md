# Transcript Normalization Rules

## 1. Text Cleanup

Remove unnecessary leading and trailing whitespace from transcript text.

## 2. Whitespace Normalization

Replace multiple consecutive spaces with a single space.

## 3. Case Normalization

Use consistent sentence casing while preserving important technical terms and identifiers.

## 4. Punctuation

Preserve meaningful punctuation and remove unnecessary repeated punctuation.

## 5. Filler Words

Common speech fillers such as "um", "uh", and "hmm" may be removed when they do not contribute meaningful information to the candidate's response.

## 6. Speaker Identification

Each transcript segment must identify the speaker as either:

- `candidate`
- `interviewer`

## 7. Timestamp Preservation

Original timestamps must be retained for each transcript segment.

## 8. Confidence Preservation

The speech-to-text confidence level must be retained for each transcript segment.

## 9. Technical Terms

Technical terms, programming languages, tools, technologies, and other domain-specific terms must be preserved accurately.

## 10. Missing or Unclear Speech

Unclear or unintelligible speech should not be replaced with guessed content. It should be marked as unclear when necessary.

## 11. Question Association

Each candidate response should be associated with the corresponding screening question using `question_id`.

## 12. Identifier Preservation

`candidate_id`, `job_id`, and `question_id` must remain unchanged during transcript normalization.