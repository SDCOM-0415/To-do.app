"""macOS unified native window chrome for the Flet edition.

Keep the real AppKit traffic-light buttons; do not draw fake window controls.
Only macOS hides its native title bar. Windows/Linux retain native chrome.
"""
from __future__ import annotations

import sys
import flet as ft
from appearance import appearance


def has_integrated_titlebar() -> bool:
    return sys.platform == "darwin"


def configure_window(page: ft.Page) -> None:
    if has_integrated_titlebar():
        page.window.title_bar_hidden = True
        # macOS still owns the red/yellow/green controls and their behavior.
        page.window.title_bar_buttons_hidden = False
        page.window.frameless = False


def titlebar(theme: str | None) -> tuple[ft.Control | None, ft.Container | None]:
    if not has_integrated_titlebar():
        return None, None
    colors = appearance(theme)
    surface = ft.Container(
        height=44,
        bgcolor=colors["sidebar"],
        padding=ft.Padding.only(left=94, right=18),
        content=ft.Row(
            controls=[
                ft.Text("TodoApp Flet", size=12, weight=ft.FontWeight.W_600,
                        color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Container(expand=True),
                ft.Text("0.3.2", size=11, color=ft.Colors.ON_SURFACE_VARIANT),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    # Reserve the left 94 logical pixels for native macOS traffic lights.
    # The rest of the strip is a draggable part of the window.
    return ft.WindowDragArea(content=surface, maximizable=True), surface


def with_titlebar(content: ft.Control, theme: str | None) -> tuple[ft.Control, ft.Container | None]:
    bar, surface = titlebar(theme)
    if bar is None:
        return content, None
    return ft.Column(controls=[bar, content], expand=True, spacing=0), surface
