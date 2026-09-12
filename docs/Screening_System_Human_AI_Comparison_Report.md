# Screening System Human-AI Comparison Report

## 1. Purpose

This report documents the human-versus-AI comparison performed for Day 30 of the Zecser AI screening system.

The objective was to compare the AI screening output from simulated screening calls with a simulated human reference judgment and identify differences that may require further screening-system optimization.

The comparison uses the ten simulated candidate screening reports generated from the existing AI screening question dataset.

## 2. AI Screening Evaluation

The AI screening system evaluates candidate responses using four parameters:

- Clarity
- Relevance
- Completeness
- Consistency

Each parameter contributes equally to the final screening score:

- Clarity: 25%
- Relevance: 25%
- Completeness: 25%
- Consistency: 25%

The final screening score is calculated from the four parameter scores.

The existing screening scoring implementation is:

`scoring/screening_scoring_engine.py`

## 3. Human Reference Method

Because the candidates used for this test are simulated candidates, the human side of the comparison is treated as a simulated human reference judgment rather than an evaluation performed by a real recruiter.

The reference judgment considers:

- Candidate answers to the screening questions
- Required role-specific skills
- Minimum experience requirements
- Required work location
- Candidate availability where applicable
- Overall suitability based on the available screening information

The existing role-specific eligibility configuration was used as the reference for role requirements.

The eligibility configuration is:

`eligibility_config.py`

No changes were made to the existing eligibility rules as part of this comparison.

## 4. Test Candidates

The following ten simulated candidates were evaluated:

| Role | Candidate |
|---|---|
| Accountant | Sample Accountant Candidate |
| AWS Cloud Engineer | Sample AWS Cloud Engineer Candidate |
| Cyber Security Analyst | Sample Cyber Security Analyst Candidate |
| Data Analyst | Sample Data Analyst Candidate |
| Digital Marketing Executive | Sample Digital Marketing Executive Candidate |
| HR Executive | Sample HR Executive Candidate |
| Python Developer | Sample Python Developer Candidate |
| Sales Executive | Sample Sales Executive Candidate |
| Staff Nurse | Sample Staff Nurse Candidate |
| UI/UX Designer | Sample UI/UX Designer Candidate |

The corresponding AI reports are stored in:

`data/ai_screening_reports/`

## 5. Comparison Results

| Role | AI Score | AI Result | Simulated Human Judgment | Comparison |
|---|---:|---|---|---|
| Accountant | 84.75 | High score | Review | Difference |
| AWS Cloud Engineer | 86.59 | High score | Review | Difference |
| Cyber Security Analyst | 85.75 | High score | Review | Difference |
| Data Analyst | 85.10 | High score | Review | Difference |
| Digital Marketing Executive | 87.12 | High score | Eligible | Aligned |
| HR Executive | 87.25 | High score | Review | Difference |
| Python Developer | 82.50 | High score | Review | Difference |
| Sales Executive | 87.12 | High score | Review | Difference |
| Staff Nurse | 84.62 | High score | Review | Difference |
| UI/UX Designer | 86.12 | High score | Review | Difference |

## 6. Human Reference Observations

### Accountant

The candidate reported three years of accounting experience and confirmed experience with Tally, GST, and Excel.

The candidate is located in Kochi, while the configured required location for the Accountant role is Thrissur.

Human reference judgment:

`Review`

### AWS Cloud Engineer

The candidate reported three years of cloud-engineering experience and provided positive responses regarding AWS, Linux, Docker, Terraform, and Kubernetes.

The candidate is located in Kochi, while the configured required location is Bengaluru.

Human reference judgment:

`Review`

### Cyber Security Analyst

The candidate reported three years of cybersecurity experience and provided positive responses regarding SIEM, network security, Python for cybersecurity, and ethical hacking.

The candidate is located in Kochi, while the configured required location is Chennai.

Human reference judgment:

`Review`

### Data Analyst

The candidate reported two years of data-analysis experience and provided positive responses regarding Python, SQL, Power BI, Excel, Pandas, and statistics.

The candidate is located in Kochi, while the configured required location is Hyderabad.

Human reference judgment:

`Review`

### Digital Marketing Executive

The candidate reported two years of digital-marketing experience and provided positive responses regarding SEO, SEM, Google Analytics, and content marketing.

The candidate is located in Kochi, which matches the configured required location.

Human reference judgment:

`Eligible`

### HR Executive

The candidate reported two years of human-resources experience and provided positive responses regarding recruitment, HRMS, Excel, and communication.

The candidate is located in Kochi, while the configured required location is Coimbatore.

Human reference judgment:

`Review`

### Python Developer

The candidate reported three years of Python-development experience and provided positive responses regarding Python, Django, Flask, SQL, Git, REST APIs, and Docker.

The candidate is located in Kochi, while the configured required location is Bengaluru.

Human reference judgment:

`Review`

### Sales Executive

The candidate reported three years of sales experience and provided positive responses regarding CRM systems, negotiation, lead generation, and professional presentations.

The candidate is located in Kochi, while the configured required location is Ernakulam.

Human reference judgment:

`Review`

### Staff Nurse

The candidate reported three years of nursing experience and provided positive responses regarding patient care, ICU experience, emergency care, and communication.

The candidate is located in Kochi, while the configured required location is Kozhikode.

Human reference judgment:

`Review`

### UI/UX Designer

The candidate reported two years of UI/UX design experience and provided positive responses regarding Figma, Adobe XD, wireframes, and HTML/CSS.

The candidate is located in Kochi, while the configured required location is Pune.

Human reference judgment:

`Review`

## 7. AI Output Observations

The AI screening scores were relatively high across all ten simulated candidates.

The observed final screening scores were:

- Accountant: 84.75
- AWS Cloud Engineer: 86.59
- Cyber Security Analyst: 85.75
- Data Analyst: 85.10
- Digital Marketing Executive: 87.12
- HR Executive: 87.25
- Python Developer: 82.50
- Sales Executive: 87.12
- Staff Nurse: 84.62
- UI/UX Designer: 86.12

All ten simulated candidates answered all questions in their respective generated reports.

## 8. Skill Detection Observations

The AI screening report summaries did not consistently expose every skill explicitly confirmed in the candidate answers.

For example, the AWS Cloud Engineer candidate answered positively regarding AWS, Linux, Docker, Terraform, and Kubernetes, while the screening summary displayed:

`aws, docker, kubernetes`

Similarly, some other role reports contained fewer skill confirmations than the skills explicitly stated in the candidate answers.

This indicates a potential difference between the candidate's stated information and the information surfaced by the AI screening summary.

This observation is relevant to subsequent intent-detection and screening optimization work.

## 9. Human-AI Agreement

The comparison produced:

- 1 aligned case
- 9 cases requiring review because the human reference considered the configured location requirement while the AI score remained high

The main observed source of difference was that the AI screening score evaluates the quality of individual answers, while role-specific eligibility also considers configured candidate requirements such as location and mandatory skills.

Therefore, a high AI screening score does not by itself establish final role eligibility.

## 10. Findings

The Day 30 human-versus-AI comparison identified the following findings:

1. The AI screening system successfully generated screening scores for all ten simulated candidates.
2. The AI scores were generally high for the prepared complete answers.
3. The simulated human reference identified location-based review cases that were not reflected directly in the screening score.
4. The AI screening summary did not consistently surface all skills explicitly stated in candidate answers.
5. The existing scoring engine and eligibility engine evaluate different aspects of candidate suitability.
6. The observed differences provide test evidence for further optimization of intent detection, scoring thresholds, and false-rejection handling.

## 11. Conclusion

The human-versus-AI comparison for the ten simulated screening candidates was completed.

The comparison demonstrates that the AI screening score and role-specific human suitability judgment can produce different outcomes because they evaluate different aspects of the candidate information.

The identified differences will be used as evidence for the remaining Day 30 optimization tasks without changing the existing scoring or eligibility rules prematurely.
