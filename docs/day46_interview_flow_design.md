# Day 46 – Technical Interview Flow Design

## 1. Purpose

Define the sequence of stages followed during a role-based technical interview.

## 2. Interview Stages

| Order | Stage | Purpose |
|---|---|---|
| 1 | Introduction | Establish the interview session |
| 2 | Experience-Based | Discuss previous technical experience |
| 3 | Conceptual | Assess technical knowledge |
| 4 | Scenario-Based | Assess practical reasoning and problem-solving |
| 5 | Closing | Conclude the interview |
| 6 | Completed | Mark the session as complete |

## 3. Flow Diagram

```mermaid
flowchart TD
    A[Introduction] --> B[Experience-Based]
    B --> C[Conceptual]
    C --> D[Scenario-Based]
    D --> E[Closing]
    E --> F[Completed]
