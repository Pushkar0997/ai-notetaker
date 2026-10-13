# AI Notetaker — brief

**Product:** A lightweight Windows desktop assistant that listens to rendered class audio locally, marks configured name/attendance phrases, and saves transcript notes without retaining raw audio.

**Current milestone:** M0 — target-machine validation (OPEN). The desktop path is implemented; behavior has not been exercised on the user's audio devices or old PC.

**Last done:** Replaced the prototype's console entry points with a Tkinter session app, local SoundCard loopback/microphone capture, English CPU-int8 Whisper base.en and Hindi bundled Vosk recognition (one engine per session), optional quiet-audio gain, phrase alerts, bounded buffering, and local Markdown notes. English Whisper weights download once to the user's AppData cache.

**Next task:** M0-VAL-01 — run the manual checklist in `spec/smoke.md` on the target Windows machine and record each outcome in `spec/evals.md`.

**Next-session prompt:** Read `AGENTS.md`, `CONTRACT.md`, `spec/architecture.md`, `spec/plan.md`, `spec/tasks.md`, and the top entry of `AGENT_LOG.md`. Continue M0-VAL-01 by following `spec/smoke.md`; do not mark an item PASS without observing it on the target machine.

**Most likely to break:** Windows loopback device discovery; Whisper throughput and transcript delay on the target i3; English model download availability on first use; meeting output routing when the selected system device changes.

**Spec consistency:** `python scripts/spec_lint.py` checks the required spec set and invariant/evaluation links.

Details: `README.md` for users; `spec/` for product, architecture, plan, tasks, evaluations, smoke steps, and decisions; `CONTRACT.md` for invariants.
