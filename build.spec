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
    
    # 2. 查找并添加 TCL/TK 库文件 - 更精确的方法
    
    # 查找 TCL 库
    tcl_locations = [
        python_path / 'tcl' / 'tcl8.6',
        python_path / 'lib' / 'tcl8.6',
        python_path.parent / 'tcl' / 'tcl8.6',
        python_path.parent / 'lib' / 'tcl8.6',
    ]
    
    for tcl_path in tcl_locations:
        if tcl_path.exists():
            init_tcl = tcl_path / 'init.tcl'
            if init_tcl.exists():
                datas.append((str(tcl_path), '_tcl_data/tcl8.6'))
                print(f"Added complete TCL library: {tcl_path}")
                break
    
    # 查找 TK 库 - 将tk.tcl直接放在_tk_data根目录
    tk_locations = [
        python_path / 'tcl' / 'tk8.6',  # 通常在 tcl 目录下
        python_path / 'tk' / 'tk8.6',
        python_path / 'lib' / 'tk8.6',
        python_path.parent / 'tcl' / 'tk8.6',
        python_path.parent / 'tk' / 'tk8.6',
        python_path.parent / 'lib' / 'tk8.6',
    ]
    
    tk_library_found = False
    for tk_path in tk_locations:
        if tk_path.exists():
            tk_tcl = tk_path / 'tk.tcl'
            if tk_tcl.exists():
                # 将整个TK库内容直接放在_tk_data目录，而不是_tk_data/tk8.6子目录
                datas.append((str(tk_path), '_tk_data'))
                print(f"Added complete TK library with tk.tcl: {tk_path} -> _tk_data")
                print(f"Verified tk.tcl exists: {tk_tcl}")
                tk_library_found = True
                break
    
    if not tk_library_found:
        # 如果没找到标准位置，尝试查找任何包含 tk.tcl 的目录
        print("Warning: 未找到标准 TK 库位置，尝试搜索 tk.tcl 文件...")
        for root_path in [python_path, python_path.parent]:
            for tk_tcl_file in root_path.rglob('tk.tcl'):
                tk_dir = tk_tcl_file.parent
                # 直接放在_tk_data根目录
                datas.append((str(tk_dir), '_tk_data'))
                print(f"Found tk.tcl and added TK library: {tk_dir} -> _tk_data")
                tk_library_found = True
                break
            if tk_library_found:
                break
    
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
    runtime_hooks=['pyi_rth_tkinter_fix.py', 'pyi_rth_tkinter_override.py', 'pyi_rth_tkinter_final.py', 'hook-runtime.py'],
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
