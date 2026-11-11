"""Tk 字体模式与进程内字体注册。

内置 HarmonyOS Sans SC 未修改文件随程序分发；缺失时自动回退系统字体。
"""
from __future__ import annotations

import ctypes
import os
import sys
from pathlib import Path

FONT_MODES = ("harmony", "system")
FONT_FILENAME = "HarmonyOS_Sans_SC_Regular.ttf"
FONT_FAMILY = "HarmonyOS Sans SC"
_registered = False

def normalize_font_mode(value):
    return value if value in FONT_MODES else "harmony"

def system_font_family(platform=None):
    p = platform or sys.platform
    if p == "win32":
        return "Microsoft YaHei UI"
    if p == "darwin":
        return "PingFang SC"
    return "Noto Sans CJK SC"

def font_path():
    roots = [Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)),
             Path(__file__).resolve().parent]
    for root in roots:
        path = root / "res" / "fonts" / FONT_FILENAME
        if path.is_file():
            return path
    return None

def register_bundled_font():
    global _registered
    if _registered:
        return True
    path = font_path()
    if path is None:
        return False
    try:
        if sys.platform == "win32":
            # FR_PRIVATE: 字体只在 TodoApp 进程可见，不修改系统字体安装。
            result = ctypes.windll.gdi32.AddFontResourceExW(str(path), 0x10, None)
            _registered = bool(result)
        elif sys.platform == "darwin":
            coretext = ctypes.CDLL("/System/Library/Frameworks/CoreText.framework/CoreText")
            corefoundation = ctypes.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
            corefoundation.CFURLCreateFromFileSystemRepresentation.argtypes = [
                ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long, ctypes.c_bool]
            corefoundation.CFURLCreateFromFileSystemRepresentation.restype = ctypes.c_void_p
            raw = os.fsencode(path)
            url = corefoundation.CFURLCreateFromFileSystemRepresentation(None, raw, len(raw), False)
            if url:
                try:
                    coretext.CTFontManagerRegisterFontsForURL.argtypes = [
                        ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
                    coretext.CTFontManagerRegisterFontsForURL.restype = ctypes.c_bool
                    _registered = bool(coretext.CTFontManagerRegisterFontsForURL(url, 1, None))
                finally:
                    corefoundation.CFRelease.argtypes = [ctypes.c_void_p]
                    corefoundation.CFRelease(url)
        else:
            from ctypes.util import find_library
            library = find_library("fontconfig")
            if library:
                fc = ctypes.CDLL(library)
                fc.FcConfigGetCurrent.restype = ctypes.c_void_p
                fc.FcConfigAppFontAddFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
                fc.FcConfigAppFontAddFile.restype = ctypes.c_int
                _registered = bool(fc.FcConfigAppFontAddFile(
                    fc.FcConfigGetCurrent(), os.fsencode(path)))
    except (OSError, AttributeError, ValueError) as exc:
        print(f"无法注册内置字体，将使用系统字体：{exc}")
    return _registered

def current_font_family(mode="harmony"):
    if normalize_font_mode(mode) == "harmony" and register_bundled_font():
        return FONT_FAMILY
    return system_font_family()

def apply_tk_font(root, mode="harmony"):
    """设置 CustomTkinter 默认字体和 Tk 原生控件字体，不安装系统字体。"""
    import customtkinter as ctk
    family = current_font_family(mode)
    # CTkFont 默认构造器由主题映射决定，无需逐个指定所有控件。
    ctk.ThemeManager.theme["CTkFont"]["family"] = family
    root.option_add("*Font", (family, 12))
    return family
