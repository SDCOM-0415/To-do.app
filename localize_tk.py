"""Translate existing CustomTkinter controls after language settings change."""
from __future__ import annotations

from tkinter import TclError

from i18n import tr, normalize_language


def localize_tk(root, language: str) -> None:
    """Apply translated UI labels to CTk widgets without editing task input."""
    language = normalize_language(language)

    def visit(widget):
        cls = type(widget).__name__
        if widget is root and hasattr(widget, "title"):
            try:
                old_title = widget.title()
                new_title = tr(old_title, language)
                if new_title != old_title:
                    widget.title(new_title)
            except (RuntimeError, TypeError, ValueError):
                pass
        # CTkTabview: tab names are backed by a separate segmented button.
        if cls == "CTkTabview":
            previous = getattr(widget, "_i18n_tab_language", "zh-cn")
            if previous != language:
                for canonical in ("外观", "行为", "颜色", "高级", "关于"):
                    old_name = tr(canonical, previous)
                    new_name = tr(canonical, language)
                    if old_name != new_name:
                        try:
                            widget.rename(old_name, new_name)
                        except (ValueError, KeyError, AttributeError):
                            pass
                widget._i18n_tab_language = language
        if cls in ("CTkLabel", "CTkButton", "CTkCheckBox", "CTkRadioButton", "CTkSwitch", "CTkSegmentedButton"):
            try:
                value = widget.cget("text")
            except (TclError, ValueError, AttributeError, KeyError):
                value = None
            # Some CustomTkinter widgets, notably radio buttons on macOS,
            # expose their caption through _text instead of cget("text").
            if value is None:
                value = getattr(widget, "_text", None)
            if isinstance(value, str):
                updated = tr(value, language)
                if updated != value:
                    try:
                        widget.configure(text=updated)
                    except (TclError, ValueError, AttributeError):
                        pass
        if cls == "CTkEntry":
            try:
                value = widget.cget("placeholder_text")
                sources = getattr(widget, "_i18n_sources", None)
                if sources is None:
                    sources = {}
                    widget._i18n_sources = sources
                original = sources.setdefault("placeholder_text", value)
                updated = tr(original, language)
                if updated != value:
                    widget.configure(placeholder_text=updated)
            except (TclError, ValueError, AttributeError, KeyError):
                pass
        if cls == "CTkOptionMenu":
            # Language names are stable identifiers; all other menus can be
            # localized without changing the corresponding saved values.
            try:
                values = list(widget.cget("values"))
                if values and not any("(zh-cn)" in v or "(zh-tw)" in v for v in values):
                    old = getattr(widget, "_i18n_menu_sources", None)
                    if old is None:
                        old = tuple(values)
                        widget._i18n_menu_sources = old
                    translated = [tr(value, language) for value in old]
                    selected = widget.get()
                    index = values.index(selected) if selected in values else -1
                    if translated != values:
                        widget.configure(values=translated)
                        if index >= 0:
                            widget.set(translated[index])
            except (TclError, ValueError, AttributeError, RuntimeError):
                pass
        try:
            children = widget.winfo_children()
        except (TclError, AttributeError, RuntimeError):
            return
        for child in children:
            visit(child)

    visit(root)
