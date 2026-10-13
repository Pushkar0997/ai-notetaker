# AI Notetaker (local, offline)

A small Windows desktop assistant for online classes. It captures rendered meeting audio through Windows audio loopback, uses one local recognizer at a time (Whisper for English and Vosk for Hindi), alerts on attendance phrases and names you configure, and saves a timestamped transcript/alert log as Markdown. It does not record or retain raw audio.

## What it can do today

- Monitor the system output device used by Google Meet, Zoom, Teams, or another app. It does not require the meeting microphone to be unmuted.
- Use an available microphone instead of system loopback.
- Transcribe English locally with CPU-int8 Whisper base.en; transcribe Hindi with the bundled small Vosk model. Only the selected language's recognizer is loaded.
- Alert in the desktop app and with a local sound for configured names and built-in attendance phrases.
- Optionally raise quiet input audio before recognition (off by default); this can also make background noise louder and did not improve the clean low-volume reference samples tested.
- Show the selected source and audio level reaching recognition, which helps identify a muted, quiet, or incorrectly routed device.
- Save transcript lines and detected moments locally as Markdown.
- Run with a bounded audio queue so a slow PC cannot consume unbounded memory. English transcription waits for a 12-second audio window and can arrive later if CPU processing falls behind; name/attendance alerts therefore are reminders, not instant notifications. Hindi Vosk emits finalized utterances.

The meeting application must render remote voices to the selected Windows output device. Muting the meeting microphone is fine when using system audio; the microphone option captures only the selected mic. Check the in-session audio level: near-silence means the selected source is not receiving useful audio. Physical speaker mute/volume-zero behavior varies by driver; changing the output route or stopping rendered audio can interrupt capture. Alerts require a recognized configured name, custom phrase, or built-in attendance phrase; arbitrary music or speech does not generate an alert. Singing is a poor transcription test. English results can take at least 12 seconds plus CPU processing to appear, and speech recognition can miss words, so use alerts as reminders rather than proof of attendance.

## Requirements

- Windows 10 or 11, Python 3.10–3.12, and a working output or microphone device.
- First English use downloads Whisper base.en weights (about 150 MB) into `%APPDATA%\AI Notetaker\models`; after download it runs offline. Hindi uses the bundled Vosk model without a download.
- Whisper inference is CPU-only with int8 weights and two CPU threads. A five-clip public reference comparison on the development PC favored Whisper for English and Vosk for Hindi; classroom speech can differ, especially with noise, overlap, or very quiet voices.

## Install and run

1. Install Python 3.11 (64-bit) and enable the Python launcher (`py`).
2. Double-click `run_windows.bat`. It creates `.venv`, installs the listed dependencies, and opens the app. Internet is needed for dependency installation and the first English Whisper model download. Hindi and subsequent English sessions run locally without sending audio to a service.
3. Select the system-audio loopback source (preselected when available), choose English or Hindi, enter the name(s) you want watched, then select **Start class session**. The selected recognizer loads first; audio capture starts after it is ready.
4. Select **Stop and save** after class. Session files are written to your Windows **Documents\AI Notetaker\sessions** folder. The app displays the exact file path and **Open notes folder** opens the folder directly. Settings remain under `%APPDATA%\AI Notetaker`.

You can also use PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Privacy and limits

Audio is processed on the computer and is not written to disk. The only model download occurs on first use; meeting audio and transcripts are not uploaded. Transcripts are saved in your Documents folder and settings/model weights in your Windows app data folder. There is no cloud transcription, meeting login, Google Meet/Zoom/Teams API integration, Telegram/phone notification, or semantic LLM summary in this version. The notes are a local transcript with important moments marked, not a generated lecture summary. Telegram is listed as follow-up work so its bot credentials and chat destination can be configured deliberately.

## Project map

- `main.py` — desktop application entry point.
- `notetaker/` — capture, offline transcription, settings, session notes, and UI.
- `detector.py` — attendance, configured name, and custom phrase matching.
- `spec/` — product, architecture, invariants, plan, tasks, and acceptance criteria.
- `THIRD_PARTY_NOTICES.md` — attribution and license information for the transcription engine and downloaded model weights.
