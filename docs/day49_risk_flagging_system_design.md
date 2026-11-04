\# Day 49 – Risk Flagging System Design



\## 1. Objective



The purpose of this document is to design a risk flagging system for identifying unusual events during AI-based interviews. The system organizes observable events into explainable review flags so that authorized reviewers can examine them.



A risk flag is an indication that an event may need review. It is not proof of cheating, misconduct, or dishonesty.



\## 2. Risk Flagging Principles



The proposed system follows these principles:



\- Flags must be based on recorded and verifiable events.

\- Every flag must include the reason it was generated.

\- Risk levels represent review priority, not the probability of cheating.

\- A single event must not automatically result in candidate rejection.

\- Missing or unreliable observations must not create penalties.

\- Candidates must receive clear information about optional monitoring.

\- Human reviewers must make the final assessment.



\## 3. Risk Priority Levels



The following levels are proposed for organizing review activities.



\### Low Priority



Used for isolated or minor events that may have a technical or environmental explanation.



Examples:

\- One brief tab switch.

\- A short screen-focus interruption.

\- A single possible background voice event.



\### Moderate Priority



Used when multiple observable events occur within a defined period and require further examination.



Examples:

\- Repeated tab switches.

\- Multiple screen-focus interruptions.

\- Repeated possible background voice events.



\### High Review Priority



Used when several different event types repeatedly occur during the same interview session and require careful human review.



A high-priority flag is not a conclusion that malpractice occurred.



\## 4. Event-to-Flag Mapping



| Observable Event | Proposed Flag | Review Information |

|---|---|---|

| Tab switching | TAB\_SWITCH\_RECORDED | Number and timestamps of switches |

| Screen focus loss | SCREEN\_FOCUS\_LOSS | Duration and frequency |

| Possible external voice | POSSIBLE\_EXTERNAL\_VOICE | Detection timestamp and audio quality |

| Repeated looking away | REPEATED\_GAZE\_DIRECTION\_CHANGE | Observation count and visual quality |

| Multiple event types | MULTIPLE\_SESSION\_EVENTS | Related event references |



These events must be recorded only when the relevant monitoring method has been separately authorized and technically available.



Looking away or hearing another voice must never independently establish misconduct.



\## 5. Risk Flag Data Structure



Each proposed flag should contain the following information:



| Field | Description |

|---|---|

| flag\_id | Unique flag identifier |

| session\_id | Interview session identifier |

| event\_type | Type of recorded event |

| priority | Low, moderate, or high review priority |

| triggered\_rule | Rule that generated the flag |

| evidence\_summary | Short explanation of the observed event |

| event\_timestamp | Time when the event occurred |

| observation\_quality | Reliability or technical quality of the observation |

| consent\_reference | Reference to the applicable monitoring consent |

| review\_status | Pending, reviewed, dismissed, or inconclusive |

| reviewer\_notes | Notes entered by the authorized reviewer |

| created\_at | Flag creation timestamp |



The system should store only the information necessary for review and apply an approved retention policy.



\## 6. Real-Time Warning System



The proposed warning system should use neutral language.



\### Candidate-facing warnings



Examples:



\- "Your interview window appears to have lost focus. Please return to the interview."

\- "A possible background audio event was detected. Please ensure that your interview environment is suitable."

\- "Please keep the interview window active where possible."



Warnings should explain the observed technical event without accusing the candidate.



Warnings should not be issued when the observation is unreliable or monitoring consent is unavailable.



\### Reviewer-facing alert



Example:



"Multiple session events were recorded during this interview. Review the event timestamps and observation quality before reaching any conclusion."



\## 7. Review Workflow



1\. Record an authorized and observable event.

2\. Validate the event's technical quality.

3\. Check whether the event meets a configured review rule.

4\. Generate a neutral risk flag if appropriate.

5\. Notify the authorized reviewer.

6\. Allow the reviewer to examine the evidence and context.

7\. Record the review outcome.



\### Possible review outcomes



\- Relevant for further review.

\- Explained by a technical or environmental issue.

\- Dismissed as an unreliable observation.

\- Inconclusive due to insufficient evidence.



No outcome should automatically change the candidate's HR score or determine hiring eligibility.



\## 8. Integration with Day 48 Behavioral Signals



The proposed Day 49 system can reference the observable signal framework designed in Day 48.



Integration boundaries:



\- Day 48 describes optional behavioral observations.

\- Day 49 organizes authorized interview-session events into review flags.

\- Both systems must preserve observation quality and consent information.

\- Behavioral observations and integrity flags must remain separate.

\- Gaze direction or facial movement must not be treated as evidence of cheating.



\## 9. Separation from Existing Scoring



Integrity flags must remain separate from:



\- HR interview risk flags.

\- Technical skill scores.

\- Communication scores.

\- Behavioral indicators.

\- Overall candidate scores.



The existing HR risk flags describe interview evaluation issues. They must not be reused or overwritten for malpractice monitoring.



A reviewer may consider relevant evidence, but the flagging system must not automatically reduce scores or reject candidates.



\## 10. Privacy, Fairness, and Accessibility



\- Obtain separate, informed consent for screen, camera, or microphone monitoring.

\- Consent for recording interview responses does not automatically authorize other monitoring.

\- Provide a reasonable non-monitoring alternative.

\- Avoid collecting unnecessary personal or environmental information.

\- Apply access controls and retention limits.

\- Consider accessibility needs and technical limitations.

\- Do not penalize candidates for missing or unreliable observations.

\- Allow candidates to explain technical or environmental interruptions.

\- Maintain human oversight for every consequential decision.



\## 11. Validation Requirements



Before implementation, the proposed system requires:



\- Testing of event detection accuracy.

\- Testing of false-positive and false-negative cases.

\- Validation of configurable thresholds.

\- Testing under different network and device conditions.

\- Accessibility and fairness reviews.

\- Privacy and consent review.

\- Human-review workflow testing.



Thresholds must be treated as provisional until validated. They must not be described as cheating probabilities.



\## 12. Current Implementation Status



Repository inspection did not identify a dedicated risk flagging engine, browser tab-switch collector, screen-focus monitor, or external-voice detection module.



The existing HR summary generator has its own evaluation-related risk flags. These are separate from the proposed integrity monitoring design.



Therefore, this document describes a proposed system design only. It does not claim that real-time monitoring, event detection, or automatic malpractice flagging has been implemented.



\## 13. Conclusion



The proposed risk flagging system provides an explainable way to organize unusual interview-session events for human review.



It emphasizes informed consent, privacy, technical reliability, fairness, and separation from candidate scoring.



A recorded event is not proof of misconduct. All flags require appropriate context and human review before any decision is made.

