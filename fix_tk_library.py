# 修复 TK 库包含问题的辅助脚本
import sys
import os
from pathlib import Path

def find_tk_library():
    """查找并验证 TK 库的完整路径"""
    python_path = Path(sys.executable).parent
    
    # 可能的 TK 库位置
    possible_tk_locations = [
        python_path / 'tcl' / 'tk8.6',
        python_path / 'tk' / 'tk8.6', 
        python_path / 'lib' / 'tk8.6',
        python_path.parent / 'tcl' / 'tk8.6',
        python_path.parent / 'tk' / 'tk8.6',
        python_path.parent / 'lib' / 'tk8.6',
    ]
    
    print("🔍 搜索 TK 库位置...")
    
    for location in possible_tk_locations:
        if location.exists():
            tk_tcl_file = location / 'tk.tcl'
            if tk_tcl_file.exists():
                print(f"✅ 找到完整的 TK 库: {location}")
                print(f"✅ 验证 tk.tcl 存在: {tk_tcl_file}")
                return location
            else:
                print(f"⚠️  找到 TK 目录但缺少 tk.tcl: {location}")
    
    print("❌ 未找到有效的 TK 库")
    return None

def find_tcl_library():
    """查找并验证 TCL 库的完整路径"""
    python_path = Path(sys.executable).parent
    
    # 可能的 TCL 库位置
    possible_tcl_locations = [
        python_path / 'tcl' / 'tcl8.6',
        python_path / 'lib' / 'tcl8.6',
        python_path.parent / 'tcl' / 'tcl8.6',
        python_path.parent / 'lib' / 'tcl8.6',
    ]
    
    print("🔍 搜索 TCL 库位置...")
    
    for location in possible_tcl_locations:
        if location.exists():
            init_tcl_file = location / 'init.tcl'
            if init_tcl_file.exists():
                print(f"✅ 找到完整的 TCL 库: {location}")
                print(f"✅ 验证 init.tcl 存在: {init_tcl_file}")
                return location
            else:
                print(f"⚠️  找到 TCL 目录但缺少 init.tcl: {location}")
    
    print("❌ 未找到有效的 TCL 库")
    return None

if __name__ == "__main__":
    print("=" * 50)
    print("TK/TCL 库检测工具")
    print("=" * 50)
    
    tcl_lib = find_tcl_library()
    tk_lib = find_tk_library()
    
    print("\n" + "=" * 50)
    print("检测结果:")
    print(f"TCL 库: {tcl_lib if tcl_lib else '未找到'}")
    print(f"TK 库: {tk_lib if tk_lib else '未找到'}")
    print("=" * 50)