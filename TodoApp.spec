# -*- mode: python ; coding: utf-8 -*-
"""
Todo App v0.3.1 - PyInstaller 规范文件
用于构建单个可执行文件
"""

import sys
import os
from pathlib import Path

block_cipher = None

# 获取当前目录
current_dir = os.path.abspath(os.path.dirname(__file__))

# 添加额外的数据文件
added_files = []

# 尝试找到 tcl/tk 库路径
import tkinter
tcl_tk_dir = os.path.dirname(os.path.dirname(tkinter.__file__))
tcl_dir = os.path.join(tcl_tk_dir, 'tcl')
tk_dir = os.path.join(tcl_tk_dir, 'tk')

# 添加 tcl/tk 库文件
tcl_tk_files = []
if os.path.exists(tcl_dir) and os.path.exists(tk_dir):
    tcl_tk_files.append((os.path.join(tcl_dir, '*'), 'tcl'))
    tcl_tk_files.append((os.path.join(tk_dir, '*'), 'tk'))

a = Analysis(
    ['app.py'],
    pathex=[current_dir],
    binaries=[],
    datas=tcl_tk_files + added_files,
    hiddenimports=[
        'customtkinter',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.colorchooser',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TodoApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)