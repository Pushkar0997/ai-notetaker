# Manual smoke checklist

Run on the target Windows 10/11 PC. Record OS, Python version, chosen device, model, and results in `spec/evals.md`.

## Cold start

- [ ] On a clean supported Python install, run `run_windows.bat`; package installation completes and the app window opens.
- [ ] In English, confirm first use downloads Whisper base.en once and a later session starts offline. For Hindi, confirm the bundled model loads without a download.
- [ ] Refresh lists the actual Windows loopback output and microphone sources, if present.

## Class monitoring

- [ ] Play a known English meeting recording through the selected output with meeting microphone muted; transcript text appears.
- [ ] Repeat with a known Hindi phrase and Hindi selected.
- [ ] Speak a configured name; the alert panel and local beep fire once, then are suppressed for the cooldown.
- [ ] Play attendance phrases; an attendance alert appears.
- [ ] Compare a quiet known phrase with **Automatically boost quiet audio** off and on; record whether speech becomes clearer and whether background noise causes false recognition.
- [ ] Stop during speech; the app stops capture and the Markdown note includes recognized final text.
- [ ] Confirm the exact Markdown path stays visible after Stop; **Open notes folder** opens its parent folder and the file exists there.
- [ ] Verify the session folder contains Markdown notes only and no audio recording; settings remain in `%APPDATA%\AI Notetaker`.
- [ ] Set Windows volume to zero and observe whether the device still supplies loopback; record the result. Route the meeting to another output and confirm capture follows only the selected source.

## Failure and resource behavior

- [ ] Disconnect or disable the selected device during a session; a capture error is visible and Stop/close remains responsive.
- [ ] Observe CPU and memory after startup and after at least 30 minutes; record actual values and note any queue-overrun or delay.
- [ ] Close the window during an active session; the audio stream closes and note file ends cleanly.

## Failure protocol

If an item fails, keep M0 open, record exact steps and observed output, and file a task before changing unrelated code. No deployment exists yet; rollback by restoring the prior project files from the user's own backup/version control. Do not delete the existing model folders.
