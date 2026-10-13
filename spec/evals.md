# Evaluation record

Reference-model evaluation was run locally on five public labeled clips per language. It is not a target-class recording or a broad benchmark; the clean/read-speech results do not establish accuracy for quiet, noisy, overlapping, accented, or classroom speech.

## Invariant coverage

| ID | Contract invariant | Evaluation / evidence | Status |
|---|---|---|---|
| EV-1 | C-1 local capture; no raw audio | Inspect runtime data flow; then observe session folder during smoke | PENDING |
| EV-2 | C-2 bounded queue; one model | Inspect finite 240-block queue and one language-specific recognizer; measure target PC | PARTIAL |
| EV-3 | C-3 route/mute limitation disclosed | Review UI and README; confirm loopback on target Windows | PENDING |
| EV-4 | C-4 explicit phrase matching | Review detector; evaluate known positive/negative utterances | PENDING |
| EV-5 | C-5 local note durability | Stop a session and inspect Markdown; confirm queued segments flush | PENDING |
| EV-6 | C-6 bounded optional gain | Three clean clips per language digitally attenuated 10×, then compared with gain off/on; peak clipping counted | PARTIAL (no real-room noise test) |
| EV-7 | Recognition quality and throughput | Same five public labeled clips per language through Vosk and Whisper base; average WER and inference wall time recorded below | COMPLETE (directional only) |
| EV-8 | Recognition across loopback playback volumes | Same spoken sample at ordinary low/high Windows output levels; compare capture level, WER, and clipping with gain off/on | PENDING |
| EV-9 | English/Hindi automatic switching | Mixed and changing-language clips; measure language decisions, transcript quality, switch delay, CPU, and peak RAM on target PC | PENDING |

## EV-7 — Reference comparison (2026-10-13)

Same clips were run through both recognizers on the target development PC (Dell Inspiron 3593, Intel Core i3-1005G1, 2 cores / 4 threads, 7.8 GiB RAM) using CPU int8 Whisper with two CPU threads. Word error rate lower is better. Inference time excludes model load. English references were five short [LibriSpeech dummy clips](https://huggingface.co/datasets/hf-internal-testing/librispeech_asr_dummy); Hindi references were the first five clips in [dhruvkys/hi-asr-1k](https://huggingface.co/datasets/dhruvkys/hi-asr-1k) (Common Voice-derived). Only aggregate results are retained; reference audio was stored temporarily and is not part of the repository.

| Language / engine | Mean WER | Inference time for five clips | Model load time | Decision |
|---|---:|---:|---:|---|
| English Vosk small | 19.8% | 19.8 s | 0.6 s | Not selected |
| English Whisper base.en | 8.0% | 14.0 s | 3.6 s (cached run) | Selected |
| Hindi Vosk small | 17.0% | 17.6 s | 1.6 s | Selected |
| Hindi Whisper base | 96.3% | 19.2 s | 1.6 s (cached run) | Not selected; several outputs used Urdu/Latin script |

The selected app-path implementation was then evaluated on the same clips using 12-second Whisper windows with 2-second overlap and the actual Vosk stream interface:

| Language / app path | Mean WER | Inference time for five clips | Load time |
|---|---:|---:|---:|
| English Whisper base.en, 12 s / 2 s overlap | 8.3% | 26.5 s | 4.2 s (cached) |
| English Whisper base.en, 8 s / 1 s overlap | 30.3% | 22.2 s | 4.2 s (cached) |
| Hindi Vosk small | 14.4% | 14.3 s | 2.4 s |

Performance times reflect this target-PC run only. CPU utilization, peak process memory, queue delay during a live class, and the larger Whisper-small Hindi check were not completed; they do not change the current language-specific decision.

## EV-6 — Gain experiment (2026-10-13)

Three public reference clips per language were digitally attenuated to 10% amplitude and processed through the same 8×-capped gain/smoothing algorithm used by `AudioCapture`. This approximates low input level but contains no added room noise and is not a microphone/loopback measurement.

| Language / recognizer | WER, gain off | WER, gain on | Result RMS after gain | Clipped samples |
|---|---:|---:|---:|---:|
| English Whisper base.en | 5.0% | 5.0% | 0.047–0.056 | 0% |
| Hindi Vosk small | 12.2% | 19.1% | 0.011–0.088 | 0% |

Gain did not improve these references and worsened Hindi on this small set, so it is off by default. It remains available for a user to try when their actual input is too quiet; room-noise behavior remains unmeasured.

The note destination and in-app discovery path were changed to the Windows configured Documents folder for M1-NOTES-02. This implementation has not yet been exercised in a live app session; EV-5 remains PENDING until the target-PC smoke check confirms the file exists and contains the expected content. Quiet-gain behavior remains unmeasured (EV-6).

## Required negative cases

- Unconfigured names must not generate name alerts.
- A Latin trigger must not match merely as a substring inside a longer unrelated word.
- An empty custom phrase must never match.
- An absent model must stop startup with an actionable error, not silently use cloud recognition.
- Audio queue overload must stay bounded; a capture failure must be visible.
- Stopping during active audio must close the note only after the transcription worker flushes queued audio.
- The capture-level diagnostic must be transient, show near-silence for a silent source and higher readings when the selected device receives sound; verify on the target PC.

## Gate

M0 remains OPEN until target-machine smoke outcomes and performance observations are recorded. Automated test suite status: NOT RUN. Hardware/manual suite: NOT RUN.

## 2026-10-13 — User-reported live test failure

User reports no transcript while speaking and only a few inaccurate words while music played; no alert was generated. The selected device, live level, language, phrase configuration, and timing during this run were not recorded. This does not establish whether the cause was routing/level, language mismatch, recognizer delay/accuracy, or an alert phrase mismatch. Added a transient one-second RMS level display and explicit selected-source status for the next diagnostic run. Hardware behavior remains UNVERIFIED; repeat the short smoke checks with a spoken phrase in the selected language and a configured alert phrase.

## 2026-10-13 — User-reported follow-up class test

User reports English transcription was usable but slow, and the attendance alert appeared. Hindi required manual language selection and remained slow with poor accuracy. This is the first positive live alert report; device, exact phrase/sample, dBFS, and timings were not measured, so it does not close M0. User requests eventual English/Hindi auto-switching and similar recognition at reasonable low/high speaker volumes. Added EV-8/EV-9 to measure those requirements before changing gain or model defaults. No new hardware or model comparison was run in this turn.
