"""Apply translations to mounted Flet controls without changing task data."""
from __future__ import annotations

from i18n import tr, normalize_language


def localize_flet(root, language: str) -> None:
    """Translate UI controls in place, including tab labels and button tooltips.

    Input data values in TextField / Dropdown are never rewritten.
    """
    language = normalize_language(language)
    visited = set()

    def walk(control):
        if control is None or id(control) in visited:
            return
        visited.add(id(control))
        control_type = type(control).__name__
        for prop in ("text", "label", "tooltip", "hint_text", "help_text", "confirm_text",
                     "cancel_text", "field_label_text", "field_hint_text", "title"):
            value = getattr(control, prop, None)
            if isinstance(value, str):
                translated = tr(value, language)
                if translated != value:
                    setattr(control, prop, translated)
        # Flet Text displays value; TextField.value is actual user input.
        if control_type == "Text":
            value = getattr(control, "value", None)
            if isinstance(value, str):
                translated = tr(value, language)
                if translated != value:
                    control.value = translated
        for name in ("content", "title", "subtitle", "leading", "trailing",
                     "icon", "label", "description", "footer"):
            child = getattr(control, name, None)
            if not isinstance(child, (str, int, float, bool)):
                walk(child)
        for name in ("controls", "actions", "options", "tabs", "destinations"):
            children = getattr(control, name, None)
            if isinstance(children, (list, tuple)):
                for child in children:
                    walk(child)
    if isinstance(root, (list, tuple)):
        for element in root:
            walk(element)
    else:
        walk(root)
