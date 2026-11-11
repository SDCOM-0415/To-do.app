"""Todo App shared per-user storage and Tk edition settings."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any

from platformdirs import user_data_path


class Config:
    def __init__(self):
        self.app_name = "Todo App v0.3.2"
        self.version = "0.3.2"

        # Shared task storage for Tk and Flet; UI preferences stay edition-specific.
        self.config_dir = Path(user_data_path("TodoApp", "SDCOM", ensure_exists=True))
        self.config_file = self.config_dir / "tk-config.json"
        self.tasks_file = self.config_dir / "tasks.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.default_config = {
            "theme": "system",
            "ui_layout": "classic",
            "font_mode": "harmony",
            "window_size": "900x700",
            "window_position": "center",
            "auto_save": True,
            "show_completed": True,
            "show_statistics": True,
            "confirm_delete": True,
            "font_size": 14,
            "language": "zh-cn",
            "priority_colors": {
                "高": "#ff4444",
                "中": "#ffaa00",
                "低": "#44ff44",
            },
        }

        self.migrate_legacy_files()
        self.config = self.load_config()

    @staticmethod
    def _legacy_directories() -> list[Path]:
        candidates = [Path(__file__).resolve().parent]
        if getattr(sys, "frozen", False):
            candidates.extend([
                Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent)).resolve(),
                Path(sys.executable).resolve().parent,
            ])
            if sys.platform == "darwin":
                contents = Path(sys.executable).resolve().parent.parent
                candidates.extend([contents / "Frameworks", contents / "Resources"])
        result: list[Path] = []
        for candidate in candidates:
            if candidate not in result:
                result.append(candidate)
        return result

    def migrate_legacy_files(self) -> None:
        """Copy legacy bundle-local JSON files once; never modify their originals."""
        migrations = (
            ("config.json", self.config_file, dict),
            ("tasks.json", self.tasks_file, list),
        )
        for legacy_name, destination, expected_type in migrations:
            if destination.exists():
                continue
            for directory in self._legacy_directories():
                source = directory / legacy_name
                if not source.is_file() or source.resolve() == destination.resolve():
                    continue
                try:
                    payload = json.loads(source.read_text(encoding="utf-8"))
                    if not isinstance(payload, expected_type):
                        continue
                    # Validate task rows before copying a legacy task file.
                    if legacy_name == "tasks.json":
                        if not all(isinstance(item, dict) for item in payload):
                            continue
                    shutil.copy2(source, destination)
                    print(f"已迁移旧数据: {source} -> {destination}")
                    break
                except (OSError, ValueError, TypeError) as exc:
                    print(f"迁移旧文件失败 {source}: {exc}")

    def load_config(self) -> dict[str, Any]:
        config = self.default_config.copy()
        config["priority_colors"] = self.default_config["priority_colors"].copy()
        if self.config_file.exists():
            try:
                loaded = json.loads(self.config_file.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    config.update(loaded)
            except (OSError, ValueError, TypeError) as exc:
                print(f"加载配置失败: {exc}")
        return config

    def save_config(self) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        temp_file = self.config_file.with_suffix(".json.tmp")
        try:
            temp_file.write_text(
                json.dumps(self.config, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            temp_file.replace(self.config_file)
        except OSError as exc:
            print(f"保存配置失败: {exc}")
            if temp_file.exists():
                temp_file.unlink()

    def get(self, key: str, default=None):
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.config[key] = value
        self.save_config()

    def get_priority_color(self, priority: str) -> str:
        colors = self.config.get("priority_colors", self.default_config["priority_colors"])
        return colors.get(priority, "#ffaa00")


app_config = Config()
