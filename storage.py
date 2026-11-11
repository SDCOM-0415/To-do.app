"""Shared task storage and edition-specific settings for Todo App."""
from __future__ import annotations
import json, os, shutil, sys, tempfile
from pathlib import Path
from typing import Any
from platformdirs import user_data_path
from models import Task
from appearance import normalize_theme
from font_preferences import normalize_font_mode

APP_DIR = Path(user_data_path("TodoApp", "SDCOM", ensure_exists=True))
TASKS_FILE = APP_DIR / "tasks.json"
TK_SETTINGS_FILE = APP_DIR / "tk-config.json"
SETTINGS_FILE = APP_DIR / "flet-settings.json"
DEFAULT_SETTINGS: dict[str, Any] = {
    "theme": "graphite", "font_mode": "harmony", "window_size": "900x700", "window_position": "center",
    "auto_save": True, "show_completed": True, "show_statistics": True,
    "confirm_delete": True, "font_size": 14, "language": "zh-cn",
    "priority_colors": {"高": "#ff4444", "中": "#ffaa00", "低": "#44ff44"},
    "sort": "created_at",
}

def _legacy_directories() -> list[Path]:
    root = Path(__file__).resolve().parent
    candidates = [root]
    if getattr(sys, "frozen", False):
        executable = Path(sys.executable).resolve()
        candidates.extend([executable.parent, Path(getattr(sys, "_MEIPASS", executable.parent)).resolve()])
        if sys.platform == "darwin":
            contents = executable.parent.parent
            candidates.extend([contents / "Frameworks", contents / "Resources",
                Path("/Applications/TodoApp.app/Contents/Frameworks"),
                Path.home() / "Applications/TodoApp.app/Contents/Frameworks"])
    result = []
    for path in candidates:
        if path not in result:
            result.append(path)
    return result

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

def _find_legacy_file(name: str) -> Path | None:
    for directory in _legacy_directories():
        candidate = directory / name
        if candidate.is_file():
            return candidate
    return None

def migrate_legacy_data() -> None:
    """Import bundle-local legacy data only if the shared destination is absent."""
    if not TASKS_FILE.exists():
        source = _find_legacy_file("tasks.json")
        if source:
            raw = json.loads(source.read_text(encoding="utf-8"))
            if not isinstance(raw, list) or not all(isinstance(row, dict) for row in raw):
                raise ValueError("Legacy tasks.json must contain a JSON array of objects")
            tasks = [Task.from_dict(dict(row)) for row in raw]
            save_tasks(tasks)
            _atomic_json_write(APP_DIR / "migration.json", {
                "tasks_imported_from": str(source), "task_count": len(tasks)})
    if not TK_SETTINGS_FILE.exists():
        source = _find_legacy_file("config.json")
        if source:
            raw = json.loads(source.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                _atomic_json_write(TK_SETTINGS_FILE, raw)
                _atomic_json_write(APP_DIR / "tk-settings-migration.json", {
                    "settings_imported_from": str(source)})

def load_tasks() -> list[Task]:
    migrate_legacy_data()
    if not TASKS_FILE.exists():
        return []
    raw = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    if not isinstance(raw, list) or not all(isinstance(row, dict) for row in raw):
        raise ValueError("tasks.json must contain a JSON array of objects")
    return [Task.from_dict(dict(row)) for row in raw]

def save_tasks(tasks: list[Task]) -> None:
    _atomic_json_write(TASKS_FILE, [task.to_dict() for task in tasks])

def load_settings() -> dict[str, Any]:
    settings = json.loads(json.dumps(DEFAULT_SETTINGS))
    migrate_legacy_data()
    if SETTINGS_FILE.exists():
        raw = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            settings.update(raw)
    elif TK_SETTINGS_FILE.exists():
        try:
            raw = json.loads(TK_SETTINGS_FILE.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                for key in DEFAULT_SETTINGS:
                    if key in raw:
                        settings[key] = raw[key]
        except (OSError, ValueError, TypeError):
            pass
    # 兼容历史的 dark/light/system，同时保留三套新主题的选择。
    settings["theme"] = normalize_theme(settings.get("theme"))
    settings["font_mode"] = normalize_font_mode(settings.get("font_mode"))
    return settings

def save_settings(settings: dict[str, Any]) -> None:
    data = {key: settings.get(key, default) for key, default in DEFAULT_SETTINGS.items()}
    data["theme"] = normalize_theme(data.get("theme"))
    data["font_mode"] = normalize_font_mode(data.get("font_mode"))
    _atomic_json_write(SETTINGS_FILE, data)
