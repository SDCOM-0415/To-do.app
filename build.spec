# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(SPEC))
sys.path.insert(0, current_dir)

block_cipher = None

# 数据文件收集
datas = []

# CustomTkinter 资源文件
try:
    import customtkinter
    ctk_path = Path(customtkinter.__file__).parent
    
    # 添加主题文件
    themes_path = ctk_path / 'assets' / 'themes'
    if themes_path.exists():
        datas.append((str(themes_path), 'customtkinter/assets/themes'))
    
    # 添加字体文件
    fonts_path = ctk_path / 'assets' / 'fonts'
    if fonts_path.exists():
        datas.append((str(fonts_path), 'customtkinter/assets/fonts'))
    
    # 添加图标文件
    icons_path = ctk_path / 'assets' / 'icons'
    if icons_path.exists():
        datas.append((str(icons_path), 'customtkinter/assets/icons'))
        
except ImportError:
    print("Warning: CustomTkinter not found")

# Tkinter 库文件
try:
    import tkinter
    import _tkinter
    
    # 获取 Python 安装路径
    python_path = Path(sys.executable).parent
    
    # TCL/TK 库文件
    tcl_path = python_path / 'tcl'
    tk_path = python_path / 'tk'
    
    if tcl_path.exists():
        datas.append((str(tcl_path), 'tcl'))
    if tk_path.exists():
        datas.append((str(tk_path), 'tk'))
        
    # DLLs 目录中的 TCL/TK 相关文件
    dlls_path = python_path / 'DLLs'
    if dlls_path.exists():
        for dll_file in dlls_path.glob('t*.dll'):
            datas.append((str(dll_file), '.'))
            
except ImportError:
    print("Warning: Tkinter not found")

# 隐藏导入
hiddenimports = [
    'customtkinter',
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'tkinter.colorchooser',
    'PIL',
    'PIL._tkinter_finder',
    '_tkinter',
    'tkinter.constants',
    'tkinter.commondialog',
    'tkinter.dialog',
    'tkinter.dnd',
    'tkinter.font',
    'tkinter.simpledialog',
    'tkinter.tix',
    'darkdetect',
    'packaging',
    'packaging.version',
    'packaging.specifiers',
    'packaging.requirements',
]

# 排除的模块
excludes = [
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'pytest',
    'setuptools',
]

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=['hook-runtime.py'],
    excludes=excludes,
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
    name='To-do',
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
