#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 TK 库设置的脚本
用于验证 PyInstaller 打包后的应用程序是否能正确找到 tk.tcl
"""

import os
import sys
from pathlib import Path

def test_tk_environment():
    """测试 TK 环境设置"""
    print("=" * 60)
    print("TK 环境测试")
    print("=" * 60)
    
    # 检查是否在 PyInstaller 环境中
    if hasattr(sys, '_MEIPASS'):
        meipass = Path(sys._MEIPASS)
        print(f"✅ 检测到 PyInstaller 环境")
        print(f"📁 MEIPASS 目录: {meipass}")
    else:
        print("ℹ️  运行在开发环境中")
        meipass = Path(__file__).parent
    
    # 检查环境变量
    tcl_lib = os.environ.get('TCL_LIBRARY')
    tk_lib = os.environ.get('TK_LIBRARY')
    
    print(f"\n🔧 环境变量:")
    print(f"   TCL_LIBRARY: {tcl_lib}")
    print(f"   TK_LIBRARY: {tk_lib}")
    
    # 验证 TCL 库
    if tcl_lib and Path(tcl_lib).exists():
        init_tcl = Path(tcl_lib) / 'init.tcl'
        if init_tcl.exists():
            print(f"✅ TCL 库验证成功: {init_tcl}")
        else:
            print(f"❌ TCL 库缺少 init.tcl: {tcl_lib}")
    else:
        print(f"❌ TCL 库路径无效: {tcl_lib}")
    
    # 验证 TK 库 - 这是关键
    if tk_lib and Path(tk_lib).exists():
        tk_tcl = Path(tk_lib) / 'tk.tcl'
        if tk_tcl.exists():
            print(f"✅ TK 库验证成功: {tk_tcl}")
        else:
            print(f"❌ TK 库缺少 tk.tcl: {tk_lib}")
            # 列出 TK 库目录内容
            print(f"📋 TK 库目录内容:")
            try:
                for item in Path(tk_lib).iterdir():
                    print(f"   - {item.name}")
            except Exception as e:
                print(f"   无法列出目录内容: {e}")
    else:
        print(f"❌ TK 库路径无效: {tk_lib}")
    
    # 测试模块导入
    print(f"\n🧪 模块导入测试:")
    
    try:
        import _tkinter
        print("✅ _tkinter 模块导入成功")
    except ImportError as e:
        print(f"❌ _tkinter 模块导入失败: {e}")
        return False
    
    try:
        import tkinter
        print("✅ tkinter 模块导入成功")
    except ImportError as e:
        print(f"❌ tkinter 模块导入失败: {e}")
        return False
    
    # 测试 Tkinter 窗口创建
    print(f"\n🪟 窗口创建测试:")
    try:
        root = tkinter.Tk()
        root.withdraw()  # 隐藏窗口
        print("✅ Tkinter 窗口创建成功")
        root.destroy()
        return True
    except Exception as e:
        print(f"❌ Tkinter 窗口创建失败: {e}")
        return False

if __name__ == "__main__":
    success = test_tk_environment()
    print("\n" + "=" * 60)
    if success:
        print("🎉 所有测试通过！TK 环境设置正确。")
    else:
        print("💥 测试失败！需要修复 TK 环境设置。")
    print("=" * 60)