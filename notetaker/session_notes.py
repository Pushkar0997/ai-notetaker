"""Append transcript, detections, and lightweight class notes to a local Markdown file."""

from __future__ import annotations

from datetime import datetime

from .config import data_dir


class SessionNotes:
    def __init__(self, title: str = "Class session"):
        stamp = datetime.now().astimezone()
        directory = data_dir() / "sessions"
        directory.mkdir(parents=True, exist_ok=True)
        base = f"{stamp:%Y-%m-%d_%H-%M-%S}"
        suffix = 1
        while True:
            candidate = directory / (f"{base}.md" if suffix == 1 else f"{base}-{suffix:02d}.md")
            try:
                with candidate.open("x", encoding="utf-8") as notes:
                    notes.write(
                        f"# {title.strip() or 'Class session'}\n\n"
                        f"Started: {stamp:%Y-%m-%d %H:%M:%S %Z}\n\n"
                        "## Class notes and transcript\n\n"
                    )
                self.path = candidate
                break
            except FileExistsError:
                suffix += 1

    def add_transcript(self, text: str) -> None:
        if text.strip():
            stamp = datetime.now().astimezone().strftime("%H:%M:%S")
            with self.path.open("a", encoding="utf-8") as notes:
                notes.write(f"- [{stamp}] {text.strip()}\n")

    def add_alert(self, category: str, phrase: str, text: str) -> None:
        stamp = datetime.now().astimezone().strftime("%H:%M:%S")
        with self.path.open("a", encoding="utf-8") as notes:
            notes.write(f"\n> **{category.title()} alert · {stamp}:** “{phrase}”\n")
            if text.strip():
                notes.write(f"> Heard: {text.strip()}\n")

    def close(self) -> None:
        stamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
        with self.path.open("a", encoding="utf-8") as notes:
            notes.write(f"\n\nStopped: {stamp}\n")
