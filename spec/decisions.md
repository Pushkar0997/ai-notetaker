# Decisions

## D-001 — Generic Windows audio route before platform integrations

**Status:** decided
**Decision:** Capture the selected Windows output through loopback and support microphone input. Do not authenticate to Meet, Zoom, or Teams.
**Rationale:** All three services render call audio to the desktop; a generic local route avoids credentials and service-specific maintenance.
**Rejected:** Separate integrations for each meeting platform, because that greatly expands auth/support scope and does not solve muted system output.
**Revisit if:** Target-machine loopback is unavailable or a required meeting use case cannot route audio through Windows.

## D-002 — One small model per session

**Status:** decided
**Decision:** User selects English or Hindi; load one included small Vosk model.
**Rationale:** Existing prototype evaluates two models on every audio block and also offers 1.5–1.8 GB models. That conflicts with the 8 GB target.
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
