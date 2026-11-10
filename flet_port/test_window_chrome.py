"""Smoke tests for platform-dependent window chrome."""
from __future__ import annotations

import unittest
from unittest.mock import patch
from types import SimpleNamespace

import flet as ft
import window_chrome


class WindowChromeTests(unittest.TestCase):
    def test_mac_titlebar_preserves_native_buttons(self):
        with patch.object(window_chrome.sys, "platform", "darwin"):
            page = SimpleNamespace(window=SimpleNamespace())
            window_chrome.configure_window(page)
            self.assertTrue(page.window.title_bar_hidden)
            self.assertFalse(page.window.title_bar_buttons_hidden)
            self.assertFalse(page.window.frameless)
            content, surface = window_chrome.with_titlebar(ft.Text("Tasks"), "graphite")
            self.assertIsInstance(content, ft.Column)
            self.assertIsNotNone(surface)
            self.assertEqual(surface.height, 44)

    def test_non_mac_keeps_native_titlebar(self):
        with patch.object(window_chrome.sys, "platform", "win32"):
            content, surface = window_chrome.with_titlebar(ft.Text("Tasks"), "paper")
            self.assertIsNone(surface)
            self.assertIsInstance(content, ft.Text)

    def test_titlebar_matches_appearance(self):
        with patch.object(window_chrome.sys, "platform", "darwin"):
            _, surface = window_chrome.with_titlebar(ft.Text("Tasks"), "blue")
            self.assertEqual(surface.bgcolor, "#152436")


if __name__ == "__main__":
    unittest.main()
