"""Small, predictable phrase detector for attendance and configured names."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass


ATTENDANCE_PHRASES = (
    "attendance", "roll call", "attendance check", "present", "is present",
    "हाजिरी", "उपस्थिति", "हाजिर", "हजेरी", "उपस्थिती", "नाम पुकार",
    "haajiri", "hajiri", "upasthiti", "hajeri", "naam pukar",
)


@dataclass(frozen=True)
class Detection:
    category: str
    phrase: str


def _normalise(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"\s+", " ", value).strip()


def _contains_phrase(text: str, phrase: str) -> bool:
    phrase = _normalise(phrase)
    if not phrase:
        return False
    if any("\u0900" <= char <= "\u097f" for char in phrase):
        return phrase in text
    return re.search(r"(?<![\w])" + re.escape(phrase) + r"(?![\w])", text) is not None


class Detector:
    """Match explicit phrases; intentionally avoids fuzzy whole-sentence matches."""

    def __init__(self, names: list[str] | None = None, custom_phrases: list[str] | None = None):
        self.names = [name.strip() for name in (names or []) if name.strip()]
        self.custom_phrases = [phrase.strip() for phrase in (custom_phrases or []) if phrase.strip()]

    def detect(self, text: str) -> list[Detection]:
        normalized = _normalise(text)
        detections: list[Detection] = []
        for phrase in ATTENDANCE_PHRASES:
            if _contains_phrase(normalized, phrase):
                detections.append(Detection("attendance", phrase))
        for name in self.names:
            if _contains_phrase(normalized, name):
                detections.append(Detection("name", name))
        for phrase in self.custom_phrases:
            if _contains_phrase(normalized, phrase):
                detections.append(Detection("custom", phrase))
        # One alert per category/phrase even when the same phrase is configured twice.
        return list(dict.fromkeys(detections))
