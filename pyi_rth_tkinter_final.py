#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终的 Tkinter 运行时钩子 - 确保 tk.tcl 能被正确找到
"""

import os
import sys
import shutil

def setup_tkinter_final():
    """最终设置 Tkinter 环境"""
    if not getattr(sys, 'frozen', False):
        return
    
    base_dir = sys._MEIPASS
    print(f"[Tkinter Final] MEIPASS: {base_dir}")
    
    # 检查当前的目录结构
    tk_data_dir = os.path.join(base_dir, '_tk_data')
    tcl_data_dir = os.path.join(base_dir, '_tcl_data')
    
    print(f"[Tkinter Final] 检查目录结构:")
    for check_dir in [tk_data_dir, tcl_data_dir]:
        if os.path.exists(check_dir):
            print(f"[Tkinter Final] ✓ {check_dir} 存在")
            # 列出目录内容
            try:
                contents = os.listdir(check_dir)
                for item in contents[:10]:  # 只显示前10个项目
                    item_path = os.path.join(check_dir, item)
                    if os.path.isfile(item_path):
                        print(f"[Tkinter Final]   文件: {item}")
                    else:
                        print(f"[Tkinter Final]   目录: {item}/")
                if len(contents) > 10:
                    print(f"[Tkinter Final]   ... 还有 {len(contents) - 10} 个项目")
            except Exception as e:
                print(f"[Tkinter Final] 无法列出目录内容: {e}")
        else:
            print(f"[Tkinter Final] ❌ {check_dir} 不存在")
    
    # 查找 tk.tcl 文件的实际位置
    tk_tcl_locations = []
    for root, dirs, files in os.walk(base_dir):
        if 'tk.tcl' in files:
            tk_tcl_path = os.path.join(root, 'tk.tcl')
            tk_tcl_locations.append(tk_tcl_path)
            print(f"[Tkinter Final] 找到 tk.tcl: {tk_tcl_path}")
    
    if not tk_tcl_locations:
        print("[Tkinter Final] ❌ 未找到 tk.tcl 文件")
        return
    
    # 使用第一个找到的 tk.tcl 文件位置
    tk_tcl_file = tk_tcl_locations[0]
    tk_library_dir = os.path.dirname(tk_tcl_file)
    
    # 设置环境变量指向包含 tk.tcl 的实际目录
    os.environ['TK_LIBRARY'] = tk_library_dir
    print(f"[Tkinter Final] 设置 TK_LIBRARY={tk_library_dir}")
    
    # 确保 TCL_LIBRARY 也正确设置
    tcl_library_candidates = [
        os.path.join(base_dir, '_tcl_data', 'tcl8.6'),
        os.path.join(base_dir, '_tcl_data'),
        os.path.join(base_dir, 'tcl', 'tcl8.6'),
    ]
    
    for tcl_path in tcl_library_candidates:
        if os.path.exists(tcl_path):
            init_tcl = os.path.join(tcl_path, 'init.tcl')
            if os.path.exists(init_tcl):
                os.environ['TCL_LIBRARY'] = tcl_path
                print(f"[Tkinter Final] 设置 TCL_LIBRARY={tcl_path}")
                break
    
    # 如果 _tk_data 目录不存在或为空，创建符号链接
    if not os.path.exists(tk_data_dir) or not os.listdir(tk_data_dir):
        try:
            if os.path.exists(tk_data_dir):
                shutil.rmtree(tk_data_dir)
            
            # 创建指向实际 TK 库的链接
            if os.path.exists(tk_library_dir):
                shutil.copytree(tk_library_dir, tk_data_dir)
                print(f"[Tkinter Final] 创建 _tk_data 目录副本: {tk_library_dir} -> {tk_data_dir}")
                
                # 验证 tk.tcl 现在在正确位置
                new_tk_tcl = os.path.join(tk_data_dir, 'tk.tcl')
                if os.path.exists(new_tk_tcl):
                    print(f"[Tkinter Final] ✓ tk.tcl 现在位于: {new_tk_tcl}")
                    # 更新环境变量指向新位置
                    os.environ['TK_LIBRARY'] = tk_data_dir
                    print(f"[Tkinter Final] 更新 TK_LIBRARY={tk_data_dir}")
                
        except Exception as e:
            print(f"[Tkinter Final] 创建 _tk_data 目录失败: {e}")
    
    # 最终验证
    final_tk_library = os.environ.get('TK_LIBRARY')
    if final_tk_library:
        final_tk_tcl = os.path.join(final_tk_library, 'tk.tcl')
        if os.path.exists(final_tk_tcl):
            print(f"[Tkinter Final] ✓ 最终验证成功: tk.tcl 位于 {final_tk_tcl}")
        else:
            print(f"[Tkinter Final] ❌ 最终验证失败: {final_tk_tcl} 不存在")
    
    print(f"[Tkinter Final] 最终环境变量:")
    print(f"[Tkinter Final] TCL_LIBRARY: {os.environ.get('TCL_LIBRARY', '未设置')}")
    print(f"[Tkinter Final] TK_LIBRARY: {os.environ.get('TK_LIBRARY', '未设置')}")

# 立即执行设置
setup_tkinter_final()