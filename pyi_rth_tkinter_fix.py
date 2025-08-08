# PyInstaller 运行时钩子：修复 tkinter 导入问题
# 文件名: pyi_rth_tkinter_fix.py

import sys
import os
from pathlib import Path

def setup_tkinter_environment():
    """设置 tkinter 运行环境"""
    try:
        # 获取应用程序目录
        if hasattr(sys, '_MEIPASS'):
            app_dir = Path(sys._MEIPASS)
            print(f"🔧 MEIPASS 目录: {app_dir}")
        else:
            app_dir = Path(__file__).parent
            print(f"🔧 应用目录: {app_dir}")
        
        # 1. 设置 TCL/TK 环境变量
        tcl_data_path = app_dir / '_tcl_data'
        tk_data_path = app_dir / '_tk_data'
        
        if tcl_data_path.exists():
            # 查找 tcl8.6 目录
            tcl86_path = tcl_data_path / 'tcl8.6'
            if tcl86_path.exists():
                os.environ['TCL_LIBRARY'] = str(tcl86_path)
                print(f"✅ 设置 TCL_LIBRARY: {tcl86_path}")
            else:
                os.environ['TCL_LIBRARY'] = str(tcl_data_path)
                print(f"✅ 设置 TCL_LIBRARY: {tcl_data_path}")
        
        if tk_data_path.exists():
            # 查找 tk8.6 目录
            tk86_path = tk_data_path / 'tk8.6'
            if tk86_path.exists():
                os.environ['TK_LIBRARY'] = str(tk86_path)
                print(f"✅ 设置 TK_LIBRARY: {tk86_path}")
                # 检查 tk.tcl 文件
                tk_tcl_file = tk86_path / 'tk.tcl'
                if tk_tcl_file.exists():
                    print(f"✅ 找到 tk.tcl: {tk_tcl_file}")
                else:
                    print(f"❌ 未找到 tk.tcl 在: {tk86_path}")
            else:
                os.environ['TK_LIBRARY'] = str(tk_data_path)
                print(f"✅ 设置 TK_LIBRARY: {tk_data_path}")
                # 检查 tk.tcl 文件
                tk_tcl_file = tk_data_path / 'tk.tcl'
                if tk_tcl_file.exists():
                    print(f"✅ 找到 tk.tcl: {tk_tcl_file}")
                else:
                    print(f"❌ 未找到 tk.tcl 在: {tk_data_path}")
        
        # 2. 确保 tkinter 模块在 sys.path 中
        tkinter_path = app_dir / 'tkinter'
        if tkinter_path.exists():
            if str(app_dir) not in sys.path:
                sys.path.insert(0, str(app_dir))
                print(f"✅ 添加到 sys.path: {app_dir}")
        
        # 3. 预加载 _tkinter 模块
        try:
            import _tkinter
            print("✅ _tkinter 模块加载成功")
        except ImportError as e:
            print(f"❌ _tkinter 模块加载失败: {e}")
        
        # 4. 尝试导入 tkinter
        try:
            import tkinter
            print("✅ tkinter 模块导入成功")
            return True
        except ImportError as e:
            print(f"❌ tkinter 模块导入失败: {e}")
            
            # 尝试手动设置模块路径
            if tkinter_path.exists():
                import importlib.util
                spec = importlib.util.spec_from_file_location("tkinter", tkinter_path / "__init__.py")
                if spec and spec.loader:
                    tkinter_module = importlib.util.module_from_spec(spec)
                    sys.modules['tkinter'] = tkinter_module
                    spec.loader.exec_module(tkinter_module)
                    print("✅ 手动加载 tkinter 模块成功")
                    return True
            
            return False
            
    except Exception as e:
        print(f"❌ 设置 tkinter 环境时出错: {e}")
        return False

# 在导入时立即执行设置
print("🚀 开始设置 tkinter 环境...")
setup_success = setup_tkinter_environment()
if setup_success:
    print("✅ tkinter 环境设置完成")
else:
    print("❌ tkinter 环境设置失败")