# AI Notetaker — brief

**Product:** A lightweight Windows desktop assistant that listens to rendered class audio locally, marks configured name/attendance phrases, and saves transcript notes without retaining raw audio.

**Current milestone:** M0 — target-machine validation (OPEN). The desktop path is implemented; behavior has not been exercised on the user's audio devices or old PC.

**Last done:** Replaced the prototype's console entry points with a Tkinter session app, local SoundCard loopback/microphone capture, one-model Vosk transcription, phrase alerts, bounded buffering, and local Markdown notes. Added a Windows launcher and project specs.

**Next task:** M0-VAL-01 — run the manual checklist in `spec/smoke.md` on the target Windows machine and record each outcome in `spec/evals.md`.

**Next-session prompt:** Read `AGENTS.md`, `CONTRACT.md`, `spec/architecture.md`, `spec/plan.md`, `spec/tasks.md`, and the top entry of `AGENT_LOG.md`. Continue M0-VAL-01 by following `spec/smoke.md`; do not mark an item PASS without observing it on the target machine.

**Most likely to break:** Windows loopback device discovery; speech model performance/accuracy on 8 GB hardware; meeting output routing when the selected system device changes.

**Spec consistency:** `python scripts/spec_lint.py` checks the required spec set and invariant/evaluation links.

Details: `README.md` for users; `spec/` for product, architecture, plan, tasks, evaluations, smoke steps, and decisions; `CONTRACT.md` for invariants.
