# Day 46 – Technical Interview AI Blueprint

## 1. Objective

Design a role-based technical interview system that selects relevant questions according to a candidate's technical role and years of experience, then manages the interview through defined stages.

## 2. System Architecture

The Day 46 design contains three main components:

1. **Technical Question Bank**
   - Stores questions in JSON format.
   - Organizes questions by technical role and experience band.
   - Each question contains an ID, question type, difficulty, domain, question text, and expected answer points.

2. **Technical Interview Generator**
   - Implemented in `question_generator/technical_interview_generator.py`.
   - Loads and validates the question bank.
   - Identifies the requested role.
   - Selects the experience band.
   - Organizes questions by conceptual, practical, and scenario-based types.
   - Supports question limits and skill-domain filtering.

3. **Technical Interview Flow Manager**
   - Implemented in `interview_ai/technical_interview_flow.py`.
   - Manages interview phases.
   - Allows only the next valid phase.
   - Records phase history and completion status.

## 3. Supported Technical Roles

The question bank currently supports:

- Python Developer
- Data Analyst
- AWS Cloud Engineer
- Cyber Security Analyst

Each role has three experience bands:

| Experience | Band | Intended level |
|---|---|---|
| 0–2 years | 0-2 | Basic |
| 3–5 years | 3-5 | Intermediate |
| 5+ years | 5+ | Advanced |

The current bank contains 36 questions: 4 roles × 3 experience bands × 3 question types.

## 4. Question Hierarchy Model

Questions are organized into three types:

### Conceptual Questions
Evaluate understanding of technical concepts, terminology, and fundamentals.

### Practical Questions
Evaluate the ability to apply technical knowledge through coding, queries, configuration, or other practical tasks.

### Scenario-Based Questions
Evaluate how a candidate approaches real-world technical problems and makes decisions.

Each question includes:
- Unique question ID
- Question type
- Difficulty level
- Technical domain
- Question text
- Expected answer points

The generator presents questions in this order: conceptual, practical, and scenario-based.

## 5. Interview Flow Design

The interview follows six sequential phases:

1. Introduction – begin the interview and establish the session.
2. Experience-Based – discuss the candidate's previous technical experience.
3. Conceptual – assess understanding of technical concepts.
4. Scenario-Based – explore practical reasoning and problem-solving.
5. Closing – conclude the interview.
6. Completed – mark the interview as finished.

### Flow Diagram

```mermaid
flowchart TD
    A[Introduction] --> B[Experience-Based]
    B --> C[Conceptual]
    C --> D[Scenario-Based]
    D --> E[Closing]
    E --> F[Completed]
