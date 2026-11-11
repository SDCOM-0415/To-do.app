"""Flet 字体模式、系统回退和资源映射测试。"""
import hashlib
import unittest
from types import SimpleNamespace

from font_preferences import (
    HARMONY_FAMILY, FONT_ASSET, font_family, normalize_font_mode,
    system_font_family, register_flet_fonts, bundled_font_exists,
)
from pathlib import Path


class FletFontTests(unittest.TestCase):
    def test_default_and_system_font(self):
        self.assertEqual(normalize_font_mode(None), "harmony")
        self.assertEqual(normalize_font_mode("bad"), "harmony")
        self.assertEqual(font_family("harmony"), HARMONY_FAMILY)
        self.assertEqual(font_family("system"), system_font_family())
        self.assertEqual(system_font_family("win32"), "Microsoft YaHei UI")
        self.assertEqual(system_font_family("darwin"), "PingFang SC")
        self.assertEqual(system_font_family("linux"), "Noto Sans CJK SC")

    def test_assets_are_registered(self):
        page = SimpleNamespace(fonts={"Existing": "/fonts/existing.ttf"})
        register_flet_fonts(page)
        self.assertEqual(page.fonts[HARMONY_FAMILY], "/" + FONT_ASSET)
        self.assertIn("Existing", page.fonts)

    def test_bundled_font_integrity_when_available(self):
        if bundled_font_exists():
            p = Path(__file__).parent / "assets" / FONT_ASSET
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),
                             "297b088424be212207df2ce8b98e335468b782aa6b96832af0b8b773d711e2b1")


if __name__ == "__main__":
    unittest.main()
