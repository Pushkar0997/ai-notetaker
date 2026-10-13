"""Single-model offline Vosk transcription optimized for low-memory PCs."""

from __future__ import annotations

import json
from pathlib import Path

class OfflineTranscriber:
    def __init__(self, language: str, sample_rate: int = 16_000):
        if language not in {"english", "hindi"}:
            raise ValueError("Choose English or Hindi")
        model_path = Path(__file__).resolve().parent.parent / f"model-{language}"
        if not (model_path / "am" / "final.mdl").is_file():
            raise FileNotFoundError(f"The {language} Vosk model is missing: {model_path}")
        from vosk import KaldiRecognizer, Model

        self.model = Model(str(model_path))
        self.recognizer = KaldiRecognizer(self.model, sample_rate)

    def accept(self, pcm: bytes) -> str:
        if not self.recognizer.AcceptWaveform(pcm):
            return ""
        return json.loads(self.recognizer.Result()).get("text", "").strip()

    def finish(self) -> str:
        return json.loads(self.recognizer.FinalResult()).get("text", "").strip()
