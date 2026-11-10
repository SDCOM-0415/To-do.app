"""macOS 原生红绿灯与 Flet 标题栏的统一背景。

AppKit 负责绘制真实的红黄绿窗口按钮。隐藏系统标题文字后，
统一整个顶部拖动带的底色，而不是在原生按钮旁拼接两种材质。
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
    """无论主页还是设置页，顶部整条使用与原生按钮区域相近的侧栏底色。

    Paper & Ink 下的原生按钮区由 macOS 绘制，截图实测为 #EAE5DB；
    主题侧栏色 #EBE5DA 与之接近。统一整条标题栏可消除横向拼接。
    """
    colors = appearance(theme)
    surface.bgcolor = colors["sidebar"]
    surface.content = None


def titlebar(
    theme: str | None, *, settings_view: bool = False
) -> tuple[ft.Control | None, ft.Container | None]:
    if not has_integrated_titlebar():
        return None, None
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
