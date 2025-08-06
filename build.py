#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Todo App v0.3.1 - 本地构建脚本
用于在本地环境构建可执行文件
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def main():
    """主构建函数"""
    print("=" * 60)
    print("Todo App v0.3.1 - 本地构建脚本")
    print("=" * 60)
    
    # 检查 PyInstaller
    try:
        import PyInstaller
        print(f"✓ PyInstaller 版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller 未安装")
        print("请运行: pip install pyinstaller")
        return False
    
    # 检查依赖
    try:
        import customtkinter
        print(f"✓ CustomTkinter 版本: {customtkinter.__version__}")
    except ImportError:
        print("❌ CustomTkinter 未安装")
        print("请运行: pip install -r requirements.txt")
        return False
    
    # 获取平台信息
    system = platform.system()
    arch = platform.machine()
    
    print(f"✓ 构建平台: {system} {arch}")
    
    # 确定输出文件名
    if system == "Windows":
        output_name = f"Todo-App-v0.3.1-Windows-{arch}"
        exe_ext = ".exe"
    elif system == "Darwin":
        output_name = f"Todo-App-v0.3.1-macOS-{arch}"
        exe_ext = ""
    elif system == "Linux":
        output_name = f"Todo-App-v0.3.1-Linux-{arch}"
        exe_ext = ""
    else:
        output_name = f"Todo-App-v0.3.1-{system}-{arch}"
        exe_ext = ""
    
    print(f"✓ 输出文件名: {output_name}")
    
    # 构建命令
    build_cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "TodoApp",
        "--distpath", "dist",
        "--workpath", "build",
        "--specpath", ".",
        "app.py"
    ]
    
    # 添加图标（如果存在）
    icon_path = Path("icon.ico")
    if icon_path.exists():
        build_cmd.extend(["--icon", str(icon_path)])
        print("✓ 使用自定义图标")
    
    # 添加隐藏导入
    hidden_imports = [
        "customtkinter",
        "tkinter",
        "tkinter.ttk",
        "tkinter.messagebox",
        "tkinter.filedialog",
        "tkinter.colorchooser",
    ]
    
    for module in hidden_imports:
        build_cmd.extend(["--hidden-import", module])
    
    print("\n开始构建...")
    print("构建命令:", " ".join(build_cmd))
    print("-" * 60)
    
    try:
        # 执行构建
        result = subprocess.run(build_cmd, check=True)
        
        if result.returncode == 0:
            print("-" * 60)
            print("✅ 构建成功！")
            
            # 重命名输出文件
            original_path = Path("dist") / f"TodoApp{exe_ext}"
            new_path = Path("dist") / f"{output_name}{exe_ext}"
            
            if original_path.exists():
                original_path.rename(new_path)
                print(f"✓ 输出文件: {new_path}")
                
                # 显示文件大小
                file_size = new_path.stat().st_size / (1024 * 1024)
                print(f"✓ 文件大小: {file_size:.1f} MB")
                
                # 创建压缩包
                if system == "Windows":
                    archive_name = f"{output_name}.zip"
                    import zipfile
                    with zipfile.ZipFile(f"dist/{archive_name}", 'w', zipfile.ZIP_DEFLATED) as zf:
                        zf.write(new_path, new_path.name)
                    print(f"✓ 压缩包: dist/{archive_name}")
                else:
                    archive_name = f"{output_name}.tar.gz"
                    import tarfile
                    with tarfile.open(f"dist/{archive_name}", 'w:gz') as tf:
                        tf.add(new_path, new_path.name)
                    print(f"✓ 压缩包: dist/{archive_name}")
                
                print("\n🎉 构建完成！")
                print(f"可执行文件位于: {new_path}")
                return True
            else:
                print("❌ 找不到构建输出文件")
                return False
        else:
            print("❌ 构建失败")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建过程出错: {e}")
        return False
    except Exception as e:
        print(f"❌ 构建失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)