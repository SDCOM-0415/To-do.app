"""Run: python -m unittest discover -s flet_port -p 'test_*.py'"""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import storage
from models import Task


class StorageTests(unittest.TestCase):
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
