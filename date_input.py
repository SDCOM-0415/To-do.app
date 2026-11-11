"""Date text input UX and ISO-compatible persistence for Flet task deadlines."""
from __future__ import annotations

import re
from datetime import date


def format_date_input(value: str) -> str:
    """Render numeric input as YYYY/MM/DD without changing stored ISO dates.

    Supports pasting YYYY-MM-DD and YYYY/MM/DD, and allows users to erase
    characters normally instead of forcing a trailing slash at boundaries.
    """
    value = (value or "").strip()
    digits = re.sub(r"\D", "", value)[:8]
    if len(digits) <= 4:
        return digits
    if len(digits) <= 6:
        return digits[:4] + "/" + digits[4:]
    return digits[:4] + "/" + digits[4:6] + "/" + digits[6:]


def parse_date_input(value: str) -> date | None:
    """Convert full YYYY/MM/DD, YYYY-MM-DD or YYYYMMDD to a date.

    Incomplete, malformed and nonexistent dates are rejected. Empty is allowed.
    """
    value = (value or "").strip()
    if not value:
        return None
    if re.fullmatch(r"\d{8}", value):
        value = f"{value[:4]}-{value[4:6]}-{value[6:]}"
    elif re.fullmatch(r"\d{4}/\d{2}/\d{2}|\d{4}-\d{2}-\d{2}", value):
        value = value.replace("/", "-")
    else:
        raise ValueError("日期格式应为 YYYY/MM/DD")
    return date.fromisoformat(value)
