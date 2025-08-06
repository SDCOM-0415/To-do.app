# -*- mode: python ; coding: utf-8 -*-
# Todo App v0.3.1 - PyInstaller 构建配置

import sys
from pathlib import Path

# 获取项目根目录
try:
    # 尝试使用 __file__ 变量
    project_root = Path(__file__).parent
except NameError:
    # 在 GitHub Actions 环境中，使用当前工作目录
    import os
    project_root = Path(os.getcwd())

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[str(project_root)],
    binaries=[],
    # 初始化数据列表
    datas=[],
    
    # 添加Tcl/Tk库文件
    hiddenimports=[
        'customtkinter',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.colorchooser',
        'PIL',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'pytest',
        'setuptools',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 添加Tcl/Tk库文件
import os
import tkinter

# 获取Tcl/Tk库路径
tcl_dir = os.path.join(os.path.dirname(os.path.dirname(tkinter.__file__)), 'tcl')
tk_dir = os.path.join(os.path.dirname(os.path.dirname(tkinter.__file__)), 'tk')

# 如果路径存在，添加到datas列表
if os.path.exists(tcl_dir):
    tcl_lib = os.path.join(tcl_dir, 'tcl8.6')
    if os.path.exists(tcl_lib):
        a.datas += [(os.path.join(tcl_lib, f), os.path.join('tcl', 'tcl8.6', f)) 
                   for f in os.listdir(tcl_lib) if os.path.isfile(os.path.join(tcl_lib, f))]

if os.path.exists(tk_dir):
    tk_lib = os.path.join(tk_dir, 'tk8.6')
    if os.path.exists(tk_lib):
        a.datas += [(os.path.join(tk_lib, f), os.path.join('tk', 'tk8.6', f)) 
                   for f in os.listdir(tk_lib) if os.path.isfile(os.path.join(tk_lib, f))]

# 过滤掉 None 值
a.datas = [item for item in a.datas if item is not None]

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
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if (project_root / 'icon.ico').exists() else None,
)

# macOS 应用程序包配置
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='TodoApp.app',
        icon='icon.ico' if (project_root / 'icon.ico').exists() else None,
        bundle_identifier='com.sdcom.todoapp',
        info_plist={
            'CFBundleName': 'Todo App',
            'CFBundleDisplayName': 'Todo App v0.3.1',
            'CFBundleVersion': '0.3.1',
            'CFBundleShortVersionString': '0.3.1',
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.14.0',
        },
    )