"""Translate existing CustomTkinter controls after language settings change."""
from __future__ import annotations

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
        if cls not in ("CTkEntry", "CTkTextbox", "CTkOptionMenu", "CTkComboBox"):
            try:
                value = widget.cget("text")
            except (ValueError, AttributeError, KeyError):
                value = None
            if isinstance(value, str):
                updated = tr(value, language)
                if updated != value:
                    try:
                        widget.configure(text=updated)
                    except (ValueError, AttributeError):
                        pass
        if cls == "CTkEntry":
            try:
                value = widget.cget("placeholder_text")
                updated = tr(value, language)
                if updated != value:
                    widget.configure(placeholder_text=updated)
            except (ValueError, AttributeError, KeyError):
                pass
        try:
            children = widget.winfo_children()
        except (AttributeError, RuntimeError):
            return
        for child in children:
            visit(child)

    visit(root)
