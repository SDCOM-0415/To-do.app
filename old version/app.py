"""
应用程序入口文件
启动待办事项应用程序
"""

import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import Qt

from config import FONT_PATH, DEFAULT_FONT_FAMILY, DEFAULT_FONT_SIZE
from main_window import TodoMainWindow

def source_path(relative_path):
    """获取资源文件路径"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def setup_font(app):
    """设置应用程序字体"""
    font_path = source_path(FONT_PATH)
    
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                # 使用加载的中文字体
                default_font = QFont(font_families[0], DEFAULT_FONT_SIZE)
                app.setFont(default_font)
                print(f"已加载字体: {font_families[0]}")
                return True
            else:
                print("字体加载失败，使用默认字体")
        else:
            print("字体文件加载失败，使用默认字体")
    else:
        print(f"字体文件不存在: {font_path}，使用默认字体")
    
    # 使用默认字体
    default_font = QFont(DEFAULT_FONT_FAMILY, DEFAULT_FONT_SIZE)
    app.setFont(default_font)
    return False

def setup_global_style(app):
    """设置全局样式"""
    # 强制设置样式引擎，确保跨平台一致性
    app.setStyle("Fusion")
    
    # 全局边框重置 - 彻底去除系统默认边框
    app.setStyleSheet("""
        * {
            border: none !important;
            outline: none !important;
        }
        QWidget {
            border: none !important;
        }
        QLabel {
            border: none !important;
            background: transparent;
        }
        QListWidget {
            border: none !important;
            outline: none !important;
        }
        QListWidget::item {
            border: none !important;
            outline: none !important;
        }
        QListWidget::item:selected {
            border: none !important;
            outline: none !important;
        }
        QListWidget::item:focus {
            border: none !important;
            outline: none !important;
        }
        QLineEdit {
            border: none !important;
        }
    """)

def main():
    """主函数"""
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName("SDCOM 待办事项管理器")
    app.setApplicationVersion("v3.0")
    app.setOrganizationName("SDCOM")
    
    # 设置字体
    setup_font(app)
    
    # 设置全局样式
    setup_global_style(app)
    
    # 创建并显示主窗口
    window = TodoMainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())

if __name__ == "__main__":
    main()