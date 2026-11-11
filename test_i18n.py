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


    def test_user_flet_text_is_not_translated(self):
        from localize_flet import localize_flet

        class Text:
            _i18n_skip = True

            def __init__(self):
                self.value = "设置"

        control = Text()
        localize_flet(control, "en")
        self.assertEqual(control.value, "设置")

    def test_settings_labels_and_palette_descriptions(self):
        examples = {
            "自动保存": "Auto-save",
            "深色石墨与淡紫色强调": "Dark graphite with soft lavender accents",
            "暖白纸张与低饱和绿色": "Warm white paper with muted green",
            "📧 邮箱: ": "📧 Email: ",
            "今天到期": "Due today",
        }
        for chinese, english in examples.items():
            with self.subTest(label=chinese):
                self.assertEqual(tr(chinese, "en"), english)

    def test_dynamic_dialogs_keep_user_data(self):
        self.assertEqual(
            tr("确定删除「学习 Python」吗？", "en"),
            "Delete “学习 Python”?",
        )
        self.assertEqual(
            tr("导入 3 条任务将替换当前全部 12 条任务。确定吗？", "en"),
            "Import 3 tasks and replace all 12 existing tasks?",
        )
        self.assertEqual(tr("已导入 3 条任务", "en"), "Imported 3 tasks")
        self.assertEqual(
            tr("已创建备份：personal-settings.json", "en"),
            "Backup created：personal-settings.json",
        )
        self.assertEqual(tr("版权所有 © 2026 SDCOM", "en"),
                         "Copyright © 2026 SDCOM")
        self.assertEqual(tr("版本 0.3.2", "en"), "Version 0.3.2")

    def test_dynamic_statistics_and_statuses(self):
        self.assertEqual(tr("总任务: 2", "en"), "Total tasks: 2")
        self.assertEqual(tr("完成率: 50.0%", "en"), "Completion: 50.0%")
        self.assertEqual(tr("已过期 4 天", "en"), "Overdue by 4 days")
        self.assertEqual(tr("截止: 2026/11/11", "en"), "Due: 2026/11/11")
        self.assertEqual(tr("任务已标记为完成", "en"), "Task marked completed")

    def test_dynamic_stats_are_localized(self):
        stats = "总计 3 项  ·  已完成 1  ·  进行中 2  ·  逾期 0"
        self.assertIn("Completed 1", tr(stats, "en"))
        self.assertIn("總計 3 項", tr(stats, "zh-tw"))


if __name__ == "__main__":
    unittest.main()
