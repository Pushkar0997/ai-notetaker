# Tasks

## M0 — Correctness and validation

- [x] **M0-SPEC-01** — Establish product scope, architecture boundary, and correctness contract in the spec files.
- [ ] **M0-VAL-01** — Run `spec/smoke.md` on the target Windows PC and record actual evidence in `spec/evals.md`.
- [ ] **M0-PERF-01** — Observe CPU, memory, and queue behavior during a representative class session and record measured values.

## M1 — Local monitor

- [x] **M1-APP-01** — Add a Tkinter session UI in `notetaker/app.py` for source, language, watched phrases, live transcript, alert, and stop.
- [x] **M1-AUDIO-01** — Add Windows loopback/microphone capture and bounded queue handling in `notetaker/audio_capture.py` and `notetaker/app.py`.
- [x] **M1-ASR-01** — Add single-model finalized-utterance transcription in `notetaker/transcription.py`.
- [x] **M1-ALERT-01** — Replace fuzzy prototype matches with explicit configured phrases and per-trigger cooldown in `detector.py` and `notetaker/app.py`.
- [x] **M1-NOTES-01** — Save transcript and alert moments as local Markdown via `notetaker/session_notes.py`.
- [x] **M1-NOTES-02** — Save notes in the configured Documents folder, expose the exact file and folder in the UI, and report write failures.
- [x] **M1-SETUP-01** — Document setup and add Windows launcher in `README.md` and `run_windows.bat`.
- [x] **M1-CLEAN-01** — Remove obsolete prototype launchers, utilities, and unused large-model assets from the active project.
- [x] **M1-OPT-01** — Lazy-load recognition and array libraries until session start/capture in `notetaker/`.
- [x] **M1-LICENSE-01** — Preserve Vosk model attribution and Apache license when publishing bundled models.

## Backlog — do not start before M0 closes

- **M2-TELEGRAM-01** — Add explicit opt-in Telegram bot/chat settings, secret storage guidance, and delivery status.
- **M2-NOTES-01** — Explore extractive topic/action notes that need no second large model; keep transcript as source of truth.
- **M2-PACKAGE-01** — Produce and verify a packaged Windows build on a clean machine.
