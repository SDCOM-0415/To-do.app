"""Flet 桌面版的统一界面风格配置。

主题元数据、下拉选择、显示说明和持久化共用同一份字典。
新增主题时应补全全部配色令牌，并验证深浅色模式。
"""
from __future__ import annotations

import flet as ft

PALETTES = {
    "graphite": {
        "label": "Graphite Focus",
        "description": "深色石墨与淡紫色强调",
        "mode": ft.ThemeMode.DARK,
        "accent": "#A99CF4",
        "canvas": "#141519",
        "sidebar": "#1C1D23",
        "surface": "#22232B",
        "selected": "#353047",
        "divider": "#33353F",
    },
    "paper": {
        "label": "Paper & Ink",
        "description": "暖白纸张与低饱和绿色",
        "mode": ft.ThemeMode.LIGHT,
        "accent": "#57735F",
        "canvas": "#F5F1E9",
        "sidebar": "#EBE5DA",
        "surface": "#FFFCF7",
        "selected": "#D8E5D8",
        "divider": "#DCD4C9",
    },
    "blue": {
        "label": "Blue Hour",
        "description": "深海蓝与冷青色强调",
        "mode": ft.ThemeMode.DARK,
        "accent": "#78C7DD",
        "canvas": "#101A27",
        "sidebar": "#152436",
        "surface": "#1D3043",
        "selected": "#24435A",
        "divider": "#304A5E",
    },
    "nord": {
        "label": "Nord Frost",
        "description": "冰川浅灰蓝与沉稳的北欧蓝",
        "mode": ft.ThemeMode.LIGHT,
        "accent": "#456A91",
        "canvas": "#EDF3F7",
        "sidebar": "#DFE9F0",
        "surface": "#FFFFFF",
        "selected": "#C8DCEB",
        "divider": "#C7D6E0",
    },
    "forest": {
        "label": "Forest Studio",
        "description": "墨绿工作台与柔和苔绿色",
        "mode": ft.ThemeMode.DARK,
        "accent": "#A4C795",
        "canvas": "#121B17",
        "sidebar": "#1B2922",
        "surface": "#24352C",
        "selected": "#334E3D",
        "divider": "#37493D",
    },
    "rose": {
        "label": "Rose Quartz",
        "description": "淡粉米白与柔和玫瑰色",
        "mode": ft.ThemeMode.LIGHT,
        "accent": "#AC647D",
        "canvas": "#FCF5F4",
        "sidebar": "#F4E8E9",
        "surface": "#FFFBFA",
        "selected": "#EFD4DD",
        "divider": "#E7D5D8",
    },
    "solar": {
        "label": "Solar Sand",
        "description": "浅沙色纸面与温暖赭橙",
        "mode": ft.ThemeMode.LIGHT,
        "accent": "#98622E",
        "canvas": "#F8F2E4",
        "sidebar": "#EEE3CF",
        "surface": "#FFFCF5",
        "selected": "#F0D9B8",
        "divider": "#DFD1BB",
    },
    "midnight": {
        "label": "Midnight OLED",
        "description": "近黑色界面与清透薄荷青",
        "mode": ft.ThemeMode.DARK,
        "accent": "#83DDC4",
        "canvas": "#090C0D",
        "sidebar": "#101617",
        "surface": "#192122",
        "selected": "#203A36",
        "divider": "#293739",
    },
}

# Existing theme values from Tk or early Flet builds must remain readable.
ALIASES = {
    "dark": "graphite",
    "light": "paper",
    "system": "graphite",
    "graphite": "graphite",
    "paper": "paper",
    "blue": "blue",
    "nord": "nord",
    "forest": "forest",
    "rose": "rose",
    "solar": "solar",
    "midnight": "midnight",
}


def normalize_theme(value: str | None) -> str:
    return ALIASES.get(value or "", "graphite")


def appearance(value: str | None) -> dict:
    return PALETTES[normalize_theme(value)]
