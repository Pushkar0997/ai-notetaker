"""SoundCard-based audio capture. System output loopback is the default path."""

from __future__ import annotations

import threading
from dataclasses import dataclass

from .config import BLOCK_SECONDS, SAMPLE_RATE


@dataclass(frozen=True)
class AudioDevice:
    device_id: object
    name: str
    is_loopback: bool

    @property
    def label(self) -> str:
        return f"System audio · {self.name}" if self.is_loopback else f"Microphone · {self.name}"


def list_audio_devices() -> list[AudioDevice]:
    import soundcard as sc

    devices = []
    for microphone in sc.all_microphones(include_loopback=True):
        is_loopback = bool(getattr(microphone, "isloopback", False))
        devices.append(AudioDevice(microphone.id, microphone.name, is_loopback))
    return devices


class AudioCapture:
    """Capture fixed-size mono PCM blocks in a daemon worker with bounded buffering."""

    def __init__(self, device_id: object, on_block, on_error, auto_gain: bool = False):
        self.device_id = device_id
        self.on_block = on_block
        self.on_error = on_error
        self.auto_gain = auto_gain
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._gain = 1.0

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._capture, name="audio-capture", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2.0)

    def _capture(self) -> None:
        try:
            import numpy as np
            import soundcard as sc

            microphone = sc.get_microphone(self.device_id, include_loopback=True)
            frames = int(SAMPLE_RATE * BLOCK_SECONDS)
            with microphone.recorder(samplerate=SAMPLE_RATE) as recorder:
                while not self._stop.is_set():
                    samples = recorder.record(numframes=frames)
                    if samples.ndim == 2:
                        samples = samples.mean(axis=1)
                    if self.auto_gain:
                        rms = float(np.sqrt(np.mean(samples * samples)))
                        if rms >= 0.001:
                            target_gain = min(8.0, max(1.0, 0.08 / rms))
                        else:
                            target_gain = 1.0
                        # Raise quiet input promptly, but release gain more slowly to avoid pumping.
                        smoothing = 0.5 if target_gain > self._gain else 0.15
                        self._gain += (target_gain - self._gain) * smoothing
                        samples = samples * self._gain
                    pcm = (np.clip(samples, -1.0, 1.0) * 32767).astype("int16").tobytes()
                    self.on_block(pcm)
        except Exception as exc:
            if not self._stop.is_set():
                self.on_error(str(exc))
