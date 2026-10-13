# Plan

## M0 — Correctness and target-machine validation (OPEN)

**Deliverable:** Safe, bounded local capture and verifiable behavior on the actual target machine.
**Exit criteria:**

- [ ] The smoke checklist passes on Windows using loopback and microphone modes where present.
- [ ] Notes are present after Stop and contain final transcript segments and any alert markers.
- [ ] No raw audio file appears in the session folder.
- [ ] CPU/RAM and queue behavior are observed during a representative class period; no hang or unbounded growth is observed.
- [ ] Accuracy/miss limitations are captured from a known short audio sample.

**Blocking:** none.

## M1 — Local class monitor (IMPLEMENTED; VALIDATION PENDING)

**Deliverable:** Start/stop UI, one-model English/Hindi offline transcription, loopback/mic source selection, phrase alerts, local notes.
**Exit criteria:**

- [x] User can configure language, names, and custom alert phrases.
- [x] Audio work queue has an explicit finite capacity and one recognizer is loaded.
- [x] Session notes and alert markers are written locally; raw audio is not saved.
- [ ] Target Windows setup and smoke behavior are observed (M0).

**Blocking:** M0 validation before shipping as complete.

## M2 — External alerts and release polish (BACKLOG)

**Deliverable:** User-approved notification destinations, packaged setup, improved note summaries.
**Exit criteria:** each externally visible feature has opt-in setup, credential handling, failure feedback, privacy text, and verified clean-machine behavior.
**Blocking:** M0. Do not start until the local monitor is validated.

## Anti-goals for M0/M1

- Adding both recognizers concurrently to claim multilingual auto-detection.
- Adding a cloud LLM or cloud speech service to improve summary quality.
- Calling the output an attendance guarantee.
- Adding direct meeting-app integrations before generic loopback is tested.
