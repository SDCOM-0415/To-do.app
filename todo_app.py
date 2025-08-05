#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
待办事项应用程序
使用 PySide6 (Qt for Python) 构建的现代化跨平台待办事项应用
支持 Windows, macOS 和 Linux
支持深色/浅色模式自动切换
"""

import os
import sys
import json
from datetime import datetime

# 导入 PySide6 模块
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QLabel,
    QMessageBox, QMenu, QCheckBox, QStyle, QSplitter, QFrame
)
from PySide6.QtCore import Qt, Signal, Slot, QSize, QTimer
from PySide6.QtGui import QIcon, QFont, QColor, QPalette, QAction, QFontDatabase

# 资源文件目录访问
def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 自定义待办事项项目组件
class TodoListItem(QWidget):
    deleted = Signal(QListWidgetItem)
    completed = Signal(QListWidgetItem, bool)
    
    def __init__(self, text, parent=None, completed=False, is_dark_mode=False):
        super().__init__(parent)
        self.text = text
        self.completed = completed
        self.is_dark_mode = is_dark_mode
        
        # 创建布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # 创建完成复选框
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(completed)
        self.checkbox.stateChanged.connect(self.on_state_changed)
        layout.addWidget(self.checkbox)
        
        # 创建任务文本标签
        self.label = QLabel(text)
        font = QFont("NotoSansSC", 10)
        self.label.setFont(font)
        self.update_label_style()
        layout.addWidget(self.label, 1)  # 1 表示伸展因子
        
        # 创建删除按钮
        self.delete_button = QPushButton()
        self.delete_button.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.delete_button.setFixedSize(24, 24)
        self.delete_button.setStyleSheet("QPushButton { border: none; }")
        self.delete_button.clicked.connect(self.on_delete_clicked)
        layout.addWidget(self.delete_button)
        
        self.setLayout(layout)
    
    def update_label_style(self):
        if self.completed:
            if self.is_dark_mode:
                self.label.setStyleSheet("text-decoration: line-through; color: #888888;")
            else:
                self.label.setStyleSheet("text-decoration: line-through; color: gray;")
        else:
            if self.is_dark_mode:
                self.label.setStyleSheet("color: #e0e0e0;")
            else:
                self.label.setStyleSheet("color: #333333;")
    
    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.update_label_style()
    
    def on_state_changed(self, state):
        is_completed = (state == Qt.CheckState.Checked.value)
        self.completed = is_completed
        self.update_label_style()
        parent_item = self.parent_item if hasattr(self, 'parent_item') else None
        self.completed.emit(parent_item, is_completed)
    
    def on_delete_clicked(self):
        parent_item = self.parent_item if hasattr(self, 'parent_item') else None
        self.deleted.emit(parent_item)

# 主窗口类
class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口属性
        self.setWindowTitle("SDCOM的待办项目")
        self.setWindowIcon(QIcon(source_path("res/icon.jpg")))
        self.setMinimumSize(500, 600)
        
        # 检测系统主题
        self.is_dark_mode = self.detect_dark_mode()
        
        # 设置应用样式
        self.setup_style()
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # 创建标题标签
        title_label = QLabel("我的待办事项")
        title_font = QFont("NotoSansSC", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # 创建任务列表
        self.todo_list = QListWidget()
        # 移除方框设计，使用更简洁的样式
        self.update_list_style(remove_borders=True)
        self.todo_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.todo_list.customContextMenuRequested.connect(self.show_context_menu)
        main_layout.addWidget(self.todo_list, 1)  # 1 表示伸展因子
        
        # 创建输入区域
        input_layout = QHBoxLayout()
        
        # 创建任务输入框
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("输入新任务...")
        self.update_input_style()
        self.task_input.returnPressed.connect(self.add_task)
        input_layout.addWidget(self.task_input, 1)  # 1 表示伸展因子
        
        # 创建添加按钮
        self.add_button = QPushButton("添加")
        self.update_button_style()
        self.add_button.clicked.connect(self.add_task)
        input_layout.addWidget(self.add_button)
        
        main_layout.addLayout(input_layout)
        
        # 创建状态栏
        self.statusBar().showMessage("准备就绪")
        
        # 创建菜单栏
        self.create_menu()
        
        # 加载任务数据
        self.tasks_file = "tasks.json"
        self.load_tasks()
        
        # 设置自动保存定时器
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.timeout.connect(self.save_tasks)
        self.auto_save_timer.start(30000)  # 每30秒自动保存一次
    
    def detect_dark_mode(self):
        # 检测系统是否使用深色模式
        # 这是一个简单的实现，实际上可能需要根据不同平台进行调整
        app = QApplication.instance()
        palette = app.palette()
        bg_color = palette.color(QPalette.Window)
        brightness = (bg_color.red() * 299 + bg_color.green() * 587 + bg_color.blue() * 114) / 1000
        return brightness < 128  # 如果亮度小于128，认为是深色模式
    
    def setup_style(self):
        # 根据深色/浅色模式设置不同的样式
        if self.is_dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                }
                QWidget {
                    font-family: 'NotoSansSC';
                }
                QLabel {
                    color: #e0e0e0;
                    font-family: 'NotoSansSC';
                }
                QPushButton {
                    font-family: 'NotoSansSC';
                    color: #e0e0e0;
                }
                QLineEdit {
                    font-family: 'NotoSansSC';
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: none;
                }
                QListWidget {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: none;
                }
                QMenuBar {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    font-family: 'NotoSansSC';
                }
                QMenuBar::item:selected {
                    background-color: #3d3d3d;
                }
                QMenu {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: none;
                    font-family: 'NotoSansSC';
                }
                QMenu::item:selected {
                    background-color: #3d3d3d;
                }
                QStatusBar {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    font-family: 'NotoSansSC';
                }
                QFrame {
                    background-color: #444444;
                }
                QCheckBox {
                    color: #e0e0e0;
                    font-family: 'NotoSansSC';
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f9f9f9;
                }
                QWidget {
                    font-family: 'NotoSansSC';
                }
                QLabel {
                    color: #333333;
                    font-family: 'NotoSansSC';
                }
                QPushButton {
                    font-family: 'NotoSansSC';
                    color: #333333;
                }
                QLineEdit {
                    font-family: 'NotoSansSC';
                    background-color: #f9f9f9;
                    color: #333333;
                    border: none;
                }
                QListWidget {
                    background-color: #f9f9f9;
                    color: #333333;
                    border: none;
                }
                QMenuBar {
                    background-color: #f9f9f9;
                    color: #333333;
                    font-family: 'NotoSansSC';
                }
                QMenu {
                    background-color: #f9f9f9;
                    color: #333333;
                    font-family: 'NotoSansSC';
                }
                QStatusBar {
                    color: #333333;
                    font-family: 'NotoSansSC';
                }
                QCheckBox {
                    color: #333333;
                    font-family: 'NotoSansSC';
                }
            """)
    
    def update_list_style(self, remove_borders=False):
        if self.is_dark_mode:
            if remove_borders:
                self.todo_list.setStyleSheet("""
                    QListWidget {
                        background-color: #2d2d2d;
                        padding: 5px;
                        border: none;
                    }
                    QListWidget::item {
                        padding: 5px;
                    }
                    QListWidget::item:selected {
                        background-color: #3d3d3d;
                        color: #2196f3;
                    }
                """)
            else:
                self.todo_list.setStyleSheet("""
                    QListWidget {
                        background-color: #2d2d2d;
                        padding: 5px;
                    }
                    QListWidget::item {
                        border-bottom: 1px solid #444444;
                        padding: 5px;
                    }
                    QListWidget::item:selected {
                        background-color: #3d3d3d;
                        color: #2196f3;
                    }
                """)
        else:
            if remove_borders:
                self.todo_list.setStyleSheet("""
                    QListWidget {
                        background-color: #f9f9f9;
                        padding: 5px;
                        border: none;
                    }
                    QListWidget::item {
                        padding: 5px;
                    }
                    QListWidget::item:selected {
                        background-color: #e3f2fd;
                        color: #1976d2;
                    }
                """)
            else:
                self.todo_list.setStyleSheet("""
                    QListWidget {
                        background-color: #f5f5f5;
                        padding: 5px;
                    }
                    QListWidget::item {
                        border-bottom: 1px solid #e0e0e0;
                        padding: 5px;
                    }
                    QListWidget::item:selected {
                        background-color: #e3f2fd;
                        color: #1976d2;
                    }
                """)
    
    def update_input_style(self):
        if self.is_dark_mode:
            self.task_input.setStyleSheet("""
                QLineEdit {
                    border: none;
                    border-bottom: 1px solid #444444;
                    padding: 8px;
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    font-family: 'NotoSansSC';
                }
                QLineEdit:focus {
                    border-bottom: 1px solid #2196f3;
                }
            """)
        else:
            self.task_input.setStyleSheet("""
                QLineEdit {
                    border: none;
                    border-bottom: 1px solid #ccc;
                    padding: 8px;
                    background-color: #f9f9f9;
                    color: #333333;
                    font-family: 'NotoSansSC';
                }
                QLineEdit:focus {
                    border-bottom: 1px solid #1976d2;
                }
            """)
    
    def update_button_style(self):
        if self.is_dark_mode:
            self.add_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    font-family: 'NotoSansSC';
                }
                QPushButton:hover {
                    background-color: #1976d2;
                }
                QPushButton:pressed {
                    background-color: #0d47a1;
                }
            """)
        else:
            self.add_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    font-family: 'NotoSansSC';
                }
                QPushButton:hover {
                    background-color: #1976d2;
                }
                QPushButton:pressed {
                    background-color: #0d47a1;
                }
            """)
    
    def create_menu(self):
        # 创建菜单栏
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        # 保存操作
        save_action = QAction("保存", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_tasks)
        file_menu.addAction(save_action)
        
        # 清空操作
        clear_action = QAction("清空所有任务", self)
        clear_action.triggered.connect(self.clear_tasks)
        file_menu.addAction(clear_action)
        
        file_menu.addSeparator()
        
        # 退出操作
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 视图菜单
        view_menu = menubar.addMenu("视图")
        
        # 显示已完成任务
        self.show_completed_action = QAction("显示已完成任务", self)
        self.show_completed_action.setCheckable(True)
        self.show_completed_action.setChecked(True)
        self.show_completed_action.triggered.connect(self.filter_tasks)
        view_menu.addAction(self.show_completed_action)
        
        # 切换深色/浅色模式
        self.toggle_theme_action = QAction("切换深色/浅色模式", self)
        self.toggle_theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(self.toggle_theme_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        # 关于操作
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def toggle_theme(self):
        # 切换深色/浅色模式
        self.is_dark_mode = not self.is_dark_mode
        self.setup_style()
        self.update_list_style(remove_borders=True)
        self.update_input_style()
        self.update_button_style()
        
        # 更新所有任务项的样式
        for i in range(self.todo_list.count()):
            item = self.todo_list.item(i)
            widget = self.todo_list.itemWidget(item)
            if hasattr(widget, 'set_dark_mode'):
                widget.set_dark_mode(self.is_dark_mode)
        
        theme_name = "深色" if self.is_dark_mode else "浅色"
        self.statusBar().showMessage(f"已切换到{theme_name}模式", 3000)
    
    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            self.add_task_to_list(task_text)
            self.task_input.clear()
            self.save_tasks()
            self.statusBar().showMessage(f"已添加任务: {task_text}", 3000)
    
    def add_task_to_list(self, text, completed=False):
        # 创建列表项
        item = QListWidgetItem()
        self.todo_list.addItem(item)
        
        # 创建自定义部件
        widget = TodoListItem(text, completed=completed, is_dark_mode=self.is_dark_mode)
        widget.parent_item = item
        widget.deleted.connect(self.remove_task)
        widget.completed.connect(self.task_completed)
        
        # 设置项目大小
        item.setSizeHint(widget.sizeHint())
        
        # 设置自定义部件
        self.todo_list.setItemWidget(item, widget)
    
    def remove_task(self, item):
        row = self.todo_list.row(item)
        self.todo_list.takeItem(row)
        self.save_tasks()
        self.statusBar().showMessage("任务已删除", 3000)
    
    def task_completed(self, item, is_completed):
        self.save_tasks()
        status = "已完成" if is_completed else "未完成"
        self.statusBar().showMessage(f"任务标记为{status}", 3000)
    
    def show_context_menu(self, position):
        item = self.todo_list.itemAt(position)
        if item:
            context_menu = QMenu(self)
            
            # 删除操作
            delete_action = QAction("删除", self)
            delete_action.triggered.connect(lambda: self.remove_task(item))
            context_menu.addAction(delete_action)
            
            # 显示菜单
            context_menu.exec_(self.todo_list.mapToGlobal(position))
    
    def filter_tasks(self):
        show_completed = self.show_completed_action.isChecked()
        for i in range(self.todo_list.count()):
            item = self.todo_list.item(i)
            widget = self.todo_list.itemWidget(item)
            if widget.completed:
                item.setHidden(not show_completed)
    
    def clear_tasks(self):
        reply = QMessageBox.question(
            self, "确认清空", "确定要清空所有任务吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.todo_list.clear()
            self.save_tasks()
            self.statusBar().showMessage("所有任务已清空", 3000)
    
    def show_about(self):
        QMessageBox.about(
            self,
            "关于待办事项应用",
            "SDCOM的待办项目 v1.0\n\n"
            "一个简单而美观的跨平台待办事项应用\n"
            "使用 PySide6 (Qt for Python) 构建\n\n"
            "支持 Windows, macOS 和 Linux\n"
            "支持深色/浅色模式自动切换"
        )
    
    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, "r", encoding="utf-8") as f:
                    tasks = json.load(f)
                    for task in tasks:
                        self.add_task_to_list(task["text"], task["completed"])
                self.statusBar().showMessage("任务已加载", 3000)
            except Exception as e:
                QMessageBox.warning(self, "加载错误", f"无法加载任务: {str(e)}")
    
    def save_tasks(self):
        tasks = []
        for i in range(self.todo_list.count()):
            item = self.todo_list.item(i)
            widget = self.todo_list.itemWidget(item)
            tasks.append({
                "text": widget.text,
                "completed": widget.completed,
                "created_at": datetime.now().isoformat()
            })
        
        try:
            with open(self.tasks_file, "w", encoding="utf-8") as f:
                json.dump(tasks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "保存错误", f"无法保存任务: {str(e)}")
    
    def closeEvent(self, event):
        self.save_tasks()
        event.accept()

# 运行应用程序
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 加载字体
    font_path = source_path("res/NotoSansSC.ttf")
    if os.path.exists(font_path):
        # 使用 QFontDatabase 加载字体
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                # 设置应用程序默认字体
                default_font = QFont(font_families[0], 10)
                app.setFont(default_font)
                
                # 确保所有控件都使用这个字体
                QApplication.setFont(default_font)
    
    window = TodoApp()
    window.show()
    sys.exit(app.exec())