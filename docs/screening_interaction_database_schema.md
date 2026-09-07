# Screening Interaction Database Schema

## Purpose

The screening interaction schema defines the structured representation of a candidate's voice-based screening interaction. It connects the candidate, job, screening question, transcript, timestamp, and speech-to-text confidence information.

## Screening Interaction Fields

| Field Name | Data Type | Required | Description | Example |
|---|---|---|---|---|
| candidate_id | String | Yes | Unique identifier of the candidate. | CAND_001 |
| job_id | String | Yes | Unique identifier of the job. | JOB_DS_001 |
| question_id | String | Yes | Identifier of the screening question. | Q_001 |
| timestamp | String | Yes | Timestamp associated with the transcript segment. | 00:02:15 |
| confidence_level | Float | Yes | Speech-to-text confidence score. | 0.94 |
| speaker | String | Yes | Identifies the speaker. | candidate |
| transcript_text | String | Yes | Normalized transcript text from the screening interaction. | I have two years of experience in Python. |

## Relationships

- `candidate_id` identifies the candidate participating in the screening interaction.
- `job_id` identifies the job for which the candidate is being screened.
- `question_id` identifies the screening question associated with the interaction.
- `timestamp` identifies the position or time of the transcript segment.
- `confidence_level` represents the confidence of the speech-to-text transcription.
- `speaker` identifies whether the segment belongs to the candidate or interviewer.
- `transcript_text` contains the normalized transcript content.

## Example Screening Interaction

```json
{
  "candidate_id": "CAND_001",
  "job_id": "JOB_DS_001",
  "question_id": "Q_001",
  "timestamp": "00:02:15",
  "confidence_level": 0.94,
  "speaker": "candidate",
  "transcript_text": "I have two years of experience in Python."
}


