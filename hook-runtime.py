# hook-runtime.py - 运行时钩子，确保tkinter正确加载
import os
import sys

# 如果是打包环境，设置正确的TCL/TK路径
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
    
    # 尝试多种可能的路径
    possible_tcl_paths = [
        os.path.join(base_dir, '_tcl_data', 'tcl8.6'),  # 主要路径
        os.path.join(base_dir, 'tcl', 'tcl8.6'),        # 备用路径1
        os.path.join(base_dir, 'tcl')                   # 备用路径2
    ]
    
    possible_tk_paths = [
        os.path.join(base_dir, '_tcl_data', 'tk8.6'),   # 主要路径
        os.path.join(base_dir, 'tk', 'tk8.6'),          # 备用路径1
        os.path.join(base_dir, 'tk')                    # 备用路径2
    ]
    
    # 查找有效的TCL路径
    for tcl_path in possible_tcl_paths:
        if os.path.exists(tcl_path):
            os.environ['TCL_LIBRARY'] = tcl_path
            print(f"已设置TCL_LIBRARY={tcl_path}")
            break
    
    # 查找有效的TK路径
    for tk_path in possible_tk_paths:
        if os.path.exists(tk_path):
            os.environ['TK_LIBRARY'] = tk_path
            print(f"已设置TK_LIBRARY={tk_path}")
            break
    
    # 打印调试信息
    print(f"MEIPASS路径: {base_dir}")
    print(f"当前TCL_LIBRARY: {os.environ.get('TCL_LIBRARY', '未设置')}")
    print(f"当前TK_LIBRARY: {os.environ.get('TK_LIBRARY', '未设置')}")