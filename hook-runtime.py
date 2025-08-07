#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Todo App v0.3.1 - PyInstaller Runtime Hook
Ensures tkinter loads correctly in packaged environment
"""

import os
import sys

# If running in packaged environment, set correct TCL/TK paths
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
    
    # 扩展的可能路径列表
    possible_tcl_paths = [
        os.path.join(base_dir, '_tcl_data', 'tcl8.6'),  # PyInstaller 默认路径
        os.path.join(base_dir, '_tcl_data'),            # 备用路径
        os.path.join(base_dir, 'tcl', 'tcl8.6'),        # 自定义路径 1
        os.path.join(base_dir, 'tcl'),                  # 自定义路径 2
        os.path.join(base_dir, 'lib', 'tcl8.6'),        # 可能的 lib 路径
        os.path.join(base_dir, 'Library', 'lib', 'tcl8.6'),  # Conda 环境路径
    ]
    
    possible_tk_paths = [
        os.path.join(base_dir, '_tk_data', 'tk8.6'),    # PyInstaller 期望的路径
        os.path.join(base_dir, '_tk_data'),             # PyInstaller 期望的备用路径
        os.path.join(base_dir, '_tcl_data', 'tk8.6'),   # 旧的默认路径
        os.path.join(base_dir, '_tcl_data'),            # 旧的备用路径
        os.path.join(base_dir, 'tk', 'tk8.6'),          # 自定义路径 1
        os.path.join(base_dir, 'tk'),                   # 自定义路径 2
        os.path.join(base_dir, 'lib', 'tk8.6'),         # 可能的 lib 路径
        os.path.join(base_dir, 'Library', 'lib', 'tk8.6'),   # Conda 环境路径
    ]
    
    # 调试：列出 MEIPASS 目录内容
    print(f"MEIPASS 目录: {base_dir}")
    try:
        print("MEIPASS 内容:")
        for item in os.listdir(base_dir):
            item_path = os.path.join(base_dir, item)
            if os.path.isdir(item_path):
                print(f"  目录: {item}")
                # 如果是可能包含 tcl/tk 的目录，列出其内容
                if item in ['_tcl_data', 'tcl', 'tk', 'lib', 'Library']:
                    try:
                        for subitem in os.listdir(item_path):
                            print(f"    - {subitem}")
                    except:
                        pass
            else:
                print(f"  文件: {item}")
    except Exception as e:
        print(f"无法列出 MEIPASS 内容: {e}")
    
    # 查找有效的 TCL 路径
    tcl_found = False
    for tcl_path in possible_tcl_paths:
        if os.path.exists(tcl_path):
            os.environ['TCL_LIBRARY'] = tcl_path
            print(f"✓ 设置 TCL_LIBRARY={tcl_path}")
            tcl_found = True
            break
    
    if not tcl_found:
        print("✗ 未找到有效的 TCL 库路径")
    
    # 查找有效的 TK 路径
    tk_found = False
    for tk_path in possible_tk_paths:
        if os.path.exists(tk_path):
            os.environ['TK_LIBRARY'] = tk_path
            print(f"✓ 设置 TK_LIBRARY={tk_path}")
            tk_found = True
            break
    
    if not tk_found:
        print("✗ 未找到有效的 TK 库路径")
    
    # 最终状态
    print(f"最终 TCL_LIBRARY: {os.environ.get('TCL_LIBRARY', '未设置')}")
    print(f"最终 TK_LIBRARY: {os.environ.get('TK_LIBRARY', '未设置')}")
