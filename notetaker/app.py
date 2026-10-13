"""Tkinter desktop interface for the local AI Notetaker."""

from __future__ import annotations

import os
import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from detector import Detector

from .audio_capture import AudioCapture, AudioDevice, list_audio_devices
from .config import AUDIO_QUEUE_BLOCKS, SAMPLE_RATE, load_config, notes_dir, save_config
from .session_notes import SessionNotes
from .transcription import OfflineTranscriber


class NotetakerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AI Notetaker · Offline class monitor")
        self.root.geometry("850x690")
        self.root.minsize(700, 560)
        self.config = load_config()
        self.devices: list[AudioDevice] = []
        self.audio: AudioCapture | None = None
        self.notes: SessionNotes | None = None
        self.audio_queue: queue.Queue = queue.Queue(maxsize=AUDIO_QUEUE_BLOCKS)
        self.ui_queue: queue.Queue = queue.Queue()
        self.stop_worker = threading.Event()
        self.cooldowns: dict[tuple[str, str], float] = {}
        self.active = False
        self.stopping = False
        self.closing = False
        self.audio_drops = 0
        self.capture_failed = False
        self.input_level_dbfs: float | None = None
        self.notes_failed = False
        self.notes_error_reported = False
        self.transcript_line_count = 0
        self._build_ui()
        self.refresh_devices()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.after(100, self._drain_ui_events)

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=16)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="AI Notetaker", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(
            outer,
            text="Offline class audio monitor · audio and notes stay on this PC",
            foreground="#555555",
        ).pack(anchor="w", pady=(0, 12))

        settings = ttk.LabelFrame(outer, text="Session settings", padding=10)
        settings.pack(fill="x")
        settings.columnconfigure(1, weight=1)
        ttk.Label(settings, text="Audio source").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        self.device_var = tk.StringVar()
        self.device_combo = ttk.Combobox(settings, textvariable=self.device_var, state="readonly")
        self.device_combo.grid(row=0, column=1, sticky="ew", pady=4)
        ttk.Button(settings, text="Refresh", command=self.refresh_devices).grid(row=0, column=2, padx=(8, 0))

        ttk.Label(settings, text="Recognition language").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        self.language_var = tk.StringVar(value=self.config.get("language", "english"))
        self.language_combo = ttk.Combobox(settings, textvariable=self.language_var, values=("english", "hindi"), state="readonly", width=16)
        self.language_combo.grid(row=1, column=1, sticky="w", pady=4)
        ttk.Label(settings, text="English: Whisper · Hindi: Vosk · both run locally.", foreground="#555555").grid(row=1, column=2, sticky="w", padx=(8, 0))

        ttk.Label(settings, text="Your name(s)").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=4)
        self.names_var = tk.StringVar(value=", ".join(self.config.get("names", [])))
        ttk.Entry(settings, textvariable=self.names_var).grid(row=2, column=1, sticky="ew", pady=4)
        ttk.Label(settings, text="Comma separated; leave blank to disable name alerts.", foreground="#555555").grid(row=2, column=2, sticky="w", padx=(8, 0))

        ttk.Label(settings, text="Extra alert phrases").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=4)
        self.phrases_var = tk.StringVar(value=", ".join(self.config.get("custom_phrases", [])))
        ttk.Entry(settings, textvariable=self.phrases_var).grid(row=3, column=1, sticky="ew", pady=4)
        ttk.Label(settings, text="Attendance phrases are built in.", foreground="#555555").grid(row=3, column=2, sticky="w", padx=(8, 0))

        self.auto_gain_var = tk.BooleanVar(value=self.config.get("auto_gain", False))
        ttk.Checkbutton(
            settings,
            text="Automatically boost quiet audio",
            variable=self.auto_gain_var,
        ).grid(row=4, column=1, sticky="w", pady=4)
        ttk.Label(settings, text="Off by default; may raise noise or hurt clarity.", foreground="#555555").grid(row=4, column=2, sticky="w", padx=(8, 0))

        controls = ttk.Frame(outer)
        controls.pack(fill="x", pady=12)
        self.start_button = ttk.Button(controls, text="Start class session", command=self.start)
        self.start_button.pack(side="left")
        self.stop_button = ttk.Button(controls, text="Stop and save", command=self.stop, state="disabled")
        self.stop_button.pack(side="left", padx=8)
        ttk.Button(controls, text="Open notes folder", command=self.open_notes_folder).pack(side="left", padx=(0, 8))
        self.status_var = tk.StringVar(value="Ready · choose the audio output used by your meeting app")
        ttk.Label(controls, textvariable=self.status_var, wraplength=520).pack(side="left", padx=10)
        self.level_var = tk.StringVar(value="Audio to recognizer: waiting for session")
        ttk.Label(outer, textvariable=self.level_var, foreground="#555555").pack(anchor="w", pady=(0, 4))
        self.notes_var = tk.StringVar(value=f"Session notes folder: {notes_dir()}")
        ttk.Label(outer, textvariable=self.notes_var, foreground="#555555", wraplength=810).pack(anchor="w", pady=(0, 8))

        self.alert_var = tk.StringVar(value="No alerts yet")
        self.alert_label = ttk.Label(outer, textvariable=self.alert_var, padding=10, background="#eef2f5")
        self.alert_label.pack(fill="x", pady=(0, 10))

        transcript_frame = ttk.LabelFrame(outer, text="Live transcript", padding=8)
        transcript_frame.pack(fill="both", expand=True)
        self.transcript = tk.Text(transcript_frame, wrap="word", state="disabled", font=("Segoe UI", 10))
        scroll = ttk.Scrollbar(transcript_frame, command=self.transcript.yview)
        self.transcript.configure(yscrollcommand=scroll.set)
        self.transcript.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        ttk.Label(
            outer,
            text="System audio captures sound rendered to the selected Windows output; microphone captures only that input device. Muting your meeting microphone is fine when using system audio. Alerts need a recognized configured name, custom phrase, or attendance phrase. Singing is a poor speech test.",
            foreground="#555555", wraplength=810,
        ).pack(anchor="w", pady=(4, 0))

    def refresh_devices(self) -> None:
        try:
            self.devices = list_audio_devices()
        except Exception as exc:
            self.devices = []
            self.status_var.set(f"Audio device discovery failed: {exc}")
            return
        self.device_combo["values"] = [device.label for device in self.devices]
        if self.devices:
            selected = next((
                i for i, device in enumerate(self.devices)
                if device.name == self.config.get("audio_device")
                and device.is_loopback == self.config.get("audio_is_loopback", True)
            ), next((i for i, device in enumerate(self.devices) if device.is_loopback), 0))
            self.device_combo.current(selected)
            self.status_var.set("Ready · system audio loopback selected when available")
        else:
            self.status_var.set("No audio inputs found · connect or enable an audio device")

    def start(self) -> None:
        if self.active:
            return
        index = self.device_combo.current()
        if index < 0 or index >= len(self.devices):
            messagebox.showerror("Audio source needed", "Choose an audio source before starting.")
            return
        language = self.language_var.get().strip().lower()
        if language not in {"english", "hindi"}:
            messagebox.showerror("Language needed", "Choose English or Hindi before starting.")
            return

        self.config.update({
            "language": language,
            "names": self._split(self.names_var.get()),
            "custom_phrases": self._split(self.phrases_var.get()),
            "audio_device": self.devices[index].name,
            "audio_is_loopback": self.devices[index].is_loopback,
            "auto_gain": self.auto_gain_var.get(),
        })
        try:
            save_config(self.config)
            notes = SessionNotes()
        except OSError as exc:
            messagebox.showerror("Cannot save session", f"Could not prepare local settings or notes: {exc}")
            return
        detector = Detector(self.config["names"], self.config["custom_phrases"])
        self.notes = notes
        self.notes_failed = False
        self.notes_error_reported = False
        self.notes_var.set(f"Session note: {self.notes.path}")
        self.stop_worker.clear()
        self.audio_drops = 0
        self.capture_failed = False
        self.input_level_dbfs = None
        self.level_var.set("Audio to recognizer: waiting for audio capture")
        self.cooldowns.clear()
        self.transcript.configure(state="normal")
        self.transcript.delete("1.0", "end")
        self.transcript.configure(state="disabled")
        self.transcript_line_count = 0
        self.audio_queue = queue.Queue(maxsize=AUDIO_QUEUE_BLOCKS)
        worker = threading.Thread(target=self._transcribe, args=(language, detector), name="transcription", daemon=True)
        worker.start()
        device = self.devices[index]
        self.audio = AudioCapture(
            device.device_id,
            self._queue_audio,
            self._capture_error,
            auto_gain=self.config["auto_gain"],
            on_level=self._capture_level,
        )
        self.active = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_var.set(f"Starting local {language.title()} recognizer · {device.label}")
        self._append_transcript("[Preparing local recognizer. Audio capture starts after it is ready; raw audio is not saved.]")

    @staticmethod
    def _split(value: str) -> list[str]:
        return [item.strip() for item in value.split(",") if item.strip()]

    def _queue_audio(self, pcm: bytes) -> None:
        try:
            self.audio_queue.put_nowait(pcm)
        except queue.Full:
            # Keep the most recent sound; an overloaded old PC should not grow memory without bound.
            try:
                self.audio_queue.get_nowait()
                self.audio_queue.put_nowait(pcm)
                self.audio_drops += 1
                if self.audio_drops == 1 or self.audio_drops % 20 == 0:
                    self.ui_queue.put(("overrun", self.audio_drops))
            except (queue.Empty, queue.Full):
                pass

    def _capture_error(self, error: str) -> None:
        self.stop_worker.set()
        self.ui_queue.put(("error", error))

    def _capture_level(self, dbfs: float) -> None:
        self.ui_queue.put(("input_level", dbfs))

    def _transcribe(self, language: str, detector: Detector) -> None:
        try:
            engine = "Whisper" if language == "english" else "Vosk"
            status = "Loading local Whisper model · first use downloads it once" if language == "english" else "Loading local Hindi model"
            self.ui_queue.put(("status", status))
            transcriber = OfflineTranscriber(language, SAMPLE_RATE)
            self.ui_queue.put(("recognizer_ready", engine, language))
            while not self.stop_worker.is_set() or not self.audio_queue.empty():
                try:
                    pcm = self.audio_queue.get(timeout=0.2)
                except queue.Empty:
                    continue
                self._publish_text(transcriber.accept(pcm), detector)
            self._publish_text(transcriber.finish(), detector)
        except Exception as exc:
            self.stop_worker.set()
            self.ui_queue.put(("error", f"Transcription failed: {exc}"))
            self.capture_failed = True
        finally:
            self.ui_queue.put(("worker_done",))

    def _publish_text(self, text: str, detector: Detector) -> None:
        if not text:
            return
        self.ui_queue.put(("transcript", text))
        detections = detector.detect(text)
        if detections:
            self.ui_queue.put(("alerts", detections, text))

    def _drain_ui_events(self) -> None:
        try:
            while True:
                event = self.ui_queue.get_nowait()
                if event[0] == "transcript":
                    self._append_transcript(event[1])
                    if self.notes:
                        try:
                            self.notes.add_transcript(event[1])
                        except OSError as exc:
                            self._report_notes_error(exc)
                elif event[0] == "alerts":
                    self._handle_alerts(*event[1:])
                elif event[0] == "error":
                    self.capture_failed = True
                    self.status_var.set(f"Session error: {event[1]}")
                    self._append_transcript(f"[Session error: {event[1]}]")
                elif event[0] == "status":
                    self.status_var.set(event[1])
                elif event[0] == "recognizer_ready":
                    if self.active and not self.stop_worker.is_set() and self.audio:
                        self.audio.start()
                        index = self.device_combo.current()
                        device_label = self.devices[index].label if 0 <= index < len(self.devices) else "selected device"
                        self.status_var.set(f"Listening · {device_label} · local {event[1]} {event[2].title()} model")
                        self._append_transcript("[Audio capture started.]")
                elif event[0] == "overrun":
                    self.status_var.set(f"Audio overloaded: dropped {event[1]} old blocks. Recognition may miss words.")
                elif event[0] == "input_level":
                    self.input_level_dbfs = event[1]
                    if event[1] < -55:
                        label = "very quiet · check source, mute, and volume"
                    elif event[1] < -38:
                        label = "quiet · try the input gain option if speech is unclear"
                    else:
                        label = "audio detected"
                    self.level_var.set(f"Audio to recognizer: {event[1]:.0f} dBFS · {label}")
                elif event[0] == "worker_done":
                    if self.audio:
                        self.audio.stop()
                        self.audio = None
                    self.active = False
                    self.stop_button.configure(state="disabled")
                    if self.notes:
                        try:
                            self.notes.close()
                        except OSError as exc:
                            self._report_notes_error(exc)
                        self.notes = None
                    self.stopping = False
                    self.start_button.configure(state="normal")
                    if self.notes_failed:
                        self.status_var.set("Stopped · notes could not be fully saved; see the error message")
                    elif self.capture_failed:
                        self.status_var.set("Stopped after capture/transcription error · notes saved locally")
                    else:
                        self.status_var.set("Session stopped · notes saved locally")
                    if self.closing:
                        self.root.destroy()
                        return
        except queue.Empty:
            pass
        self.root.after(100, self._drain_ui_events)

    def _handle_alerts(self, detections, text: str) -> None:
        import time

        now = time.monotonic()
        cooldown = min(3600, max(1, int(self.config.get("alert_cooldown_seconds", 30))))
        fresh = []
        for detection in detections:
            key = (detection.category, detection.phrase.casefold())
            if now - self.cooldowns.get(key, 0) >= cooldown:
                self.cooldowns[key] = now
                fresh.append(detection)
        if not fresh:
            return
        labels = ", ".join(f"{item.category}: {item.phrase}" for item in fresh)
        self.alert_var.set(f"{labels} · {text}")
        self.alert_label.configure(background="#ffe7a3")
        if self.notes:
            try:
                for item in fresh:
                    self.notes.add_alert(item.category, item.phrase, text)
            except OSError as exc:
                self._report_notes_error(exc)
        self._play_alert()

    def _report_notes_error(self, error: OSError) -> None:
        self.notes_failed = True
        if self.notes_error_reported:
            return
        self.notes_error_reported = True
        path = self.notes.path if self.notes else notes_dir()
        detail = f"Could not write session notes at {path}: {error}"
        self.status_var.set("Notes could not be fully saved")
        self._append_transcript(f"[Notes save error: {error}]")
        messagebox.showerror("Notes could not be saved", detail)

    def open_notes_folder(self) -> None:
        folder = notes_dir()
        try:
            folder.mkdir(parents=True, exist_ok=True)
            if os.name == "nt":
                os.startfile(str(folder))
            else:
                import webbrowser
                webbrowser.open(folder.as_uri())
        except OSError as exc:
            messagebox.showerror("Cannot open notes folder", f"Could not open {folder}: {exc}")

    def _play_alert(self) -> None:
        if not self.config.get("alert_sound", True):
            return
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except (ImportError, RuntimeError):
            self.root.bell()

    def _append_transcript(self, text: str) -> None:
        self.transcript.configure(state="normal")
        self.transcript.insert("end", text.strip() + "\n")
        self.transcript.see("end")
        self.transcript_line_count += 1
        if self.transcript_line_count > 500:
            self.transcript.delete("1.0", "101.0")
            self.transcript_line_count = 400
        self.transcript.configure(state="disabled")

    def stop(self) -> None:
        if not self.active:
            return
        self.active = False
        self.stopping = True
        self.status_var.set("Stopping audio capture and finishing notes…")
        self.stop_button.configure(state="disabled")
        if self.audio:
            self.audio.stop()
            self.audio = None
        self.stop_worker.set()

    def close(self) -> None:
        self.closing = True
        if self.active:
            self.stop()
        elif self.stopping:
            return
        else:
            self.root.destroy()


def run_app() -> None:
    root = tk.Tk()
    NotetakerApp(root)
    root.mainloop()
