"""Settings migration and validation smoke tests."""
import copy
import unittest

import settings_ui
import storage
from appearance import PALETTES, normalize_theme


class SettingsValidationTests(unittest.TestCase):
    def test_tk_config_round_trip(self):
        source = {
            "theme": "dark",
            "window_size": "1200x800",
            "font_size": 16,
            "auto_save": True,
            "show_completed": False,
            "show_statistics": True,
            "confirm_delete": True,
            "language": "zh-cn",
            "priority_colors": {"高": "#ff4444", "中": "#ffaa00", "低": "#44ff44"},
        }
        validated = settings_ui.validate_settings(source)
        for key, value in source.items():
            if key == "theme":
                self.assertEqual(validated[key], "graphite")
            else:
                self.assertEqual(validated[key], value)
        self.assertIn("sort", validated)

    def test_all_appearance_presets_are_preserved(self):
        self.assertEqual(len(PALETTES), 10)
        for name in PALETTES:
            with self.subTest(name=name):
                validated = settings_ui.validate_settings({"theme": name})
                self.assertEqual(validated["theme"], name)
                self.assertIn(name, PALETTES)

    def test_all_palettes_have_required_tokens(self):
        required = {"label", "description", "mode", "accent", "canvas", "sidebar",
                    "surface", "selected", "divider"}
        for name, preset in PALETTES.items():
            with self.subTest(name=name):
                self.assertTrue(required.issubset(preset))
                self.assertEqual(normalize_theme(name), name)
                for token in ("accent", "canvas", "sidebar", "surface", "selected", "divider"):
                    self.assertRegex(preset[token], r"^#[0-9A-Fa-f]{6}$")

    def test_legacy_appearance_aliases(self):
        self.assertEqual(normalize_theme("light"), "paper")
        self.assertEqual(normalize_theme("dark"), "graphite")
        self.assertEqual(normalize_theme("system"), "graphite")

    def test_invalid_colors_rejected(self):
        value = copy.deepcopy(storage.DEFAULT_SETTINGS)
        value["priority_colors"]["高"] = "red"
        with self.assertRaises(ValueError):
            settings_ui.validate_settings(value)

    def test_out_of_range_dimensions_rejected(self):
        value = copy.deepcopy(storage.DEFAULT_SETTINGS)
        value["window_size"] = "640x480"
        with self.assertRaises(ValueError):
            settings_ui.validate_settings(value)

    def test_invalid_boolean_rejected(self):
        value = copy.deepcopy(storage.DEFAULT_SETTINGS)
        value["auto_save"] = "true"
        with self.assertRaises(ValueError):
            settings_ui.validate_settings(value)

    def test_import_does_not_mutate_default_colors(self):
        value = copy.deepcopy(storage.DEFAULT_SETTINGS)
        value["priority_colors"]["高"] = "#123abc"
        normalized = settings_ui.validate_settings(value)
        normalized["priority_colors"]["高"] = "#000000"
        self.assertEqual(storage.DEFAULT_SETTINGS["priority_colors"]["高"], "#ff4444")


if __name__ == "__main__":
    unittest.main()
