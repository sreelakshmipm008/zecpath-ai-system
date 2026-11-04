# Day 46 – Technical Interview Question Hierarchy Model

## 1. Purpose

The question hierarchy organizes technical interview questions by candidate role, experience level, technical domain, and question type.

## 2. Supported Roles

- Python Developer
- Data Analyst
- AWS Cloud Engineer
- Cyber Security Analyst

## 3. Experience-Based Hierarchy

| Experience | Band | Difficulty |
|---|---|---|
| 0–2 years | 0-2 | Basic |
| 3–5 years | 3-5 | Intermediate |
| 5+ years | 5+ | Advanced |

## 4. Question Types

### Conceptual
Checks understanding of technical concepts, definitions, principles, and fundamentals.

### Practical
Checks the ability to apply knowledge through coding, SQL queries, configurations, or technical exercises.

### Scenario-Based
Checks problem-solving approaches in realistic technical situations.

## 5. Question Metadata

Each question contains:

- `id`: Unique question identifier.
- `type`: Conceptual, practical, or scenario.
- `difficulty`: Expected difficulty level.
- `domain`: Relevant technical skill area.
- `question`: Question presented to the candidate.
- `expected_points`: Important points expected in a strong answer.

## 6. Selection Logic

1. Receive the candidate's technical role.
2. Receive experience in years.
3. Map experience to the appropriate band.
4. Load questions for the selected role and band.
5. Organize questions in conceptual, practical, and scenario-based order.
6. Optionally filter by skill domain.
7. Optionally limit the number of questions.
8. Return the selected questions with candidate and hierarchy metadata.

## 7. Current Question Bank Size

| Measure | Count |
|---|---:|
| Technical roles | 4 |
| Experience bands per role | 3 |
| Questions per role and band | 3 |
| Total questions | 36 |

## 8. Example

For a Python Developer with 2 years of experience:

- Selected band: 0-2
- Difficulty: Basic
- Question types: Conceptual, Practical, Scenario
- Questions selected: 3

## 9. Implementation Reference

- Question bank: `data/technical_interview/technical_question_bank.json`
- Generator: `question_generator/technical_interview_generator.py`
- Automated tests: `tests/test_technical_interview_generator.py`

## 10. Scope

This hierarchy provides structured question selection. It does not itself evaluate candidate answers, assign technical skill scores, or adapt difficulty based on answer quality. Those capabilities require separate implementation.
