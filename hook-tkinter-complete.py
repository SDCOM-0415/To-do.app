# PyInstaller 钩子文件：确保完整包含 tkinter 模块
# 文件名: hook-tkinter-complete.py

from PyInstaller.utils.hooks import collect_all, collect_submodules, collect_data_files
import os
import sys
from pathlib import Path

# 收集所有 tkinter 相关模块
datas, binaries, hiddenimports = collect_all('tkinter')

# 额外的隐藏导入
additional_imports = [
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
    '_tkinter',
]

hiddenimports.extend(additional_imports)

# 确保包含 tkinter 模块的源文件
try:
    import tkinter
    tkinter_path = Path(tkinter.__file__).parent
    
    # 添加所有 .py 文件
    for py_file in tkinter_path.rglob('*.py'):
        if not py_file.name.startswith('__pycache__'):
            rel_path = py_file.relative_to(tkinter_path.parent)
            datas.append((str(py_file), str(rel_path.parent)))
            
    print(f"Hook: Added tkinter module files from {tkinter_path}")
    
except ImportError as e:
    print(f"Hook: Failed to import tkinter: {e}")

# 添加 TCL/TK 库文件
try:
    python_path = Path(sys.executable).parent
    
    # 查找 TCL/TK 库
    for lib_name in ['tcl', 'tk']:
        lib_path = python_path / lib_name
        if lib_path.exists():
            # 查找版本目录
            version_dir = lib_path / f'{lib_name}8.6'
            if version_dir.exists():
                datas.append((str(version_dir), f'_{lib_name}_data/{lib_name}8.6'))
            else:
                datas.append((str(lib_path), f'_{lib_name}_data'))
            print(f"Hook: Added {lib_name.upper()} library from {lib_path}")
    
    # 添加相关 DLL 文件
    dlls_path = python_path / 'DLLs'
    if dlls_path.exists():
        for dll_file in dlls_path.glob('t*.dll'):
            binaries.append((str(dll_file), '.'))
            print(f"Hook: Added DLL {dll_file.name}")
            
except Exception as e:
    print(f"Hook: Error adding TCL/TK libraries: {e}")

print(f"Hook: tkinter hook completed - {len(datas)} data files, {len(binaries)} binaries, {len(hiddenimports)} hidden imports")