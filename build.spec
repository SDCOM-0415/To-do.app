# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import glob
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

# Tkinter 模块和库文件处理
try:
    import tkinter
    import _tkinter
    
    # 获取 Python 安装路径
    python_path = Path(sys.executable).parent
    
    # 1. 添加 tkinter 模块的所有 Python 源文件
    tkinter_module_path = Path(tkinter.__file__).parent
    print(f"Tkinter module path: {tkinter_module_path}")
    
    # 收集 tkinter 目录下的所有 .py 文件
    for py_file in tkinter_module_path.glob('*.py'):
        datas.append((str(py_file), 'tkinter'))
        print(f"Added tkinter file: {py_file.name}")
    
    # 收集 tkinter 子目录
    for subdir in tkinter_module_path.iterdir():
        if subdir.is_dir() and not subdir.name.startswith('__pycache__'):
            for py_file in subdir.rglob('*.py'):
                rel_path = py_file.relative_to(tkinter_module_path)
                datas.append((str(py_file), f'tkinter/{rel_path.parent}'))
                print(f"Added tkinter submodule file: {rel_path}")
    
    # 2. 查找并添加 TCL/TK 库文件
    possible_locations = [
        python_path / 'tcl',
        python_path / 'tk',
        python_path.parent / 'tcl',
        python_path.parent / 'tk',
        Path(tkinter.__file__).parent.parent / 'tcl',
        Path(tkinter.__file__).parent.parent / 'tk'
    ]
    
    # 添加 TCL 库
    for location in possible_locations:
        if location.exists() and location.name == 'tcl':
            tcl86_path = location / 'tcl8.6'
            if tcl86_path.exists():
                datas.append((str(tcl86_path), '_tcl_data/tcl8.6'))
                print(f"Added TCL library: {tcl86_path}")
            else:
                datas.append((str(location), '_tcl_data'))
                print(f"Added TCL library: {location}")
    
    # 添加 TK 库
    for location in possible_locations:
        if location.exists() and location.name == 'tk':
            tk86_path = location / 'tk8.6'
            if tk86_path.exists():
                datas.append((str(tk86_path), '_tk_data/tk8.6'))
                print(f"Added TK library: {tk86_path}")
            else:
                datas.append((str(location), '_tk_data'))
                print(f"Added TK library: {location}")
    
    # 3. 添加 DLLs 目录中的 TCL/TK 相关文件
    dlls_path = python_path / 'DLLs'
    if dlls_path.exists():
        for dll_file in dlls_path.glob('t*.dll'):
            datas.append((str(dll_file), '.'))
            print(f"Added DLL: {dll_file}")
            
except ImportError as e:
    print(f"Warning: Tkinter import failed: {e}")

# 隐藏导入 - 使用 collect-submodules 方式
hiddenimports = [
    'customtkinter',
    'PIL',
    'PIL._tkinter_finder',
    '_tkinter',
    'darkdetect',
    'packaging',
    'packaging.version',
    'packaging.specifiers',
    'packaging.requirements',
]

# 添加所有 tkinter 子模块
tkinter_submodules = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'tkinter.colorchooser',
    'tkinter.constants',
    'tkinter.commondialog',
    'tkinter.dialog',
    'tkinter.dnd',
    'tkinter.font',
    'tkinter.simpledialog',
    'tkinter.tix',
    'tkinter.scrolledtext',
    'tkinter.ttkthemes',
]

hiddenimports.extend(tkinter_submodules)

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
    runtime_hooks=['pyi_rth_tkinter_fix.py', 'pyi_rth_tkinter_override.py', 'hook-runtime.py'],
    additional_hooks_dir=['.'],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    # 强制包含 tkinter 模块
    collect_submodules=['tkinter'],
)


pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TodoApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    icon='res/icon.ico' if os.path.exists('res/icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TodoApp',
)
