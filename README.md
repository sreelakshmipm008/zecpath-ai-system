# Zecpath AI System

An AI-assisted recruitment and interview evaluation project developed as part of the Zecser Business LLP internship.

## Project Overview

Zecpath AI is a modular Python project designed to support different stages of recruitment, including resume processing, candidate screening, interview assistance, evaluation, and scoring.

The system is intended to assist recruiters. AI-generated scores and recommendations should be reviewed by humans and should not be treated as automatic hiring decisions.

## Main Modules

| Module | Purpose |
|---|---|
| `extractors/` | Extracts text from supported documents |
| `parsers/` | Resume and document parsing |
| `preprocess/` | Text cleaning and preprocessing |
| `answer_understanding/` | Interview answer understanding |
| `question_generator/` | Interview question generation |
| `interview_ai/` | Interview-related processing |
| `scoring/` | Candidate and interview scoring |
| `security/` | Security and data-governance components |
| `stt/` | Speech-to-text functionality |
| `utils/` | Shared utilities |
| `data/` | Input data and generated outputs |
| `tests/` | Automated tests |
| `scripts/` | Supporting scripts |
| `docs/` | Technical documentation, reports, and project deliverables |

## Technologies

- Python 3.12.10
- Pandas and NumPy
- scikit-learn
- RapidFuzz
- Faster-Whisper
- Matplotlib and Seaborn
- Pytest
- Git and GitHub

## Requirements

- Python 3.12.x
- Git
- pip

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/sreelakshmipm008/zecpath-ai-system.git
cd zecpath-ai-system
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Resume Processing Entry Point

The current `main.py` entry point processes PDF and DOCX resumes from `data/resumes/`, extracts their text, cleans it, and saves the results as text files in `data/cleaned_text/`.

1. Create the input folder if it does not exist:

```powershell
New-Item -ItemType Directory -Force data/resumes
```

2. Place PDF or DOCX resume files inside `data/resumes/`.

3. Run:

```bash
python main.py
```

4. Check the generated text files in `data/cleaned_text/`.

Note: `main.py` is the resume extraction and preprocessing entry point. It does not independently launch every module in the recruitment workflow.

## Running Tests

Run the test suite from the repository root:

```bash
python -m pytest -q --ignore=Zecser_Internship_Days_51-55
```

The documented validation baseline from Day 68 was 250 passing tests. Test results may vary if the code or environment changes.

## Documentation

The `docs/` directory contains:

- System architecture and technical documentation
- API design and data schemas
- Resume screening and interview evaluation logic
- Scoring, fairness, and data-governance documentation
- Testing, performance, and monitoring reports
- AI roadmap and future architecture proposals
- Internship reports, demo materials, and handover documents

Start with:

- `docs/AI_Screening_Final_System_Documentation.md`
- `docs/AI_Screening_API_Design.md`
- `docs/AI_Screening_Handover_Document.md`
- `docs/day58_ai_roadmap.md`

## Responsible AI and Limitations

- AI-generated scores are decision-support signals, not final hiring decisions.
- Human review is required for candidate evaluation and recommendations.
- Behavioral signals must be interpreted in context and should not independently determine hiring outcomes.
- Sample and simulated test data should not be interpreted as proof of real-world hiring accuracy.
- Passing automated tests does not establish production readiness.

## Project Status

This repository contains the internship project's modular codebase, supporting documentation, tests, reports, and proposed future improvements. Deployment and production-level validation are not claimed by this documentation.

## Internship Project

Developed as part of the Data Science Engineer Internship at Zecser Business LLP.

Repository: https://github.com/sreelakshmipm008/zecpath-ai-system

