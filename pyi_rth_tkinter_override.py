#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义 Tkinter 运行时钩子 - 覆盖 PyInstaller 默认行为
在 PyInstaller 内置钩子之前设置正确的 TCL/TK 环境变量
"""

import os
import sys

def setup_tkinter_environment():
    """设置 Tkinter 环境变量"""
    if not getattr(sys, 'frozen', False):
        return
    
    base_dir = sys._MEIPASS
    
    # 所有可能的 TCL 路径
    tcl_paths = [
        os.path.join(base_dir, '_tcl_data', 'tcl8.6'),
        os.path.join(base_dir, '_tcl_data'),
        os.path.join(base_dir, 'tcl', 'tcl8.6'),
        os.path.join(base_dir, 'tcl'),
        os.path.join(base_dir, 'lib', 'tcl8.6'),
    ]
    
    # 所有可能的 TK 路径
    tk_paths = [
        os.path.join(base_dir, '_tk_data', 'tk8.6'),
        os.path.join(base_dir, '_tk_data'),
        os.path.join(base_dir, '_tcl_data', 'tk8.6'),
        os.path.join(base_dir, '_tcl_data'),
        os.path.join(base_dir, 'tk', 'tk8.6'),
        os.path.join(base_dir, 'tk'),
        os.path.join(base_dir, 'lib', 'tk8.6'),
    ]
    
    # 设置 TCL_LIBRARY
    for tcl_path in tcl_paths:
        if os.path.exists(tcl_path):
            os.environ['TCL_LIBRARY'] = tcl_path
            print(f"[Tkinter Override] 设置 TCL_LIBRARY={tcl_path}")
            break
    else:
        print("[Tkinter Override] 警告：未找到 TCL 库")
    
    # 设置 TK_LIBRARY
    for tk_path in tk_paths:
        if os.path.exists(tk_path):
            os.environ['TK_LIBRARY'] = tk_path
            print(f"[Tkinter Override] 设置 TK_LIBRARY={tk_path}")
            break
    else:
        print("[Tkinter Override] 警告：未找到 TK 库")
    
    # 创建 _tk_data 目录的符号链接（如果不存在）
    tk_data_dir = os.path.join(base_dir, '_tk_data')
    if not os.path.exists(tk_data_dir):
        # 尝试从其他位置创建链接
        for source_path in [
            os.path.join(base_dir, '_tcl_data'),
            os.path.join(base_dir, 'tk'),
        ]:
            if os.path.exists(source_path):
                try:
                    # 在 Windows 上创建目录副本
                    import shutil
                    if os.path.isdir(source_path):
                        shutil.copytree(source_path, tk_data_dir, dirs_exist_ok=True)
                        print(f"[Tkinter Override] 创建 _tk_data 目录副本：{source_path} -> {tk_data_dir}")
                        break
                except Exception as e:
                    print(f"[Tkinter Override] 无法创建 _tk_data 目录：{e}")
    
    # 调试信息
    print(f"[Tkinter Override] MEIPASS: {base_dir}")
    print(f"[Tkinter Override] TCL_LIBRARY: {os.environ.get('TCL_LIBRARY', '未设置')}")
    print(f"[Tkinter Override] TK_LIBRARY: {os.environ.get('TK_LIBRARY', '未设置')}")

# 立即执行设置
setup_tkinter_environment()