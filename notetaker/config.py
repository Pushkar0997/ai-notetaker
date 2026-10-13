"""Local user configuration and application data paths."""

from __future__ import annotations

import json
import os
from pathlib import Path


APP_NAME = "AI Notetaker"
SAMPLE_RATE = 16_000
BLOCK_SECONDS = 0.25


def data_dir() -> Path:
    root = os.environ.get("APPDATA")
    base = Path(root) if root else Path.home() / ".config"
    location = base / APP_NAME
    location.mkdir(parents=True, exist_ok=True)
    return location


def default_config() -> dict:
    return {
        "language": "english",
        "names": [],
        "custom_phrases": [],
        "audio_device": "",
        "audio_is_loopback": True,
        "alert_sound": True,
        "alert_cooldown_seconds": 30,
    }


def load_config() -> dict:
    path = data_dir() / "settings.json"
    config = default_config()
    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(saved, dict):
            config.update(saved)
    except (OSError, json.JSONDecodeError):
        pass
    if config.get("language") not in {"english", "hindi"}:
        config["language"] = "english"
    for key in ("names", "custom_phrases"):
        value = config.get(key)
        if not isinstance(value, list):
            config[key] = []
        else:
            config[key] = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    if not isinstance(config.get("audio_device"), str):
        config["audio_device"] = ""
    config["audio_is_loopback"] = bool(config.get("audio_is_loopback", True))
    try:
        config["alert_cooldown_seconds"] = min(3600, max(1, int(config.get("alert_cooldown_seconds", 30))))
    except (TypeError, ValueError):
        config["alert_cooldown_seconds"] = 30
    config["alert_sound"] = bool(config.get("alert_sound", True))
    return config


def save_config(config: dict) -> None:
    path = data_dir() / "settings.json"
    temporary = path.with_name(f"settings.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)
