# Agent log

## 2026-10-13 — Desktop — Compare and tune local speech recognition

**Milestone:** M0 — target-machine correctness and validation (OPEN)
**Tasks attempted:** M1-ASR-02, EV-6, EV-7
**Landed:** Compared Vosk and CPU-int8 Whisper on public English/Hindi references on the i3-1005G1 / 7.8 GiB target PC. Selected Whisper base.en with 12-second windows for English and bundled Vosk for Hindi; removed the unused English Vosk model. Added the PyAV compatibility pin, made auto gain opt-in, and delayed capture until the recognizer is ready.
**Did not land:** Broad classroom/noise evaluation, live loopback test, or peak CPU/RAM measurement.
**Blockers:** Live class audio and device routing still require the user's manual smoke check.
**Spec changes:** Updated decisions, evaluation, architecture, user docs, and task record with the measured results and their limits.
**Next action:** Run `spec/smoke.md` during a short meeting and record transcript quality, alert delay, and device behavior.

## 2026-10-13 — Desktop — Make saved notes discoverable and report write failures

**Milestone:** M1 — local monitor implementation (validation pending)
**Tasks attempted:** M1-NOTES-02
**Landed:** Moved session Markdown from hidden AppData to the Windows configured Documents folder; added an in-app folder opener and exact active-note path; made note write/close errors visible. Kept settings in AppData and raw audio out of storage.
**Did not land:** Recovery of the earlier session file; the expected old AppData session folder was absent. No live Windows app or audio session was run for this change.
**Blockers:** User must rerun a short session to observe the target PC's configured Documents location and confirm a Markdown file is created there.
**Spec changes:** Updated C-5, architecture, README, smoke checklist, tasks, and evaluation status to match the new destination.
**Next action:** Run the updated smoke checklist on the target Windows PC; verify the app's displayed path, folder button, and saved file.

## 2026-10-13 — Desktop — M1 cleanup and optimization

**Milestone:** M1 — local monitor implementation (validation pending)
**Tasks attempted:** M1-CLEAN-01, M1-OPT-01, M1-LICENSE-01
**Landed:** Removed obsolete console prototypes and legacy utilities; removed the unused 5.6 GB large-model folder, old model archives, and alert asset; lazy-loaded Vosk/NumPy in the session path; added Vosk model attribution and Apache 2.0 license text. Kept the two small models required by the app.
**Did not land:** Runtime or target-PC performance verification; the application remains a local desktop prototype, not a packaged installer.
**Blockers:** No test execution per project rules and no Windows audio session was observed.
**Noticed, did not fix:** Audio overrun drops the oldest buffered blocks, so recognition can miss words under sustained CPU pressure. Windows device behavior and performance remain unverified.
**Spec changes:** Updated directory rules, performance budget, and release notes.
**Next action:** M0-VAL-01, run `spec/smoke.md` on the target PC and record results.

## 2026-10-13 — Codex / Desktop — M0 and M1

**Milestone:** M0 — correctness and target-machine validation (OPEN); M1 — local monitor path (implementation present, validation pending)
**Tasks attempted:** M0-SPEC-01, M1-APP-01, M1-AUDIO-01, M1-ALERT-01, M1-NOTES-01, M1-SETUP-01
**Landed:** Specs, local desktop application flow, bounded capture queue, selected-language Vosk transcriber, explicit phrase detector, local notes, and Windows launcher.
**Did not land:** Telegram/phone notifications, semantic generated lecture summaries, installer/package, device-specific verification.
**Blockers:** No target-PC audio hardware is available in this session; no app launch or test suite was run.
**Noticed, did not fix:** Prototype-only audio modules, model manager, debug tools, and model zip files remain in the tree; compatibility launchers use the new app but those old modules are not part of the main flow. Audio overrun drops the oldest buffered blocks, so recognition can miss words under sustained CPU pressure.
**Spec changes:** Created `AGENTS.md`, `CONTRACT.md`, and `spec/`; added `scripts/spec_lint.py`; revised README and requirements for the desktop app.
**Next action:** M0-VAL-01, use `spec/smoke.md` on Windows 10/11 and record actual results in `spec/evals.md`.
