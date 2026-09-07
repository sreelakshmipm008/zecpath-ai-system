# Metadata Standards

## 1. Candidate ID

- Field Name: `candidate_id`
- Data Type: String
- Required: Yes
- Format: `CAND_<unique_number>`
- Example: `CAND_001`
- Description: Unique identifier assigned to each candidate.

## 2. Job ID

- Field Name: `job_id`
- Data Type: String
- Required: Yes
- Format: `JOB_<role_identifier>_<unique_number>`
- Example: `JOB_DS_001`
- Description: Unique identifier assigned to each job.

## 3. Question ID

- Field Name: `question_id`
- Data Type: String
- Required: Yes
- Format: `Q_<unique_number>`
- Example: `Q_001`
- Description: Unique identifier assigned to each screening question.

## 4. Timestamp

- Field Name: `timestamp`
- Data Type: String
- Required: Yes
- Format: `HH:MM:SS`
- Example: `00:02:15`
- Description: Timestamp associated with the transcript segment.

## 5. Confidence Level

- Field Name: `confidence_level`
- Data Type: Float
- Required: Yes
- Range: `0.0 - 1.0`
- Example: `0.94`
- Description: Confidence score associated with the speech-to-text transcription.