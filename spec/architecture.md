# Architecture and capability register

## Stack

- Windows 10/11, Python 3.10–3.12, 64-bit.
- Tkinter/ttk for the desktop window (ships with standard CPython on Windows).
- SoundCard 0.4.2–0.x for WASAPI loopback and microphone capture.
- faster-whisper 1.1–1.x with CTranslate2 int8 CPU inference for English; Vosk 0.3.x small bundled Hindi model.
- PyAV 11–18 (PyAV 19 removed an argument used by the current faster-whisper release).
- NumPy 1.24–2.x for downmixing and PCM conversion.
- English `base.en` is downloaded on first use (about 148 MB); Hindi uses the bundled small Vosk model.
- `run_windows.bat` installs dependencies to an isolated `.venv` and launches `main.py`.

## Data flow

`Windows loopback/mic → SoundCard capture worker → optional bounded 8× input gain → bounded 240×0.25 s PCM queue → one selected recognizer (English: CPU-int8 Whisper base.en in 12 s windows with 2 s overlap; Hindi: bundled Vosk) → finalized transcript text → exact phrase detector → UI alert + Markdown session file`

No raw audio is persisted. Settings are stored in `%APPDATA%\AI Notetaker\`; session notes are stored in the current user's configured Documents folder under `AI Notetaker\sessions`. The UI shows the exact active note path, can open the notes folder, and reports write errors. The UI thread owns Tk widgets; capture and recognition run in background workers and communicate with the UI through queues. During capture, the UI displays the selected device and one-second RMS audio level (dBFS) sent to the recognizer. This diagnostic is transient and does not retain audio.

## Directory rules

- `main.py`: sole documented launch entry point.
- `notetaker/`: shipped app modules; keep audio, recognizer, UI, and persistence concerns isolated.
- `detector.py`: phrase rules independent of UI and audio devices.
- English Whisper weights: `%APPDATA%\AI Notetaker\models`, downloaded once from the Systran Hugging Face repository and reused locally. Hindi Vosk model: bundled under `model-hindi/`.
- `spec/`: maintained requirements and verification record.
- `THIRD_PARTY_NOTICES.md` and `LICENSES/Apache-2.0.txt`: attribution and license for bundled model assets.

## Capability register

| Capability | Status | Evidence / limit |
|---|---|---|
| Capture rendered Windows output via loopback | Implemented, target-device validation pending | `notetaker/audio_capture.py`; loopback route and volume-mute behavior depend on Windows endpoint/driver |
| Capture selected microphone | Implemented, target-device validation pending | Same capture path |
| English offline transcription | Implemented, target-device validation pending | Whisper `base.en`, CPU int8, `notetaker/transcription.py` |
| Hindi offline transcription | Implemented, target-device validation pending | Bundled small Vosk Hindi model, `notetaker/transcription.py` |
| Name alerts | Implemented | User supplies phrase(s); exact phrase match |
| Attendance alerts | Implemented | Small built-in English/Hindi phrase list; misses possible |
| Local sound and visible alert | Implemented, validation pending | Tkinter alert panel + Windows MessageBeep |
| Timestamped transcript and alert notes | Implemented, validation pending | `Documents\AI Notetaker\sessions\*.md`; exact path is visible in the UI |
| Quiet-audio gain control | Implemented, validation pending | Optional, user-toggleable, capped at 8×; can raise background noise |
| Capture-level diagnostic | Implemented, target-device validation pending | One-second RMS level reaching recognition; distinguishes near-silent input from recognizer misses |
| Google Meet/Zoom/Teams direct integration | Not supported | M2 would require separate platform/API design; generic output capture is current integration |
| Alert when output is muted/unrouted | Not supported | M2 would require a different capture route and explicit verification |
| Telegram, phone push, or SMS alert | Not supported | M2; requires credentials, network behavior, and user-configured destination |
| Semantic LLM class summary/action-item extraction | Not supported | M2; must prove CPU/RAM impact and local model feasibility |
| Installer/executable and auto-start service | Not supported | M2; requires packaging and clean-machine verification |

## Performance budget

- Load one recognizer only; English first use downloads Whisper base.en, then inference is offline. Hindi uses the bundled Vosk model.
- Audio input buffer: 240 blocks maximum, each 0.25 sec (60 seconds total; approximately 1.9 MB PCM). Drop oldest on overload and surface a warning because recognition may miss speech.
- Keep only the most recent 500 transcript lines in the UI; retain the full transcript in the local Markdown session file.
- Target: Dell Inspiron 3593, Intel Core i3-1005G1, 7.8 GiB RAM. ASR timing was measured here; peak resource use, live audio routing, and full-class stability remain unverified.
- English Whisper emits after a 12-second window advances by 10 seconds, plus inference time; this delay is a known alert limitation.

## Security/privacy

- No network operation is part of runtime transcription/alerting.
- Persist settings under the current user's app-data directory and transcript text/detections under the current user's Documents directory. Both remain local; do not silently redirect data to a network service.
- Treat transcript text as sensitive; user controls deletion via Explorer.
- External messages are prohibited until the user configures an integration and destination.
