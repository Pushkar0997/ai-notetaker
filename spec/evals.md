# Evaluation record

No automated tests or target-device checks have been run in this implementation session. Do not interpret implementation checkboxes as verified behavior.

## Invariant coverage

| ID | Contract invariant | Evaluation / evidence | Status |
|---|---|---|---|
| EV-1 | C-1 local capture; no raw audio | Inspect runtime data flow; then observe session folder during smoke | PENDING |
| EV-2 | C-2 bounded queue; one model | Inspect `maxsize=32` and one `OfflineTranscriber`; measure target PC | PENDING |
| EV-3 | C-3 route/mute limitation disclosed | Review UI and README; confirm loopback on target Windows | PENDING |
| EV-4 | C-4 explicit phrase matching | Review detector; evaluate known positive/negative utterances | PENDING |
| EV-5 | C-5 local note durability | Stop a session and inspect Markdown; confirm queued segments flush | PENDING |

The note destination and in-app discovery path were changed to the Windows configured Documents folder for M1-NOTES-02. This implementation has not yet been exercised in a live app session; EV-5 remains PENDING until the target-PC smoke check confirms the file exists and contains the expected content.

## Required negative cases

- Unconfigured names must not generate name alerts.
- A Latin trigger must not match merely as a substring inside a longer unrelated word.
- An empty custom phrase must never match.
- An absent model must stop startup with an actionable error, not silently use cloud recognition.
- Audio queue overload must stay bounded; a capture failure must be visible.
- Stopping during active audio must close the note only after the transcription worker flushes queued audio.

## Gate

M0 remains OPEN until target-machine smoke outcomes and performance observations are recorded. Automated test suite status: NOT RUN. Hardware/manual suite: NOT RUN.
