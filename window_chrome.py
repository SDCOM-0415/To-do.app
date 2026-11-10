"""macOS 原生标题栏与 Flet 工作空间的对齐布局。

保留由 AppKit 管理的红黄绿窗口按钮，仅隐藏系统标题栏；
窗口顶部采用与下方侧栏同宽、同分割线的两栏拖动区域。
"""
from __future__ import annotations

import sys
import flet as ft
from appearance import appearance

SIDEBAR_WIDTH = 208
TITLEBAR_HEIGHT = 44


def has_integrated_titlebar() -> bool:
    return sys.platform == "darwin"


def configure_window(page: ft.Page) -> None:
    if has_integrated_titlebar():
        page.window.title_bar_hidden = True
        page.window.title_bar_buttons_hidden = False
        page.window.frameless = False


def update_titlebar_theme(surface: ft.Container, theme: str | None) -> None:
    """同时更新标题栏两侧的背景和竖分割线。"""
    colors = appearance(theme)
    surface.bgcolor = colors["sidebar"]
    left, right = surface.content.controls
    left.bgcolor = colors["sidebar"]
    left.border = ft.Border(right=ft.BorderSide(1, colors["divider"]))
    right.bgcolor = colors["canvas"]


def titlebar(theme: str | None) -> tuple[ft.Control | None, ft.Container | None]:
    if not has_integrated_titlebar():
        return None, None

    # 红绿灯由 macOS 原生绘制，左侧 208 逻辑像素范围内不放控件。
    # 与下方侧栏使用完全相同的宽度，竖分割线自然贯穿整窗。
    surface = ft.Container(
        height=TITLEBAR_HEIGHT,
        content=ft.Row(
            spacing=0,
            controls=[
                ft.Container(width=SIDEBAR_WIDTH, height=TITLEBAR_HEIGHT),
                ft.Container(expand=True, height=TITLEBAR_HEIGHT),
            ],
        ),
    )
    update_titlebar_theme(surface, theme)
    return ft.WindowDragArea(content=surface, maximizable=True), surface


def with_titlebar(content: ft.Control, theme: str | None) -> tuple[ft.Control, ft.Container | None]:
    bar, surface = titlebar(theme)
    if bar is None:
        return content, None
    return ft.Column(controls=[bar, content], expand=True, spacing=0), surface
