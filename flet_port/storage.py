"""Portable task storage for the experimental Flet UI.

Data is copied from the legacy directory once. Never overwrite legacy files.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from platformdirs import user_data_path
from models import Task

APP_DIR = Path(user_data_path("TodoApp", "SDCOM", ensure_exists=True))
TASKS_FILE = APP_DIR / "tasks.json"
SETTINGS_FILE = APP_DIR / "flet-settings.json"
DEFAULT_SETTINGS = {"theme": "system", "show_completed": True, "sort": "created_at"}


def _legacy_directories() -> list[Path]:
    base = Path(__file__).resolve().parent.parent
    dirs = [base]
    if getattr(sys, "frozen", False):
        dirs.append(Path(sys.executable).resolve().parent)
    return dirs


def migrate_legacy_data() -> None:
    """Only import old tasks when this version has no task file."""
    if TASKS_FILE.exists():
        return
    for directory in _legacy_directories():
        source = directory / "tasks.json"
        if source.is_file():
            # Validate before importing; malformed old data must not clobber a new file.
            raw = json.loads(source.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                raise ValueError("Legacy tasks.json must contain a JSON array")
            save_tasks([Task.from_dict(dict(item)) for item in raw])
            return


def _atomic_json_write(target: Path, data: Any) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=target.name + ".", suffix=".tmp", dir=target.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, target)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def load_tasks() -> list[Task]:
    migrate_legacy_data()
    if not TASKS_FILE.exists():
        return []
    raw = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("tasks.json must contain a JSON array")
    return [Task.from_dict(dict(item)) for item in raw]


def save_tasks(tasks: list[Task]) -> None:
    _atomic_json_write(TASKS_FILE, [task.to_dict() for task in tasks])


def load_settings() -> dict[str, Any]:
    settings = dict(DEFAULT_SETTINGS)
    if SETTINGS_FILE.exists():
        raw = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            settings.update({key: raw[key] for key in DEFAULT_SETTINGS if key in raw})
    else:
        # One-time transfer of key UI preferences from the old configuration.
        for directory in _legacy_directories():
            old = directory / "config.json"
            if old.is_file():
                try:
                    raw = json.loads(old.read_text(encoding="utf-8"))
                    for key in ("theme", "show_completed"):
                        if key in raw:
                            settings[key] = raw[key]
                except (OSError, ValueError, TypeError):
                    pass
                break
    return settings


def save_settings(settings: dict[str, Any]) -> None:
    _atomic_json_write(SETTINGS_FILE, {k: settings[k] for k in DEFAULT_SETTINGS})
