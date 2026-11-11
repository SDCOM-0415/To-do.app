"""Tk 字体偏好和资源校验测试（不需要实际图形窗口）。"""
import hashlib
import unittest

from config import app_config
from font_preferences import (
    FONT_FILENAME, normalize_font_mode, system_font_family, font_path
)
from settings_manager import settings_manager


class FontPreferenceTests(unittest.TestCase):
    def test_default_and_choices(self):
        self.assertEqual(app_config.default_config["font_mode"], "harmony")
        for mode in ("harmony", "system"):
            ok, error = settings_manager.validate_setting("font_mode", mode)
            self.assertTrue(ok, error)
            self.assertEqual(normalize_font_mode(mode), mode)
        self.assertEqual(normalize_font_mode(None), "harmony")
        self.assertFalse(settings_manager.validate_setting("font_mode", "unknown")[0])

    def test_system_font_platforms(self):
        self.assertEqual(system_font_family("win32"), "Microsoft YaHei UI")
        self.assertEqual(system_font_family("darwin"), "PingFang SC")
        self.assertEqual(system_font_family("linux"), "Noto Sans CJK SC")

    def test_bundled_font_if_present_is_unmodified(self):
        p = font_path()
        if p is not None:
            self.assertEqual(p.name, FONT_FILENAME)
            self.assertEqual(
                hashlib.sha256(p.read_bytes()).hexdigest(),
                "297b088424be212207df2ce8b98e335468b782aa6b96832af0b8b773d711e2b1",
            )


if __name__ == "__main__":
    unittest.main()
