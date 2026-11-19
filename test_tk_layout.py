"""Tk 双布局配置回归测试：无须创建真实窗口。"""
import unittest

from config import app_config
from modern_ui import LAYOUTS, VIEWS, normalize_layout
from settings_manager import settings_manager


class TkLayoutTests(unittest.TestCase):
    def test_default_layout_is_classic(self):
        self.assertEqual(app_config.default_config["ui_layout"], "classic")
        self.assertEqual(normalize_layout(None), "classic")
        self.assertEqual(normalize_layout("outdated"), "classic")

    def test_both_layouts_are_supported(self):
        self.assertEqual(LAYOUTS, ("classic", "modern"))
        for name in LAYOUTS:
            with self.subTest(name=name):
                self.assertEqual(normalize_layout(name), name)
                valid, errors = settings_manager.validate_setting("ui_layout", name)
                self.assertTrue(valid, errors)

    def test_invalid_layout_is_rejected(self):
        valid, error = settings_manager.validate_setting("ui_layout", "unknown")
        self.assertFalse(valid)
        self.assertTrue(error)

    def test_navigation_has_distinct_filters(self):
        self.assertEqual(VIEWS, ("全部任务", "进行中", "已完成"))

    def test_theme_tokens_have_light_and_dark_hex_pairs(self):
        from modern_ui import THEME_TOKENS, palette
        required = {
            "canvas", "sidebar", "surface", "card", "input", "text",
            "secondary", "muted", "accent", "accent_hover", "on_accent",
            "selected", "line", "danger_soft", "danger_text", "overdue",
        }
        self.assertTrue(required.issubset(THEME_TOKENS))
        for key, pair in THEME_TOKENS.items():
            with self.subTest(token=key):
                self.assertEqual(len(pair), 2)
                for color in pair:
                    self.assertRegex(color, r"^#[0-9A-Fa-f]{6}$")
        active = palette()
        self.assertTrue(required.issubset(active))


if __name__ == "__main__":
    unittest.main()
