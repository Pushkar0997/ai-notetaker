# Agent log

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
