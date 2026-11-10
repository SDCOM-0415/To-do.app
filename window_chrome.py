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


def update_titlebar_theme(
    surface: ft.Container, theme: str | None, *, settings_view: bool = False
) -> None:
    """首页按侧栏分区；没有侧栏的设置页使用完整统一的背景。"""
    colors = appearance(theme)
    surface.bgcolor = colors["canvas" if settings_view else "sidebar"]
    if settings_view:
        surface.content = None
    else:
        surface.content = ft.Row(
            spacing=0,
            controls=[
                ft.Container(
                    width=SIDEBAR_WIDTH,
                    height=TITLEBAR_HEIGHT,
                    bgcolor=colors["sidebar"],
                    border=ft.Border(right=ft.BorderSide(1, colors["divider"])),
                ),
                ft.Container(
                    expand=True, height=TITLEBAR_HEIGHT, bgcolor=colors["canvas"]
                ),
            ],
        )


def titlebar(theme: str | None, *, settings_view: bool = False) -> tuple[ft.Control | None, ft.Container | None]:
    if not has_integrated_titlebar():
        return None, None

    # 红绿灯由 macOS 原生绘制，左侧 208 逻辑像素范围内不放控件。
    # 与下方侧栏使用完全相同的宽度，竖分割线自然贯穿整窗。
    surface = ft.Container(height=TITLEBAR_HEIGHT)
    update_titlebar_theme(surface, theme, settings_view=settings_view)
    return ft.WindowDragArea(content=surface, maximizable=True), surface


def with_titlebar(
    content: ft.Control, theme: str | None, *, settings_view: bool = False
) -> tuple[ft.Control, ft.Container | None]:
    bar, surface = titlebar(theme, settings_view=settings_view)
    if bar is None:
        return content, None
    return ft.Column(controls=[bar, content], expand=True, spacing=0), surface
