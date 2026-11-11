"""Tk 日期输入解析与 ISO 保存格式回归测试。"""
import unittest
from datetime import date
from date_input import format_date_input, parse_date_input


class DateInputTests(unittest.TestCase):
    def test_auto_separator(self):
        self.assertEqual(format_date_input("20261111"), "2026/11/11")
        self.assertEqual(format_date_input("202611"), "2026/11")
        self.assertEqual(format_date_input("2026-11-11"), "2026/11/11")
        self.assertEqual(format_date_input("2026/11/11T23:59:59"), "2026/11/11")

    def test_iso_storage_compatibility(self):
        self.assertEqual(parse_date_input("2026/11/11").isoformat(), "2026-11-11")
        self.assertEqual(parse_date_input(""), None)
        self.assertEqual(parse_date_input("20261111"), date(2026, 11, 11))

    def test_invalid_dates(self):
        for value in ("2026/02/30", "2026/11", "2026/13/01"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_date_input(value)

    def test_leap_date(self):
        self.assertEqual(parse_date_input("2028/02/29"), date(2028, 2, 29))


if __name__ == "__main__":
    unittest.main()
