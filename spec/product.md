# Product

## Definition

AI Notetaker is a lightweight Windows assistant that listens to online class audio locally, alerts when configured names or attendance phrases are recognized, and saves timestamped transcript notes for later review.

## User and problem

The target user attends online classes on an older Windows PC (Intel 10th-generation i3, 8 GB RAM). They may be muted in the meeting and miss attendance or being called by name. Heavy cloud or LLM processing is unsuitable.

## Core promise

In the current build, after selecting the meeting's Windows output and a language, the user can monitor rendered class audio, receive a local alert for configured phrases, and review a local transcript with timestamps. The desired next language behavior is automatic English/Hindi detection when the meeting language changes, subject to low-spec performance and accuracy evaluation.

## Non-goals

- Joining or authenticating to a Google Meet, Zoom, or Teams meeting.
- Capturing sound that is not rendered to the selected device; volume-mute behavior depends on the endpoint and driver.
- A guaranteed attendance record or perfect speech recognition.
- Cloud transcription, raw audio recording, or cloud-generated summaries.
- Mobile app, Telegram bot, or background service in the current milestone.

## Success measures

1. A target-machine user can choose loopback, start, alert, stop, and open the resulting notes without a command-line workflow.
2. The app remains bounded in memory and loads one language-specific recognizer at a time: CPU-int8 Whisper base.en for English or the bundled Vosk model for Hindi. Any future auto-switch must preserve this resource boundary.
3. Meeting speech is transcribed locally with accuracy and latency measured against a known sample; English currently has a 12-second window before recognition. Loopback volume normalization must be evaluated so different reasonable playback levels produce similar recognition without clipping; low or muted output and ambiguous speech remain risks.

**Anti-metric:** Number of languages/models loaded at once. Increasing it is not progress if it makes the target PC unusable.

## Glossary

- **Loopback:** Audio rendered by a Windows output device and captured back as an input stream.
- **Transcript chunk:** English Whisper text emitted from a twelve-second window with a two-second overlap; Hindi Vosk text emitted when its endpoint finalizes an utterance. Partial hypotheses are not saved.
- **Important moment:** A transcript segment matching an attendance, configured-name, or custom phrase rule.
- **Automatic language switching:** Detecting English or Hindi from captured speech and selecting the corresponding local recognizer without requiring a manual setting change. This is a requested future capability, not implemented in the current build.
