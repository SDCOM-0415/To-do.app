"""Tk task editor's slash-separated date input, compatible with ISO storage."""
from __future__ import annotations

import re
from datetime import date


def format_date_input(value: str) -> str:
    digits = re.sub(r"\D", "", (value or "").strip())[:8]
    if len(digits) <= 4:
        return digits
    if len(digits) <= 6:
        return digits[:4] + "/" + digits[4:]
    return digits[:4] + "/" + digits[4:6] + "/" + digits[6:]


def parse_date_input(value: str) -> date | None:
    value = (value or "").strip()
    if not value:
        return None
    if re.fullmatch(r"\d{8}", value):
        value = f"{value[:4]}-{value[4:6]}-{value[6:]}"
    elif re.fullmatch(r"\d{4}/\d{2}/\d{2}|\d{4}-\d{2}-\d{2}", value):
        value = value.replace("/", "-")
    else:
        raise ValueError("日期格式必须为 YYYY/MM/DD")
    return date.fromisoformat(value)
