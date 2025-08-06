# hook-customtkinter.py
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 收集customtkinter的所有子模块和数据文件
hiddenimports = collect_submodules('customtkinter')
datas = collect_data_files('customtkinter')