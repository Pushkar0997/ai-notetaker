"""Language-specific offline transcription tuned for a low-memory Windows PC."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .config import data_dir


class OfflineTranscriber:
    """Load one measured-best local recognizer for the selected language."""

    WINDOW_SECONDS = 12
    OVERLAP_SECONDS = 2

    def __init__(self, language: str, sample_rate: int = 16_000):
        if language not in {"english", "hindi"}:
            raise ValueError("Choose English or Hindi")
        self.sample_rate = sample_rate
        self.engine = "whisper" if language == "english" else "vosk"

        if self.engine == "vosk":
            self._init_vosk(language)
        else:
            self._init_whisper()

    def _init_vosk(self, language: str) -> None:
        model_path = Path(__file__).resolve().parent.parent / f"model-{language}"
        if not (model_path / "am" / "final.mdl").is_file():
            raise FileNotFoundError(f"The {language} Vosk model is missing: {model_path}")

        from vosk import KaldiRecognizer, Model

        self.model = Model(str(model_path))
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)

    def _init_whisper(self) -> None:
        from faster_whisper import WhisperModel
        import numpy as np

        self.np = np
        self.window_samples = self.WINDOW_SECONDS * self.sample_rate
        self.overlap_samples = self.OVERLAP_SECONDS * self.sample_rate
        self.buffer = np.empty(0, dtype=np.float32)
        self.previous_tokens: list[str] = []
        model_cache = data_dir() / "models"
        self.model = WhisperModel(
            "base.en",
            device="cpu",
            compute_type="int8",
            cpu_threads=2,
            num_workers=1,
            download_root=str(model_cache),
        )

    def accept(self, pcm: bytes) -> str:
        if self.engine == "vosk":
            if not self.recognizer.AcceptWaveform(pcm):
                return ""
            return json.loads(self.recognizer.Result()).get("text", "").strip()

        samples = self.np.frombuffer(pcm, dtype=self.np.int16).astype(self.np.float32) / 32768.0
        if samples.size:
            self.buffer = self.np.concatenate((self.buffer, samples))

        results = []
        while self.buffer.size >= self.window_samples:
            chunk = self.buffer[: self.window_samples]
            self.buffer = self.buffer[self.window_samples - self.overlap_samples :]
            text = self._transcribe_chunk(chunk)
            if text:
                results.append(text)
        return " ".join(results)

    def finish(self) -> str:
        if self.engine == "vosk":
            return json.loads(self.recognizer.FinalResult()).get("text", "").strip()
        if self.buffer.size < self.sample_rate // 2:
            return ""
        text = self._transcribe_chunk(self.buffer)
        self.buffer = self.np.empty(0, dtype=self.np.float32)
        return text

    def _transcribe_chunk(self, audio) -> str:
        segments, _ = self.model.transcribe(
            audio,
            language="en",
            beam_size=3,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 350, "speech_pad_ms": 150},
            condition_on_previous_text=False,
            no_speech_threshold=0.6,
        )
        text = " ".join(segment.text.strip() for segment in segments if segment.text.strip())
        if not text:
            return ""

        tokens = text.split()
        overlap = self._matching_overlap(self.previous_tokens, tokens)
        unique_text = " ".join(tokens[overlap:]).strip()
        self.previous_tokens = tokens[-12:]
        return unique_text

    @classmethod
    def _matching_overlap(cls, previous: list[str], current: list[str]) -> int:
        """Drop exact word repeats caused by the overlapping audio windows."""
        maximum = min(12, len(previous), len(current))
        for count in range(maximum, 1, -1):
            left = [cls._word_key(word) for word in previous[-count:]]
            right = [cls._word_key(word) for word in current[:count]]
            if all(left) and left == right:
                return count
        return 0

    @staticmethod
    def _word_key(word: str) -> str:
        return re.sub(r"[^\w]", "", word.casefold(), flags=re.UNICODE)
