# AI Notetaker (local, offline)

A small Windows desktop assistant for online classes. It captures rendered meeting audio through Windows audio loopback, transcribes one language at a time with a local Vosk model, alerts on attendance phrases and names you configure, and saves a timestamped transcript/alert log as Markdown. It does not record or retain raw audio.

## What it can do today

- Monitor the system output device used by Google Meet, Zoom, Teams, or another app. It does not require the meeting microphone to be unmuted.
- Use an available microphone instead of system loopback.
- Transcribe English or Hindi offline, one model at a time, for lower CPU and memory use.
- Alert in the desktop app and with a local sound for configured names and built-in attendance phrases.
- Save transcript lines and detected moments locally as Markdown.
- Run with a bounded audio queue so a slow PC cannot consume unbounded memory.

The meeting application must render remote voices to the selected Windows output device. Muting the meeting microphone is fine. Physical speaker mute/volume-zero behavior varies by driver; changing the output route or stopping rendered audio can interrupt capture. Test your device before relying on alerts. Speech recognition can miss words; use alerts as reminders, not proof of attendance.

## Requirements

- Windows 10 or 11, Python 3.10–3.12, and a working output or microphone device.
- Included Vosk models: `model-english` and `model-hindi` (models run locally).
- Roughly 300 MB for the Python environment and both offline speech models; exact use varies by Python and dependency versions.

## Install and run

1. Install Python 3.11 (64-bit) and enable the Python launcher (`py`).
2. Double-click `run_windows.bat`. It creates `.venv`, installs the listed dependencies, and opens the app. The first install needs internet for Python packages; transcription itself works offline.
3. Select the system-audio loopback source (preselected when available), choose English or Hindi, enter the name(s) you want watched, then select **Start class session**.
4. Select **Stop and save** after class. Session files are written to your Windows **Documents\AI Notetaker\sessions** folder. The app displays the exact file path and **Open notes folder** opens the folder directly. Settings remain under `%APPDATA%\AI Notetaker`.

You can also use PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Privacy and limits

Audio is processed on the computer and is not written to disk. Transcripts are saved in your Documents folder and settings in your Windows app data folder. There is no cloud transcription, meeting login, Google Meet/Zoom/Teams API integration, Telegram/phone notification, or semantic LLM summary in this version. The notes are a local transcript with important moments marked, not a generated lecture summary. Telegram is listed as follow-up work so its bot credentials and chat destination can be configured deliberately.

## Project map

- `main.py` — desktop application entry point.
- `notetaker/` — capture, offline transcription, settings, session notes, and UI.
- `detector.py` — attendance, configured name, and custom phrase matching.
- `model-english/`, `model-hindi/` — included offline recognition models.
- `spec/` — product, architecture, invariants, plan, tasks, and acceptance criteria.
- `THIRD_PARTY_NOTICES.md` and `LICENSES/Apache-2.0.txt` — attribution and license information for bundled Vosk models.
