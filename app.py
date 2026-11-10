#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Todo App v0.3.2 - 程序入口
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
        # 首先检查 tkinter
        import tkinter
        print(f"✓ tkinter 可用")
        
        # 然后检查 customtkinter
        import customtkinter
        print(f"✓ customtkinter 版本: {customtkinter.__version__}")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        return False
    except Exception as e:
        print(f"❌ 依赖检查失败: {e}")
        return False

def setup_environment():
    """设置运行环境"""
    # 设置 DPI 感知（Windows）
    try:
        import ctypes
        if sys.platform == "win32":
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    # 如果是打包环境，尝试设置正确的TCL/TK路径
    if getattr(sys, 'frozen', False):
        # 运行在PyInstaller环境中
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
        
        # 查找有效的TK路径 - 需要找到包含 tk.tcl 的目录
        tk_library_set = False
        for tk_path in possible_tk_paths:
            if os.path.exists(tk_path):
                # 检查是否包含 tk.tcl 文件
                tk_tcl_file = os.path.join(tk_path, 'tk.tcl')
                if os.path.exists(tk_tcl_file):
                    os.environ['TK_LIBRARY'] = tk_path
                    print(f"已设置TK_LIBRARY={tk_path} (找到 tk.tcl)")
                    tk_library_set = True
                    break
                else:
                    print(f"路径 {tk_path} 存在但缺少 tk.tcl 文件")
        
        # 如果没有找到包含 tk.tcl 的路径，尝试其他位置
        if not tk_library_set:
            additional_tk_paths = [
                os.path.join(base_dir, '_tk_data'),
                os.path.join(base_dir, '_tcl_data', 'tcl8.6', 'tk8.6'),
                os.path.join(base_dir, 'lib', 'tk8.6'),
            ]
            
            for tk_path in additional_tk_paths:
                if os.path.exists(tk_path):
                    tk_tcl_file = os.path.join(tk_path, 'tk.tcl')
                    if os.path.exists(tk_tcl_file):
                        os.environ['TK_LIBRARY'] = tk_path
                        print(f"已设置TK_LIBRARY={tk_path} (在备用位置找到 tk.tcl)")
                        tk_library_set = True
                        break
        
        if not tk_library_set:
            print("⚠️ 警告：未找到包含 tk.tcl 的 TK 库路径")
            # 列出 MEIPASS 中的相关文件用于调试
            print("MEIPASS 中的 TK 相关文件:")
            for item in os.listdir(base_dir):
                if 'tk' in item.lower() or 'tcl' in item.lower():
                    item_path = os.path.join(base_dir, item)
                    if os.path.isdir(item_path):
                        print(f"  目录: {item}/")
                        # 检查目录内容
                        try:
                            for subitem in os.listdir(item_path):
                                if subitem.endswith('.tcl'):
                                    print(f"    - {subitem}")
                        except:
                            pass
                    else:
                        print(f"  文件: {item}")

def print_system_info():
    """打印系统信息"""
    # 获取操作系统信息
    platform_name = sys.platform
    if platform_name == "darwin":
        try:
            # 尝试获取真正的 macOS 版本号
            import subprocess
            result = subprocess.run(['sw_vers', '-productVersion'], 
                                  capture_output=True, text=True, check=True)
            macos_version = result.stdout.strip()
            os_display = f"macOS {macos_version}"
        except:
            # 如果获取失败，只显示 macOS 不显示版本号
            os_display = "macOS"
    elif platform_name == "win32":
        os_display = "Windows"
    elif platform_name.startswith("linux"):
        try:
            # 尝试获取 Linux 发行版信息
            import subprocess
            # 优先尝试 lsb_release
            try:
                result = subprocess.run(['lsb_release', '-d'], 
                                      capture_output=True, text=True, check=True)
                distro_info = result.stdout.strip().split('\t')[1] if '\t' in result.stdout else result.stdout.strip()
                os_display = distro_info
            except:
                # 如果 lsb_release 不可用，尝试读取 /etc/os-release
                try:
                    with open('/etc/os-release', 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            if line.startswith('PRETTY_NAME='):
                                os_display = line.split('=')[1].strip().strip('"')
                                break
                        else:
                            os_display = "Linux"
                except:
                    os_display = "Linux"
        except:
            os_display = "Linux"
    else:
        os_display = platform_name
    
    print("=" * 50)
    from config import app_config
    print(f"Todo App v{app_config.version} - 系统信息")
    print("=" * 50)
    print(f"Python 版本: {sys.version}")
    print(f"操作系统: {os_display}")
    print(f"工作目录: {os.getcwd()}")
    print("=" * 50)

def main():
    """主函数"""
    print_system_info()
    
    # 检查依赖
    if not check_dependencies():
        print("❌ 缺少必要依赖，程序无法启动")
        print("请运行: pip install -r requirements.txt")
        # 移除 input() 调用，直接退出
        sys.exit(1)
    
    # 设置环境
    setup_environment()
    
    try:
        # 导入数据库和任务数量
        from database import task_db
        tasks = task_db.get_all_tasks()
        print(f"已加载 {len(tasks)} 个任务")
        
        # 导入并启动主应用
        from main_app import main as run_app
        from config import app_config
        print(f"🚀 启动 Todo App v{app_config.version}...")
        run_app()
    except KeyboardInterrupt:
        print("\n👋 程序被用户中断")
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        # 移除 input() 调用，直接退出
        sys.exit(1)

if __name__ == "__main__":
    main()