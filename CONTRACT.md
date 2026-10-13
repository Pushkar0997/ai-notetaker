# Correctness contract

## Invariants

### C-1 — Local processing by default

**Rule:** Captured audio is passed to the local Vosk recognizer and is never written to a file or transmitted by the default application.
**Why:** Class conversations may contain personal information; local processing is the product's core promise.
**Violation:** Adding cloud transcription, raw-audio persistence, or an external notification without explicit opt-in.
**Detection:** Review all audio data flows in `notetaker/audio_capture.py` and `notetaker/app.py`; see EV-1 in `spec/evals.md`.

### C-2 — Bounded memory and single recognizer

**Rule:** Audio buffering remains bounded at 32 blocks of 0.25 seconds each, and only one language model/recognizer is loaded per session.
**Why:** The target computer has 8 GB RAM and an Intel 10th-generation i3.
**Violation:** An unbounded queue, simultaneous bilingual recognizers, or loading the large models in the prototype's `models/` directory.
**Detection:** Inspect queue construction and model construction; see EV-2.

### C-3 — No false promise of platform access

**Rule:** The app monitors a selected system loopback or microphone device. It does not join meetings or bypass audio streams that the selected endpoint does not render. Whether endpoint volume mute affects loopback is device/driver-dependent.
**Why:** Capture availability depends on the user's Windows audio output route.
**Violation:** Saying that the tool hears remote audio when Windows is not rendering it to the chosen device.
**Detection:** UI and README explicitly describe the route and mute limitation; see EV-3.

### C-4 — Explicit phrase detection

**Rule:** Names and custom triggers are user-configured; attendance terms are exact phrase matches. Do not use whole-sentence fuzzy matching.
**Why:** Fuzzy matching the prototype marked unrelated words such as “pusher” or “rumor” as names.
**Violation:** Alerting on unrelated partial words or assuming a person's name without user input.
**Detection:** Trace `detector.py`; see EV-4.

### C-5 — Notes are durable, local, and transparent

**Rule:** Only finalized recognition segments and detected moments are saved to `%APPDATA%\AI Notetaker\sessions` as UTF-8 Markdown; stop drains queued audio before closing the note file.
**Why:** The user should be able to review what was heard without recording all audio.
**Violation:** Writing partial recognition repeatedly, losing accepted segments on stop, or saving to a shared/remote destination.
**Detection:** Trace the stop and worker-done flow; inspect generated note format; see EV-5.

## Pinned conventions

- Platform: Windows 10/11 desktop; Python 3.10–3.12, 64-bit.
- Audio: 16,000 Hz mono signed 16-bit PCM; capture blocks are 0.25 seconds.
- Audio work buffer: maximum 32 blocks (8 seconds); when full, discard the oldest block to bound memory and favor fresh audio.
- Languages: English or Hindi selected per session; exactly one Vosk model is active.
- Model paths: root folders `model-english/` and `model-hindi/`; no other model folders are part of the active application.
- Time: local machine timezone; note timestamps use `YYYY-MM-DD HH:MM:SS` with timezone where available; transcript line times use `HH:MM:SS`.
- Note encoding: UTF-8 Markdown, file name `YYYY-MM-DD_HH-MM-SS.md`; if that exists, append a two-digit numeric suffix.
- Detection dedupe: 30-second cooldown per normalized `(category, phrase)`.
- Config: JSON under `%APPDATA%\AI Notetaker\settings.json`; no secrets are currently stored.

## Never do this

- Never change default audio capture to a remote service; it breaks offline privacy (C-1).
- Never make transcript storage opt-out or raw-audio recording implicit; it violates C-1 and C-5.
- Never call an alert proof of attendance; speech recognition can miss or misrecognize speech (C-3/C-4).
- Never include tokens or phone numbers in source, examples, logs, or committed settings; they can leak (C-1).
