# Decisions

## D-001 — Generic Windows audio route before platform integrations

**Status:** decided
**Decision:** Capture the selected Windows output through loopback and support microphone input. Do not authenticate to Meet, Zoom, or Teams.
**Rationale:** All three services render call audio to the desktop; a generic local route avoids credentials and service-specific maintenance.
**Rejected:** Separate integrations for each meeting platform, because that greatly expands auth/support scope and does not solve muted system output.
**Revisit if:** Target-machine loopback is unavailable or a required meeting use case cannot route audio through Windows.

## D-002 — One small model per session

**Status:** superseded by D-005
**Decision:** User selects English or Hindi; the original app loaded one included small Vosk model.
**Rationale:** This kept the original implementation small, but user testing found recognition quality inadequate.
**Rejected:** Simultaneous model evaluation and large models, due to memory and CPU cost.
**Revisit if:** Measured target PC has adequate headroom and user requests auto language switching.

## D-003 — Local transcript notes before generative summaries

**Status:** decided
**Decision:** Save finalized local transcript segments with timestamps and matched triggers; no LLM summary in M1.
**Rationale:** Transcript output is useful and auditable while requiring no additional model or network.
**Rejected:** Cloud summary, because it breaks the local-processing promise; a second local LLM, because the target PC budget is unknown.
**Revisit if:** User approves a specific local extractive summary and target-device performance is measured.

## D-004 — Names are configured, not inferred from prototype defaults

**Status:** decided
**Decision:** Leave name triggers blank until the user enters them in the app.
**Rationale:** The old README hard-coded a sample name; making it a default risks personal-data and false-alert errors.
**Rejected:** Reusing the prototype's “Pushkar Kumar” as a default.
**Revisit if:** User supplies desired default trigger names.

## D-005 — Choose recognizer by measured language quality

**Status:** decided from a small public-reference comparison; target-class validation pending
**Decision:** Use CPU-int8 Whisper `base.en` for English and the bundled small Vosk model for Hindi, loading only the selected engine. Cache English Whisper weights in the user's AppData folder.
**Rationale:** On five English LibriSpeech dummy reference clips, per-file Whisper measured 8.0% average WER versus Vosk at 19.8%. The actual streaming Whisper path measured 8.3% WER with twelve-second windows and two-second overlap; eight-second windows had repeated-word hallucinations and scored 30.3%. On five Hindi Common Voice subset clips, Vosk measured 17.0% per-file and 14.4% in the app streaming path, versus Whisper base at 96.3%; Whisper often emitted Urdu/Latin instead of Devanagari. The app-path run took 26.5 seconds for English and 14.3 seconds for Hindi, excluding model load. These small clean/read-speech samples are directional and do not represent classroom noise or overlap.
**Rejected:** Whisper base for Hindi due to measured script/accuracy failures; large Vosk server or larger Whisper models pending evidence they fit the target hardware; cloud transcription due to local-only processing.
**Revisit if:** A broader Hindi benchmark or user's own class samples show a different best recognizer, or the target i3 cannot keep up with English Whisper.

## D-006 — Treat automatic language switching as a measured follow-up

**Status:** required future capability; implementation deferred
**Decision:** The current session language remains manually selected. Evaluate window-level English/Hindi detection and switching without keeping both recognizers loaded. Do not ship auto mode until it handles language changes and code-switching acceptably on the target PC and its added delay is measured.
**Rationale:** The user cannot know the language in advance in every live meeting. The current Hindi Vosk path is responsive but has poor observed accuracy; Whisper base auto-detection was also poor on the prior small Hindi reference set. A naive switch could worsen both latency and transcript quality.
**Rejected:** Silently loading both ASR engines throughout a class, because it conflicts with the 8 GB RAM / older i3 budget.
**Revisit if:** A locally tested design passes the mixed-language accuracy, switching delay, and CPU/RAM criteria in EV-9.

## D-007 — Evaluate loopback loudness normalization before changing defaults

**Status:** evaluation required
**Decision:** Keep the existing quiet-audio gain opt-in until a controlled loopback test compares low and high Windows playback levels, transcription, and clipping. The user's desired behavior is similar recognition quality across ordinary playback volumes, but muted/near-zero output cannot be recovered by gain.
**Rationale:** Windows loopback captures the rendered system mix; attenuation changes the samples available to recognition. Gain can restore level only while usable signal remains and can amplify noise or clip. Existing public-reference attenuation results did not show a consistent recognition improvement.
**Rejected:** Claiming volume-independent capture or enabling an unmeasured gain rule by default.
**Revisit if:** EV-8 shows a safe bounded normalization improves low-level loopback without worsening ordinary-level recognition.
