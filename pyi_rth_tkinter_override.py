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
    
    # 所有可能的 TK 路径 - 根据错误信息调整优先级
    tk_paths = [
        os.path.join(base_dir, '_tk_data'),  # 错误显示tk.tcl应该直接在这里
        os.path.join(base_dir, '_tk_data', 'tk8.6'),
        os.path.join(base_dir, '_tcl_data', 'tcl8.6', 'tk8.6'),  # 有时tk在tcl目录下
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
    
    # 设置 TK_LIBRARY - 优先查找包含 tk.tcl 的目录
    tk_library_set = False
    for tk_path in tk_paths:
        if os.path.exists(tk_path):
            # 检查是否包含 tk.tcl 文件
            tk_tcl_file = os.path.join(tk_path, 'tk.tcl')
            if os.path.exists(tk_tcl_file):
                os.environ['TK_LIBRARY'] = tk_path
                print(f"[Tkinter Override] 设置 TK_LIBRARY={tk_path} (包含 tk.tcl)")
                tk_library_set = True
                break
            else:
                print(f"[Tkinter Override] 跳过 {tk_path} (缺少 tk.tcl)")
    
    # 如果没找到包含 tk.tcl 的目录，使用第一个存在的目录
    if not tk_library_set:
        for tk_path in tk_paths:
            if os.path.exists(tk_path):
                os.environ['TK_LIBRARY'] = tk_path
                print(f"[Tkinter Override] 设置 TK_LIBRARY={tk_path} (备用选择)")
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
    
    # 尝试直接导入 tkinter 模块进行测试
    try:
        # 确保 _tkinter 模块可以被找到
        tkinter_pyd = os.path.join(base_dir, '_tkinter.pyd')
        if os.path.exists(tkinter_pyd):
            print(f"[Tkinter Override] 找到 _tkinter.pyd: {tkinter_pyd}")
        
        # 尝试导入 _tkinter
        import _tkinter
        print("[Tkinter Override] ✓ _tkinter 模块导入成功")
        
        # 尝试导入 tkinter
        import tkinter
        print("[Tkinter Override] ✓ tkinter 模块导入成功")
        
    except ImportError as e:
        print(f"[Tkinter Override] ❌ 模块导入失败: {e}")
        # 尝试添加更多调试信息
        print(f"[Tkinter Override] Python 路径: {sys.path}")
        
        # 检查是否有其他 tkinter 相关文件
        for item in os.listdir(base_dir):
            if 'tkinter' in item.lower() or 'tcl' in item.lower() or 'tk' in item.lower():
                print(f"[Tkinter Override] 相关文件: {item}")
                
    except Exception as e:
        print(f"[Tkinter Override] ❌ 其他错误: {e}")

# 立即执行设置
setup_tkinter_environment()
