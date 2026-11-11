"""Regression tests for date entry and persisted deadline compatibility."""
import unittest
from datetime import date
from date_input import format_date_input, parse_date_input


class DateInputTests(unittest.TestCase):
    def test_slashes_insert_while_typing(self):
        cases = {
            "": "", "2": "2", "2026": "2026",
            "20261": "2026/1", "202611": "2026/11",
            "2026111": "2026/11/1", "20261111": "2026/11/11",
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(format_date_input(raw), expected)

    def test_paste_and_existing_iso_dates(self):
        self.assertEqual(format_date_input("2026-11-11"), "2026/11/11")
        self.assertEqual(format_date_input("2026/11/11"), "2026/11/11")
        self.assertEqual(parse_date_input("2026/11/11"), date(2026, 11, 11))
        self.assertEqual(parse_date_input("2026-11-11"), date(2026, 11, 11))
        self.assertEqual(parse_date_input("20261111"), date(2026, 11, 11))
        self.assertEqual(parse_date_input(""), None)

    def test_calendar_and_manual_store_the_same_iso_value(self):
        manual = parse_date_input("2026/11/11").isoformat()
        calendar = date(2026, 11, 11).isoformat()
        self.assertEqual(manual, calendar)
        self.assertEqual(manual, "2026-11-11")

    def test_invalid_dates_rejected(self):
        for value in ("2026/02/30", "2026/13/01", "2026/11/1",
                      "2026/1/11", "2026/11", "abc", "2026-11/11"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_date_input(value)

    def test_leap_day(self):
        self.assertEqual(parse_date_input("2028/02/29"), date(2028, 2, 29))
        with self.assertRaises(ValueError):
            parse_date_input("2027/02/29")


if __name__ == "__main__":
    unittest.main()
