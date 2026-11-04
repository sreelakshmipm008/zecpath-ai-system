\# Day 49 â€“ Malpractice Detection Logic



\## 1. Objective



This document defines proposed logic for identifying unusual interview-session events that may require integrity review. These events are indicators for review only and do not prove cheating or misconduct.



\## 2. Events to Monitor



\### 2.1 Tab Switching



Record browser visibility changes and count repeated events within a configurable rolling five-minute window.



Provisional review levels:

\- 0â€“1 events: Record only; no flag.

\- 2â€“3 events: Low-priority review indicator.

\- 4 or more events: Moderate-priority review indicator.



These thresholds are design proposals and require validation before production use.



\### 2.2 Screen Focus Loss



Record when the interview window loses focus and the duration of the event.



Proposed handling:

\- Less than 3 seconds: Diagnostic event only.

\- 3â€“10 seconds: Optional low-priority review indicator.

\- More than 10 seconds: Review event, subject to technical validation.



Operating-system notifications, accidental clicks, and other legitimate interruptions may cause focus loss.



\### 2.3 Possible External Voice



Any optional audio-based detection must require separate, informed microphone-monitoring consent.



\- Record only the minimum necessary event metadata.

\- Do not identify speakers.

\- Do not assume that another voice indicates unauthorized assistance.

\- Refer uncertain events for human review.

\- No numerical detection threshold is proposed because validated evidence is unavailable.



\### 2.4 Repeated Looking Away



Looking away may occur naturally while thinking, reading, or due to accessibility needs.



\- Treat gaze observations as descriptive only.

\- Do not classify looking away as cheating.

\- Do not generate an automatic malpractice flag from gaze alone.

\- Consider accessibility and individual differences.



\## 3. Pattern Recognition



A combination of independently recorded events may create a review indicator when:

\- Events occur repeatedly within a defined time window.

\- Event timestamps and technical quality are available.

\- The monitoring feature was separately authorized.

\- The pattern is explainable and can be reviewed by a human.



Multiple weak indicators must not be converted into a claim of guilt.



\## 4. Proposed Detection Flow



1\. Confirm the relevant monitoring consent.

2\. Collect permitted event metadata.

3\. Validate timestamps and event quality.

4\. Apply configurable threshold rules.

5\. Create a neutral review indicator when appropriate.

6\. Present evidence to an authorized human reviewer.



\## 5. Example Pseudocode



&#x20;   IF monitoring\_consent\_is\_valid:

&#x20;       collect\_permitted\_events()

&#x20;       validate\_event\_quality()



&#x20;       IF tab\_switch\_count >= configured\_threshold:

&#x20;           create\_neutral\_review\_indicator()



&#x20;       IF focus\_loss\_duration exceeds configured\_threshold:

&#x20;           create\_neutral\_review\_indicator()



&#x20;       send\_indicator\_for\_human\_review()

&#x20;   ELSE:

&#x20;       do\_not\_collect\_monitoring\_events()



\## 6. False Positives and Limitations



Possible explanations for unusual events include:

\- Network or browser interruptions.

\- Accidental tab changes.

\- Operating-system notifications.

\- Accessibility tools.

\- Environmental noise.

\- Natural gaze movement.



Missing or unreliable observations must not create a penalty.



\## 7. Privacy and Fairness



\- Obtain separate consent for browser, screen, camera, or microphone monitoring.

\- Provide a non-monitoring alternative.

\- Collect only necessary information.

\- Define retention and deletion rules.

\- Do not automatically disqualify candidates.

\- Allow candidates to explain flagged events.



\## 8. Implementation Status



This document describes a proposed detection design. Repository inspection did not identify a dedicated browser-event collector, screen-focus monitor, external-voice detector, or malpractice detection engine. No such functionality is claimed as implemented.



## 9. Conclusion



The proposed malpractice detection logic provides a structured and explainable approach to identifying unusual interview-session events for further review. It emphasizes privacy, informed consent, technical reliability, fairness, and human oversight.



The indicators must never be treated as proof of misconduct or used for automatic candidate rejection. Further implementation, testing, and validation are required before this design can be used in a production interview system.


