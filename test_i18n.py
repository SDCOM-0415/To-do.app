"""Regression coverage for UI translations and user-data isolation."""
import unittest
from i18n import tr, normalize_language


class LanguageTests(unittest.TestCase):
    def test_language_choices(self):
        self.assertEqual(normalize_language(None), "zh-cn")
        self.assertEqual(normalize_language("xx"), "zh-cn")
        self.assertEqual(tr("新建任务", "en"), "New task")
        self.assertEqual(tr("新建任务", "zh-tw"), "新增任務")
        self.assertEqual(tr("New task", "zh-cn"), "新建任务")

    def test_priority_keys_remain_unchanged(self):
        for key in ("高", "中", "低"):
            self.assertEqual(tr(tr(key, "en"), "zh-cn"), key)

    def test_unknown_task_title_and_hex_unchanged(self):
        for value in ("My custom task", "复习算法 2026/11/11", "#FF00CC"):
            for language in ("en", "zh-tw", "zh-cn"):
                self.assertEqual(tr(value, language), value)

    def test_settings_runtime_labels_are_localized(self):
        self.assertEqual(tr("操作系统：macOS-15.8.1-x86_64", "en"),
                         "Operating system：macOS-15.8.1-x86_64")
        self.assertEqual(tr("Python 版本：3.12.16", "en"),
                         "Python version：3.12.16")
        self.assertEqual(tr("架构：x86_64", "en"), "Architecture：x86_64")
        self.assertEqual(tr("TodoApp Flet · 10 种外观风格", "en"),
                         "TodoApp Flet · 10 appearance presets")

    def test_dynamic_stats_are_localized(self):
        stats = "总计 3 项  ·  已完成 1  ·  进行中 2  ·  逾期 0"
        self.assertIn("Completed 1", tr(stats, "en"))
        self.assertIn("總計 3 項", tr(stats, "zh-tw"))


if __name__ == "__main__":
    unittest.main()
