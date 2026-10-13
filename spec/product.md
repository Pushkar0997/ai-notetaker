# Product

## Definition

AI Notetaker is a lightweight Windows assistant that listens to online class audio locally, alerts when configured names or attendance phrases are recognized, and saves timestamped transcript notes for later review.

## User and problem

The target user attends online classes on an older Windows PC (Intel 10th-generation i3, 8 GB RAM). They may be muted in the meeting and miss attendance or being called by name. Heavy cloud or LLM processing is unsuitable.

## Core promise

After selecting the meeting's Windows output and a language, the user can let the app monitor rendered class audio, receive a local alert for configured phrases, and review a local transcript with timestamps.

## Non-goals

- Joining or authenticating to a Google Meet, Zoom, or Teams meeting.
- Capturing sound that is not rendered to the selected device; volume-mute behavior depends on the endpoint and driver.
- A guaranteed attendance record or perfect speech recognition.
- Cloud transcription, raw audio recording, or cloud-generated summaries.
- Mobile app, Telegram bot, or background service in the current milestone.

## Success measures

1. A target-machine user can choose loopback, start, alert, stop, and open the resulting notes without a command-line workflow.
2. The app remains bounded in memory and loads one small Vosk model.
3. Meeting speech is transcribed locally when the selected route supplies clear audio.

**Anti-metric:** Number of languages/models loaded at once. Increasing it is not progress if it makes the target PC unusable.

## Glossary

- **Loopback:** Audio rendered by a Windows output device and captured back as an input stream.
- **Final segment:** Vosk text emitted after an utterance boundary; partial hypotheses are not saved.
- **Important moment:** A transcript segment matching an attendance, configured-name, or custom phrase rule.
