# Agent instructions

**Rigor:** spec-anchored. This is a local Windows audio application with concurrent capture/transcription and persistent personal notes.

## Read order

1. `CONTRACT.md` — correctness and privacy invariants.
2. `spec/architecture.md` — actual capability and technology boundary.
3. `spec/plan.md` and `spec/tasks.md` — sequence and current work.
4. Top entry of `AGENT_LOG.md` — current state.
5. `README.md` — user setup and operation.

## Rules

- Keep inference, audio processing, alert matching, and session storage local unless the user explicitly authorizes a remote feature.
- Never save raw audio by default. Store transcripts and settings only under the user's application-data directory.
- Never claim reliable attendance detection, perfect transcription, access to a meeting's private API, or capture of audio that Windows does not render.
- Use one Vosk model at a time on the target i3/8 GB machine. Keep queues bounded and stop capture cleanly.
- Update the relevant spec and `AGENT_LOG.md` with each material behavior change.
- Run `python scripts/spec_lint.py` after changing the spec files; it checks required files, unresolved placeholders, and invariant-to-evaluation links.
- Do not add real credentials to tracked files. External messaging requires user-supplied configuration and must not be enabled silently.
- Do not add `Co-Authored-By` or Codex attribution to commits. All commits, if requested, must be authored in the user's name only.
- Do not run tests unless the user asks for testing or verification. Review code paths and report unverified behavior honestly.

## Definition of done

- The app has an observable user path to start, monitor, alert, stop, and locate notes.
- The correctness invariants in `CONTRACT.md` remain true.
- User-facing claims match `spec/architecture.md` and real implementation.
- Manual and automated evaluation status is recorded; unverified hardware behavior is not rounded up to PASS.
