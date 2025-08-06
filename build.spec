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
    
    # 添加Tcl/Tk库文件和所有必要的依赖
    hiddenimports=[
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
    ],
    hookspath=['.'],  # 添加当前目录作为hooks路径
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
import shutil
from pathlib import Path

# 获取Tcl/Tk库路径
tcl_dir = os.path.join(os.path.dirname(os.path.dirname(tkinter.__file__)), 'tcl')
tk_dir = os.path.join(os.path.dirname(os.path.dirname(tkinter.__file__)), 'tk')

print(f"Tcl目录: {tcl_dir}")
print(f"Tk目录: {tk_dir}")

# 递归收集所有Tcl/Tk文件
def collect_all_files(src_dir, target_prefix):
    collected_data = []
    if not os.path.exists(src_dir):
        print(f"警告: 目录不存在 {src_dir}")
        return collected_data
        
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            source_path = os.path.join(root, file)
            # 计算相对路径
            rel_path = os.path.relpath(source_path, os.path.dirname(src_dir))
            target_path = os.path.join(target_prefix, rel_path)
            collected_data.append((source_path, os.path.dirname(target_path)))
            print(f"添加文件: {source_path} -> {os.path.dirname(target_path)}")
    return collected_data

# 收集Tcl文件
tcl_lib = os.path.join(tcl_dir, 'tcl8.6')
if os.path.exists(tcl_lib):
    print(f"收集Tcl文件从: {tcl_lib}")
    a.datas += collect_all_files(tcl_lib, '_tcl_data/tcl8.6')
else:
    print(f"警告: Tcl库目录不存在: {tcl_lib}")

# 收集Tk文件
tk_lib = os.path.join(tk_dir, 'tk8.6')
if os.path.exists(tk_lib):
    print(f"收集Tk文件从: {tk_lib}")
    a.datas += collect_all_files(tk_lib, '_tcl_data/tk8.6')
else:
    print(f"警告: Tk库目录不存在: {tk_lib}")

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
    console=True,  # 临时启用控制台窗口以显示错误信息
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