# AI Screening System - API Design

## 1. Purpose

This document describes the proposed API design for exposing the existing AI Screening System to a web application or recruiter interface.

The current repository does not contain a live HTTP API. This document defines the planned API architecture based on the existing Python screening modules.

## 2. API Architecture

The proposed API will connect the client application with the existing AI screening pipeline.

Client Application
        |
        v
API Layer
        |
        v
Speech-to-Text
        |
        v
Transcript Normalization
        |
        v
Answer Understanding
        |
        v
Screening Scoring
        |
        v
Screening Report

## 3. Main API Responsibilities

The API should provide functionality to:

- Start a screening session.
- Retrieve role-specific screening questions.
- Submit candidate audio responses.
- Process candidate transcripts.
- Analyze candidate answers.
- Calculate screening scores.
- Generate screening reports.
- Return controlled errors and retry instructions.

## 4. Current Implementation Status

The API described in this document is a proposed design.

The current repository contains the underlying Python screening components but does not currently contain a deployed FastAPI, Flask, or other HTTP API implementation.

## 5. Proposed API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/screening/start` | Start a screening session for a candidate and role |
| GET | `/screening/{session_id}/questions` | Retrieve screening questions |
| POST | `/screening/{session_id}/answer` | Submit a candidate answer or audio response |
| GET | `/screening/{session_id}/result` | Retrieve the screening result |
| GET | `/screening/{session_id}/report` | Retrieve the generated screening report |

These endpoints are proposed interfaces for a future HTTP API and are not currently implemented in the repository.

## 6. Request and Response Design

### Start Screening

**Request:**
- Candidate ID
- Candidate name
- Target role

**Response:**
- Screening session ID
- Selected role
- Screening status

### Submit Answer

**Request:**
- Session ID
- Question ID
- Candidate audio or transcript

**Response:**
- Processed transcript
- Answer understanding result
- Answer score
- Processing status

### Screening Result

**Response:**
- Overall screening score
- Question-level evaluation
- Screening highlights
- Generated screening report

The exact request and response schemas can be implemented when the HTTP API is developed.

## 7. Error Handling

The proposed API should return controlled responses when screening processing fails.

Examples include:

- Poor or unclear audio
- Missing candidate answers
- Background noise
- Unsupported or mixed language input
- Vague or off-topic answers
- Speech-to-text processing failures
- Unexpected processing errors

The existing `AIErrorHandler` provides the underlying error-handling logic. The future API layer should expose these outcomes as appropriate HTTP responses and retry or clarification instructions.

The API should avoid exposing internal Python errors or implementation details to the client.
