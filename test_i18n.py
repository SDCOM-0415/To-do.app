"""Regression coverage for UI translations and user-data isolation."""
import unittest
from tkinter import TclError

from localize_tk import localize_tk
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

    def test_tk_radio_caption_fallback(self):
        from localize_tk import localize_tk
        from tkinter import TclError

        class CTkRadioButton:
            def __init__(self):
                self._text = "跟随系统"

            def cget(self, key):
                raise TclError('unknown option "-text"')

            def configure(self, **kwargs):
                self._text = kwargs["text"]

            def winfo_children(self):
                return []

        radio = CTkRadioButton()
        localize_tk(radio, "en")
        self.assertEqual(radio._text, "Follow system")
        localize_tk(radio, "zh-cn")
        self.assertEqual(radio._text, "跟随系统")

    def test_tk_localization_ignores_containers_without_text_option(self):
        """容器没有 -text 时，切换语言不能阻断设置保存回调。"""
        class CTkFrame:
            def __init__(self, children=()):
                self.children = list(children)
                self.text_queries = 0

            def cget(self, option):
                self.text_queries += 1
                raise TclError('unknown option "-text"')

            def winfo_children(self):
                return self.children

        class CTkLabel:
            def __init__(self, value):
                self.text = value

            def cget(self, option):
                if option == "text":
                    return self.text
                raise TclError(f'unknown option "-{option}"')

            def configure(self, **options):
                self.text = options["text"]

            def winfo_children(self):
                return []

        label = CTkLabel("新建任务")
        frame = CTkFrame([label])
        localize_tk(frame, "en")
        self.assertEqual(label.text, "New task")
        localize_tk(frame, "zh-cn")
        self.assertEqual(label.text, "新建任务")
        self.assertEqual(frame.text_queries, 0)

    def test_tk_localization_tolerates_unsupported_text_option(self):
        class CTkLabel:
            def cget(self, option):
                raise TclError('unknown option "-text"')

            def winfo_children(self):
                return []

        localize_tk(CTkLabel(), "en")


if __name__ == "__main__":
    unittest.main()
