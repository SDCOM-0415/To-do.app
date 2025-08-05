#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Todo App v0.3 - 程序入口
现代化跨平台待办事项管理器
支持 Windows、Linux、macOS 和深色模式
"""

import sys
import os
from pathlib import Path

# 添加当前目录到 Python 路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_dependencies():
    """检查依赖包"""
    try:
        import customtkinter
        print(f"✓ customtkinter 版本: {customtkinter.__version__}")
        
        # 检查 macOS 版本兼容性
        if sys.platform == "darwin":
            import platform
            version = platform.mac_ver()[0]
            if version:
                major, minor, patch = map(int, version.split('.'))
                if major == 14 and minor < 7:
                    print(f"⚠️  警告: macOS {version} 与 customtkinter 不兼容")
                    print("🔄 将自动使用 Tkinter 备用版本")
                    return False  # 直接返回 False，使用备用版本
        
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"⚠️  依赖检查警告: {e}")
        return False  # 有问题就使用备用版本

def setup_environment():
    """设置运行环境"""
    # 设置 DPI 感知（Windows）
    try:
        import ctypes
        if sys.platform == "win32":
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    # 设置环境变量
    os.environ['TCL_LIBRARY'] = ''
    os.environ['TK_LIBRARY'] = ''

def print_system_info():
    """打印系统信息"""
    print("=" * 50)
    print("Todo App v0.3 - 系统信息")
    print("=" * 50)
    print(f"Python 版本: {sys.version}")
    print(f"操作系统: {sys.platform}")
    print(f"工作目录: {os.getcwd()}")
    print("=" * 50)

def main():
    """主函数"""
    print_system_info()
    
    # 检查依赖
    if not check_dependencies():
        print("\n🔄 尝试使用 Tkinter 备用版本...")
        try:
            from app_tkinter import main as run_tkinter_app
            run_tkinter_app()
            return
        except Exception as e:
            print(f"❌ Tkinter 版本也无法启动: {e}")
            input("按回车键退出...")
            sys.exit(1)
    
    # 设置环境
    setup_environment()
    
    try:
        # 导入并启动主应用
        from main_app import main as run_app
        print("🚀 启动 Todo App v0.3...")
        run_app()
    except KeyboardInterrupt:
        print("\n👋 程序被用户中断")
    except Exception as e:
        print(f"❌ CustomTkinter 版本运行出错: {e}")
        print("🔄 自动切换到 Tkinter 备用版本...")
        
        try:
            from app_tkinter import main as run_tkinter_app
            run_tkinter_app()
        except Exception as e2:
            print(f"❌ Tkinter 版本也无法启动: {e2}")
            import traceback
            traceback.print_exc()
            input("按回车键退出...")
            sys.exit(1)

if __name__ == "__main__":
    main()