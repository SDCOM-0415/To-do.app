"""Design tokens for the three Flet desktop appearances.

Graphite Focus: graphite canvas + muted violet accent.
Paper & Ink: warm ivory canvas + earthy green accent.
Blue Hour: deep blue canvas + cool cyan accent.
"""
from __future__ import annotations

import flet as ft

PALETTES = {
    "graphite": {
        "label": "Graphite Focus",
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
        "mode": ft.ThemeMode.DARK,
        "accent": "#78C7DD",
        "canvas": "#101A27",
        "sidebar": "#152436",
        "surface": "#1D3043",
        "selected": "#24435A",
        "divider": "#304A5E",
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
}


def normalize_theme(value: str | None) -> str:
    return ALIASES.get(value or "", "graphite")


def appearance(value: str | None) -> dict:
    return PALETTES[normalize_theme(value)]
