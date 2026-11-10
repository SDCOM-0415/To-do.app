"""Run: python -m unittest discover -s flet_port -p 'test_*.py'"""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import storage
from models import Task


class StorageTests(unittest.TestCase):
    def test_appearance_persists_after_reload(self):
        # 模拟重启：每种主题保存到磁盘后，使用全新的读取调用验证。
        for theme in ("graphite", "paper", "blue"):
            with self.subTest(theme=theme), tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "flet-settings.json"
                with patch.object(storage, "SETTINGS_FILE", path):
                    with patch.object(storage, "migrate_legacy_data", return_value=None):
                        storage.save_settings({"theme": theme})
                        saved = json.loads(path.read_text(encoding="utf-8"))
                        self.assertEqual(saved["theme"], theme)
                        reloaded = storage.load_settings()
                        self.assertEqual(reloaded["theme"], theme)

    def test_old_theme_values_are_migrated_without_overwriting_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "flet-settings.json"
            original = '{"theme": "light", "auto_save": false}'
            path.write_text(original, encoding="utf-8")
            with patch.object(storage, "SETTINGS_FILE", path):
                with patch.object(storage, "migrate_legacy_data", return_value=None):
                    self.assertEqual(storage.load_settings()["theme"], "paper")
                    self.assertFalse(storage.load_settings()["auto_save"])
                    self.assertEqual(path.read_text(encoding="utf-8"), original)
                    storage.save_settings({"theme": "system"})
                    self.assertEqual(storage.load_settings()["theme"], "graphite")

    def test_json_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tasks.json"
            with patch.object(storage, "TASKS_FILE", path):
                task = Task(id="", title="测试任务", description="note", tags=["tag"])
                storage.save_tasks([task])
                result = storage.load_tasks()
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0].title, task.title)
                self.assertEqual(result[0].tags, ["tag"])

    def test_existing_data_not_overwritten_by_migration(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            original = root / "tasks.json"
            original.write_text(json.dumps([Task(id="", title="existing").to_dict()]))
            with patch.object(storage, "TASKS_FILE", original):
                with patch.object(storage, "_legacy_directories", return_value=[]):
                    storage.migrate_legacy_data()
                self.assertEqual(storage.load_tasks()[0].title, "existing")

    def test_migration_copies_and_preserves_source(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            legacy = root / "legacy"
            legacy.mkdir()
            source = legacy / "tasks.json"
            source.write_text(json.dumps([{"text": "old title"}]), encoding="utf-8")
            original_text = source.read_text(encoding="utf-8")
            with patch.object(storage, "TASKS_FILE", root / "new.json"):
                with patch.object(storage, "_legacy_directories", return_value=[legacy]):
                    self.assertEqual(storage.load_tasks()[0].title, "old title")
            self.assertEqual(source.read_text(encoding="utf-8"), original_text)


if __name__ == "__main__":
    unittest.main()
