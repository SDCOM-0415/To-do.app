# hook-tkinter.py
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os
import tkinter

# 收集tkinter的所有子模块
hiddenimports = collect_submodules('tkinter')

# 获取Tcl/Tk库路径
tcl_dir = os.path.join(os.path.dirname(os.path.dirname(tkinter.__file__)), 'tcl')
tk_dir = os.path.join(os.path.dirname(os.path.dirname(tkinter.__file__)), 'tk')

# 收集Tcl/Tk数据文件
datas = []

# 添加tcl库文件
tcl_lib = os.path.join(tcl_dir, 'tcl8.6')
if os.path.exists(tcl_lib):
    for root, dirs, files in os.walk(tcl_lib):
        for file in files:
            source = os.path.join(root, file)
            dest = os.path.join('tcl', os.path.relpath(source, tcl_dir))
            datas.append((source, os.path.dirname(dest)))

# 添加tk库文件
tk_lib = os.path.join(tk_dir, 'tk8.6')
if os.path.exists(tk_lib):
    for root, dirs, files in os.walk(tk_lib):
        for file in files:
            source = os.path.join(root, file)
            dest = os.path.join('tk', os.path.relpath(source, tk_dir))
            datas.append((source, os.path.dirname(dest)))