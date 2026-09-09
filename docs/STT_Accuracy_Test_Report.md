# STT Accuracy Test Report

## 1. Purpose

This report documents the speech-to-text (STT) testing performed for Day 24 of the Zecser AI screening system.

The objective was to evaluate speech transcription across different prepared speech conditions and verify that the resulting transcripts can pass through the transcript normalization pipeline.

## 2. STT Implementation

The system uses Faster-Whisper for speech-to-text transcription.

Configuration used during testing:

- Model: `tiny`
- Device: `cpu`
- Compute type: `int8`
- Language: English (`en`)

The STT service is implemented in:

`stt/speech_to_text.py`

The clean transcript pipeline is implemented in:

`stt/clean_transcript_processor.py`

The normalization logic is implemented in:

`stt/transcript_normalizer.py`

## 3. Test Fixtures

The following WAV fixtures were tested:

1. `accent_sample_1.wav`
2. `accent_sample_2.wav`
3. `accent_sample_3.wav`
4. `clean_sample.wav`
5. `filler_speech.wav`
6. `interrupted_speech.wav`
7. `partial_answer.wav`
8. `silence_speech.wav`

No specific accent or noise labels were assigned where the available test evidence did not establish them.

## 4. Test Results

### Accent Samples

| Fixture | Observed Clean Transcript | Observation |
|---|---|---|
| `accent_sample_1.wav` | I have two years of experience in Python, SQL and machine learning. | Good transcription |
| `accent_sample_2.wav` | I have two years of experience in Python, c-good and machine learning. | Recognition error observed |
| `accent_sample_3.wav` | I have two years of experience in Python in glenn machine learning. | Recognition error observed |

### Other Speech Conditions

| Fixture | Observed Clean Transcript | Observation |
|---|---|---|
| `clean_sample.wav` | I have experienced in bite and sea gulp and does a machine learning. | Multiple recognition errors observed |
| `filler_speech.wav` | I have two years of experience in Python, worked on several data analysis projects. | Transcript produced and filler processing worked |
| `interrupted_speech.wav` | I have experience in Python and actually i started working Python during my final year project when i moved into data music. | Transcript preserved; recognition/casing issues remain |
| `partial_answer.wav` | I have experienced it five days in school and. | Partial response preserved without inventing missing content |
| `silence_speech.wav` | I have experience in finding them. | Transcript produced despite the low-energy portion |

## 5. Normal Speech Baseline

The known reference transcript for `normal_speech.wav` was:

> I have two years of experience in Python and SQL. I have worked on data analysis projects using pandas and machine learning.

The clean transcript produced by the complete pipeline was:

> I have two years of experience in Python and SQL. I have worked on data analysis projects using Pandas and machine learning.

The spoken content matched the reference. The observed difference was capitalization of `pandas` as `Pandas`, caused by the technical-term preservation rule in transcript normalization.

## 6. Filler-Word Handling

The filler speech fixture was processed successfully.

The clean transcript did not contain the filler words present in the speech input.

This confirms that filler-word removal is integrated into the clean transcript processing pipeline.

## 7. Interrupted Speech Handling

The interrupted speech fixture produced a usable transcript.

The system preserves the available spoken content rather than attempting to reconstruct or invent missing speech.

Some speech-recognition errors were observed in the resulting transcript.

## 8. Partial Answer Handling

The partial-answer fixture produced:

> I have experienced it five days in school and.

The incomplete response was preserved.

The system does not fabricate the missing portion of an incomplete answer.

## 9. Silence Detection

Audio-level silence detection was implemented using RMS energy analysis.

For `silence_speech.wav`:

- Sample rate: 44,100 Hz
- Duration: approximately 5.28 seconds
- Analysis window: 0.5 seconds
- RMS threshold used: `0.02`
- Detected silent windows: 6

The lower-energy region begins at approximately 2.5 seconds.

A unit test was added for this behavior and passed successfully.

## 10. VAD Testing

Faster-Whisper voice activity detection was also tested.

Without VAD:

> I have experience in finding them.

With VAD:

> I have experience in frightened.

This demonstrates that VAD does not guarantee transcription accuracy. Therefore, audio-level silence detection and STT transcription accuracy are treated as separate concerns.

## 11. Test Validation

The transcript normalization test suite contains six tests.

Validation result:

`6 passed`

The tests cover:

- Filler-word removal
- Whitespace normalization
- Punctuation normalization
- Leading filler/punctuation cleanup
- Empty filler-only transcript handling
- Audio silence detection

## 12. Findings

The Day 24 implementation successfully provides:

- Faster-Whisper STT integration
- Transcript normalization
- Filler-word removal
- Punctuation normalization
- Case normalization
- Interrupted speech processing
- Partial-answer preservation
- Audio-level silence detection
- VAD testing
- End-to-end clean transcript processing

The tests also show that STT recognition quality varies across the prepared speech fixtures. Some samples contain recognition errors, particularly in the accent and other speech-condition tests.

The system therefore treats the STT output as input to the normalization pipeline rather than assuming that every transcription is perfectly accurate.

## 13. Conclusion

The STT and transcript-processing implementation required for Day 24 has been implemented and tested using the available speech fixtures.

The complete pipeline successfully converts audio into normalized text suitable for downstream AI screening analysis, while preserving incomplete responses and avoiding unsupported reconstruction of unclear speech.