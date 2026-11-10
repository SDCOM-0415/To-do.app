"""窗口标题栏的跨平台结构和主题一致性测试。"""
from __future__ import annotations

import unittest
from unittest.mock import patch
from types import SimpleNamespace

import flet as ft
import window_chrome
from appearance import PALETTES


class WindowChromeTests(unittest.TestCase):
    def test_macos_keeps_real_traffic_lights(self):
        with patch.object(window_chrome.sys, "platform", "darwin"):
            page = SimpleNamespace(window=SimpleNamespace())
            window_chrome.configure_window(page)
            self.assertTrue(page.window.title_bar_hidden)
            self.assertFalse(page.window.title_bar_buttons_hidden)
            self.assertFalse(page.window.frameless)

    def test_main_and_settings_use_same_unbroken_titlebar(self):
        with patch.object(window_chrome.sys, "platform", "darwin"):
            for theme, palette in PALETTES.items():
                with self.subTest(theme=theme):
                    _, main = window_chrome.with_titlebar(ft.Text("任务"), theme)
                    _, settings = window_chrome.with_titlebar(
                        ft.Text("设置"), theme, settings_view=True
                    )
                    for surface in (main, settings):
                        self.assertEqual(surface.height, window_chrome.TITLEBAR_HEIGHT)
                        self.assertEqual(surface.bgcolor, palette["sidebar"])
                        self.assertIsNone(surface.content)

    def test_theme_change_keeps_titlebar_unified(self):
        with patch.object(window_chrome.sys, "platform", "darwin"):
            _, surface = window_chrome.with_titlebar(ft.Text("设置"), "graphite", settings_view=True)
            window_chrome.update_titlebar_theme(surface, "paper", settings_view=True)
            self.assertEqual(surface.bgcolor, "#EBE5DA")
            self.assertIsNone(surface.content)
            window_chrome.update_titlebar_theme(surface, "blue")
            self.assertEqual(surface.bgcolor, "#152436")
            self.assertIsNone(surface.content)

    def test_other_systems_keep_native_titlebar(self):
        with patch.object(window_chrome.sys, "platform", "win32"):
            content = ft.Text("任务")
            layout, surface = window_chrome.with_titlebar(content, "paper")
            self.assertIs(layout, content)
            self.assertIsNone(surface)


if __name__ == "__main__":
    unittest.main()
