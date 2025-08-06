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

print(f"TCL_LIBRARY: {tcl_dir}")
print(f"TK_LIBRARY: {tk_dir}")
# 使用英文输出，避免编码问题

# 递归收集所有Tcl/Tk文件
def collect_all_files(src_dir, target_prefix):
    collected_data = []
    if not os.path.exists(src_dir):
        print(f"WARNING: Directory does not exist {src_dir}")
        return collected_data
        
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            source_path = os.path.join(root, file)
            # 计算相对路径
            rel_path = os.path.relpath(source_path, os.path.dirname(src_dir))
            # 确保使用正斜杠作为路径分隔符
            target_path = os.path.join(target_prefix, rel_path).replace('\\', '/')
            # 使用PyInstaller期望的格式: (source_path, target_path)
            # 注意：不要使用os.path.dirname，保留完整的目标路径
            collected_data.append((source_path, target_path))
            print(f"Adding file: {source_path} -> {target_path}")
    return collected_data

# 收集Tcl文件
tcl_lib = os.path.join(tcl_dir, 'tcl8.6')
if os.path.exists(tcl_lib):
    print(f"Collecting Tcl files from: {tcl_lib}")
    # 确保目标路径使用正确的格式
    a.datas += collect_all_files(tcl_lib, '_tcl_data/tcl8.6')
    
    # 添加init.tcl文件（这是tkinter初始化所必需的）
    init_tcl = os.path.join(tcl_lib, 'init.tcl')
    if os.path.exists(init_tcl):
        print(f"Adding key file: {init_tcl}")
        a.datas.append((init_tcl, '_tcl_data/tcl8.6/init.tcl'))
else:
    print(f"WARNING: Tcl library directory does not exist: {tcl_lib}")

# 收集Tk文件
tk_lib = os.path.join(tk_dir, 'tk8.6')
if os.path.exists(tk_lib):
    print(f"Collecting Tk files from: {tk_lib}")
    # 确保目标路径使用正确的格式
    a.datas += collect_all_files(tk_lib, '_tcl_data/tk8.6')
    
    # 添加tk.tcl文件（这是tkinter初始化所必需的）
    tk_tcl = os.path.join(tk_lib, 'tk.tcl')
    if os.path.exists(tk_tcl):
        print(f"Adding key file: {tk_tcl}")
        a.datas.append((tk_tcl, '_tcl_data/tk8.6/tk.tcl'))
else:
    print(f"WARNING: Tk library directory does not exist: {tk_lib}")

# 添加环境变量设置
print("Adding environment variable settings to runtime hooks")

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