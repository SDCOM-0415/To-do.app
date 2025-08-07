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
    
    # 获取 tkinter 模块路径
    tkinter_path = Path(tkinter.__file__).parent.parent
    
    # 查找 TCL/TK 库文件的多个可能位置
    possible_locations = [
        tkinter_path / 'tcl',
        tkinter_path / 'tk', 
        Path(sys.executable).parent / 'tcl',
        Path(sys.executable).parent / 'tk',
        Path(sys.executable).parent.parent / 'tcl',
        Path(sys.executable).parent.parent / 'tk'
    ]
    
    # 添加找到的 TCL 库
    for location in possible_locations:
        if location.exists() and location.name == 'tcl':
            # 查找 tcl8.6 目录
            tcl86_path = location / 'tcl8.6'
            if tcl86_path.exists():
                datas.append((str(tcl86_path), '_tcl_data/tcl8.6'))
                print(f"Added TCL library: {tcl86_path}")
            else:
                datas.append((str(location), '_tcl_data'))
                print(f"Added TCL library: {location}")
    
    # 添加找到的 TK 库
    for location in possible_locations:
        if location.exists() and location.name == 'tk':
            # 查找 tk8.6 目录
            tk86_path = location / 'tk8.6'
            if tk86_path.exists():
                datas.append((str(tk86_path), '_tk_data/tk8.6'))
                print(f"Added TK library: {tk86_path}")
            else:
                datas.append((str(location), '_tk_data'))
                print(f"Added TK library: {location}")
        
    # DLLs 目录中的 TCL/TK 相关文件
    python_path = Path(sys.executable).parent
    dlls_path = python_path / 'DLLs'
    if dlls_path.exists():
        for dll_file in dlls_path.glob('t*.dll'):
            datas.append((str(dll_file), '.'))
            print(f"Added DLL: {dll_file}")
            
except ImportError:
    print("Warning: Tkinter not found")

# 添加 tkinter 模块源码
try:
    import tkinter
    tkinter_module_path = Path(tkinter.__file__).parent
    # 将整个 tkinter 模块目录作为数据文件包含
    datas.append((str(tkinter_module_path), 'tkinter'))
    print(f"Added tkinter module source: {tkinter_module_path}")
except ImportError:
    print("Warning: Could not add tkinter module source")

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
    runtime_hooks=['pyi_rth_tkinter_override.py', 'hook-runtime.py'],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 保持 PyInstaller 的内置 tkinter 钩子，与我们的自定义钩子配合使用
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
    
    # 获取 tkinter 模块路径
    tkinter_path = Path(tkinter.__file__).parent.parent
    
    # 查找 TCL/TK 库文件的多个可能位置
    possible_locations = [
        tkinter_path / 'tcl',
        tkinter_path / 'tk', 
        Path(sys.executable).parent / 'tcl',
        Path(sys.executable).parent / 'tk',
        Path(sys.executable).parent.parent / 'tcl',
        Path(sys.executable).parent.parent / 'tk'
    ]
    
    # 添加找到的 TCL 库
    for location in possible_locations:
        if location.exists() and location.name == 'tcl':
            # 查找 tcl8.6 目录
            tcl86_path = location / 'tcl8.6'
            if tcl86_path.exists():
                datas.append((str(tcl86_path), '_tcl_data/tcl8.6'))
                print(f"Added TCL library: {tcl86_path}")
            else:
                datas.append((str(location), '_tcl_data'))
                print(f"Added TCL library: {location}")
    
    # 添加找到的 TK 库
    for location in possible_locations:
        if location.exists() and location.name == 'tk':
            # 查找 tk8.6 目录
            tk86_path = location / 'tk8.6'
            if tk86_path.exists():
                datas.append((str(tk86_path), '_tk_data/tk8.6'))
                print(f"Added TK library: {tk86_path}")
            else:
                datas.append((str(location), '_tk_data'))
                print(f"Added TK library: {location}")
        
    # DLLs 目录中的 TCL/TK 相关文件
    python_path = Path(sys.executable).parent
    dlls_path = python_path / 'DLLs'
    if dlls_path.exists():
        for dll_file in dlls_path.glob('t*.dll'):
            datas.append((str(dll_file), '.'))
            print(f"Added DLL: {dll_file}")
            
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
    runtime_hooks=['pyi_rth_tkinter_override.py', 'hook-runtime.py'],
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
