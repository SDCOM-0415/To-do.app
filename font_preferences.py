"""Flet 字体偏好，使用应用内字体或各平台本地中文字体。"""
from __future__ import annotations

import sys
from pathlib import Path

FONT_MODES = ("harmony", "system")
HARMONY_FAMILY = "HarmonyOS Sans SC"
FONT_ASSET = "fonts/HarmonyOS_Sans_SC_Regular.ttf"

def normalize_font_mode(value: str | None) -> str:
    return value if value in FONT_MODES else "harmony"

def system_font_family(platform: str | None = None) -> str:
    platform = platform or sys.platform
    if platform == "win32":
        return "Microsoft YaHei UI"
    if platform == "darwin":
        return "PingFang SC"
    return "Noto Sans CJK SC"

def bundled_font_exists() -> bool:
    return (Path(__file__).resolve().parent / "assets" / FONT_ASSET).is_file()

def font_family(value: str | None) -> str:
    if normalize_font_mode(value) == "harmony":
        return HARMONY_FAMILY
    return system_font_family()

def register_flet_fonts(page) -> None:
    # Flutter 的内置 assets 在 .app/.exe 中不一定映射为 Python 文件路径。
    # 因此始终注册逻辑资源路径，不依赖打包后的 Path.exists()。
    page.fonts = {**(page.fonts or {}), HARMONY_FAMILY: "/" + FONT_ASSET}
