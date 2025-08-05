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
    QMessageBox, QMenu, QCheckBox, QStyle, QSplitter, QFrame,
    QComboBox, QDateEdit, QDialog, QFormLayout
)
from PySide6.QtCore import Qt, Signal, Slot, QSize, QTimer, QDate
from PySide6.QtGui import QIcon, QFont, QColor, QPalette, QAction, QFontDatabase

# 资源文件目录访问
def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 任务优先级颜色
PRIORITY_COLORS = {
    "低": "#28a745",  # 绿色
    "中": "#ffc107",  # 黄色
    "高": "#dc3545"   # 红色
}

# 任务编辑对话框
class TaskEditDialog(QDialog):
    def __init__(self, parent=None, task_text="", priority="中", due_date=None, is_dark_mode=False):
        super().__init__(parent)
        self.setWindowTitle("编辑任务")
        self.is_dark_mode = is_dark_mode
        
        # 设置对话框样式
        if is_dark_mode:
            self.setStyleSheet("""
                QDialog {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                }
                QLabel {
                    color: #e0e0e0;
                }
                QLineEdit {
                    background-color: #3d3d3d;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #1976d2;
                }
                QComboBox {
                    background-color: #3d3d3d;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                    padding: 5px;
                }
                QDateEdit {
                    background-color: #3d3d3d;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                    padding: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: #f9f9f9;
                    color: #333333;
                }
                QLineEdit {
                    background-color: white;
                    color: #333333;
                    border: 1px solid #cccccc;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #1976d2;
                }
                QComboBox {
                    background-color: white;
                    color: #333333;
                    border: 1px solid #cccccc;
                    padding: 5px;
                }
                QDateEdit {
                    background-color: white;
                    color: #333333;
                    border: 1px solid #cccccc;
                    padding: 5px;
                }
            """)
        
        # 创建表单布局
        layout = QFormLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 任务文本输入
        self.text_input = QLineEdit(task_text)
        layout.addRow("任务内容:", self.text_input)
        
        # 优先级选择
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["低", "中", "高"])
        self.priority_combo.setCurrentText(priority)
        layout.addRow("优先级:", self.priority_combo)
        
        # 截止日期选择
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        if due_date:
            self.date_edit.setDate(due_date)
        else:
            self.date_edit.setDate(QDate.currentDate().addDays(1))
        layout.addRow("截止日期:", self.date_edit)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 确认按钮
        self.ok_button = QPushButton("确认")
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)
        
        # 取消按钮
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addRow("", button_layout)
        
        # 设置对话框大小
        self.setMinimumWidth(300)
    
    def get_task_data(self):
        return {
            "text": self.text_input.text(),
            "priority": self.priority_combo.currentText(),
            "due_date": self.date_edit.date().toString("yyyy-MM-dd")
        }

# 自定义待办事项项目组件
class TodoListItem(QWidget):
    deleted = Signal(QListWidgetItem)
    task_completed = Signal(QListWidgetItem, bool)  # 重命名信号，避免与属性冲突
    edited = Signal(QListWidgetItem)
    
    def __init__(self, text, parent=None, completed=False, is_dark_mode=False, priority="中", due_date=None):
        super().__init__(parent)
        self.text = text
        self.is_completed = completed  # 重命名属性，避免与信号冲突
        self.is_dark_mode = is_dark_mode
        self.priority = priority
        self.due_date = due_date if due_date else ""
        
        # 创建布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # 创建完成复选框
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(completed)
        self.checkbox.stateChanged.connect(self.on_state_changed)
        layout.addWidget(self.checkbox)
        
        # 创建优先级标签
        self.priority_label = QLabel()
        self.priority_label.setFixedSize(16, 16)
        self.update_priority_label()
        layout.addWidget(self.priority_label)
        
        # 创建任务文本标签
        self.label = QLabel(text)
        font = QFont("NotoSansSC", 10)
        self.label.setFont(font)
        self.update_label_style()
        layout.addWidget(self.label, 1)  # 1 表示伸展因子
        
        # 创建截止日期标签
        if due_date:
            self.date_label = QLabel(f"截止: {due_date}")
            self.date_label.setStyleSheet("color: gray; font-size: 9pt;")
            layout.addWidget(self.date_label)
            
            # 检查是否接近截止日期
            self.check_due_date()
        
        # 创建编辑按钮
        self.edit_button = QPushButton()
        self.edit_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.edit_button.setFixedSize(24, 24)
        self.edit_button.setStyleSheet("QPushButton { border: none; }")
        self.edit_button.clicked.connect(self.on_edit_clicked)
        layout.addWidget(self.edit_button)
        
        # 创建删除按钮
        self.delete_button = QPushButton()
        self.delete_button.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.delete_button.setFixedSize(24, 24)
        self.delete_button.setStyleSheet("QPushButton { border: none; }")
        self.delete_button.clicked.connect(self.on_delete_clicked)
        layout.addWidget(self.delete_button)
        
        self.setLayout(layout)
    
    def update_priority_label(self):
        color = PRIORITY_COLORS.get(self.priority, "#ffc107")  # 默认为中优先级
        self.priority_label.setStyleSheet(f"background-color: {color}; border-radius: 8px;")
        self.priority_label.setToolTip(f"{self.priority}优先级")
    
    def check_due_date(self):
        if not self.due_date:
            return
            
        try:
            due_date = QDate.fromString(self.due_date, "yyyy-MM-dd")
            days_left = QDate.currentDate().daysTo(due_date)
            
            if days_left < 0:
                # 已过期
                self.date_label.setStyleSheet("color: #dc3545; font-size: 9pt; font-weight: bold;")
                self.date_label.setText(f"已过期: {self.due_date}")
            elif days_left == 0:
                # 今天到期
                self.date_label.setStyleSheet("color: #dc3545; font-size: 9pt; font-weight: bold;")
                self.date_label.setText(f"今天到期")
            elif days_left <= 2:
                # 即将到期
                self.date_label.setStyleSheet("color: #ffc107; font-size: 9pt; font-weight: bold;")
                self.date_label.setText(f"即将到期: {self.due_date}")
            else:
                # 正常显示
                self.date_label.setStyleSheet("color: gray; font-size: 9pt;")
                self.date_label.setText(f"截止: {self.due_date}")
        except Exception:
            pass
    
    def update_label_style(self):
        base_style = "text-decoration: line-through; " if self.is_completed else ""
        
        if self.is_completed:
            if self.is_dark_mode:
                self.label.setStyleSheet(f"{base_style}color: #888888;")
            else:
                self.label.setStyleSheet(f"{base_style}color: gray;")
        else:
            if self.is_dark_mode:
                self.label.setStyleSheet(f"{base_style}color: #e0e0e0;")
            else:
                self.label.setStyleSheet(f"{base_style}color: #333333;")
    
    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.update_label_style()
        if hasattr(self, 'date_label'):
            self.check_due_date()
    
    def on_state_changed(self, state):
        self.is_completed = (state == Qt.CheckState.Checked.value)
        self.update_label_style()
        parent_item = self.parent_item if hasattr(self, 'parent_item') else None
        self.task_completed.emit(parent_item, self.is_completed)
    
    def on_delete_clicked(self):
        parent_item = self.parent_item if hasattr(self, 'parent_item') else None
        self.deleted.emit(parent_item)
        
    def on_edit_clicked(self):
        parent_item = self.parent_item if hasattr(self, 'parent_item') else None
        self.edited.emit(parent_item)

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
        
        # 新建任务操作
        new_task_action = QAction("新建任务", self)
        new_task_action.setShortcut("Ctrl+N")
        new_task_action.triggered.connect(self.show_new_task_dialog)
        file_menu.addAction(new_task_action)
        
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
        
        # 按优先级排序
        sort_priority_action = QAction("按优先级排序", self)
        sort_priority_action.triggered.connect(lambda: self.sort_tasks("priority"))
        view_menu.addAction(sort_priority_action)
        
        # 按截止日期排序
        sort_date_action = QAction("按截止日期排序", self)
        sort_date_action.triggered.connect(lambda: self.sort_tasks("due_date"))
        view_menu.addAction(sort_date_action)
        
        view_menu.addSeparator()
        
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
    
    def show_new_task_dialog(self):
        dialog = TaskEditDialog(self, is_dark_mode=self.is_dark_mode)
        if dialog.exec():
            task_data = dialog.get_task_data()
            self.add_task_to_list(
                task_data["text"], 
                completed=False,
                priority=task_data["priority"],
                due_date=task_data["due_date"]
            )
            self.save_tasks()
            self.statusBar().showMessage(f"已添加任务: {task_data['text']}", 3000)
    
    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            # 使用默认值创建任务
            self.add_task_to_list(
                task_text, 
                completed=False,
                priority="中",
                due_date=QDate.currentDate().addDays(1).toString("yyyy-MM-dd")
            )
            self.task_input.clear()
            self.save_tasks()
            self.statusBar().showMessage(f"已添加任务: {task_text}", 3000)
    
    def add_task_to_list(self, text, completed=False, priority="中", due_date=None):
        # 创建列表项
        item = QListWidgetItem()
        self.todo_list.addItem(item)
        
        # 创建自定义部件
        widget = TodoListItem(
            text, 
            completed=completed, 
            is_dark_mode=self.is_dark_mode,
            priority=priority,
            due_date=due_date
        )
        widget.parent_item = item
        widget.deleted.connect(self.remove_task)
        widget.task_completed.connect(self.task_completed)  # 使用重命名后的信号
        widget.edited.connect(self.edit_task)
        
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
    
    def edit_task(self, item):
        widget = self.todo_list.itemWidget(item)
        if widget:
            dialog = TaskEditDialog(
                self,
                task_text=widget.text,
                priority=widget.priority,
                due_date=QDate.fromString(widget.due_date, "yyyy-MM-dd") if widget.due_date else None,
                is_dark_mode=self.is_dark_mode
            )
            
            if dialog.exec():
                task_data = dialog.get_task_data()
                
                # 更新任务数据
                widget.text = task_data["text"]
                widget.priority = task_data["priority"]
                widget.due_date = task_data["due_date"]
                
                # 更新UI
                widget.label.setText(task_data["text"])
                widget.update_priority_label()
                
                # 更新或添加截止日期标签
                if hasattr(widget, 'date_label'):
                    widget.date_label.setText(f"截止: {task_data['due_date']}")
                    widget.check_due_date()
                else:
                    widget.date_label = QLabel(f"截止: {task_data['due_date']}")
                    widget.date_label.setStyleSheet("color: gray; font-size: 9pt;")
                    widget.layout().insertWidget(widget.layout().count() - 2, widget.date_label)
                    widget.check_due_date()
                
                self.save_tasks()
                self.statusBar().showMessage(f"任务已更新: {task_data['text']}", 3000)
    
    def show_context_menu(self, position):
        item = self.todo_list.itemAt(position)
        if item:
            context_menu = QMenu(self)
            
            # 编辑操作
            edit_action = QAction("编辑", self)
            edit_action.triggered.connect(lambda: self.edit_task(item))
            context_menu.addAction(edit_action)
            
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
            if widget.is_completed:  # 使用重命名后的属性
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
                        # 获取任务属性，如果不存在则使用默认值
                        text = task.get("text", "")
                        completed = task.get("completed", False)
                        priority = task.get("priority", "中")
                        due_date = task.get("due_date", "")
                        
                        self.add_task_to_list(text, completed, priority, due_date)
                self.statusBar().showMessage("任务已加载", 3000)
            except Exception as e:
                QMessageBox.warning(self, "加载错误", f"无法加载任务: {str(e)}")
    
    def sort_tasks(self, sort_by):
        # 收集所有任务
        tasks = []
        for i in range(self.todo_list.count()):
            item = self.todo_list.item(i)
            widget = self.todo_list.itemWidget(item)
            tasks.append({
                "item": item,
                "widget": widget,
                "text": widget.text,
                "completed": widget.is_completed,
                "priority": widget.priority,
                "due_date": widget.due_date if hasattr(widget, 'due_date') else ""
            })
        
        # 从列表中移除所有项目
        self.todo_list.clear()
        
        # 根据指定字段排序
        if sort_by == "priority":
            # 优先级排序: 高 > 中 > 低
            priority_order = {"高": 0, "中": 1, "低": 2}
            tasks.sort(key=lambda x: (x["completed"], priority_order.get(x["priority"], 1)))
        elif sort_by == "due_date":
            # 截止日期排序
            tasks.sort(key=lambda x: (x["completed"], x["due_date"] if x["due_date"] else "9999-99-99"))
        
        # 重新添加排序后的任务
        for task in tasks:
            self.add_task_to_list(
                task["text"],
                completed=task["completed"],
                priority=task["priority"],
                due_date=task["due_date"]
            )
        
        sort_type = "优先级" if sort_by == "priority" else "截止日期"
        self.statusBar().showMessage(f"已按{sort_type}排序", 3000)
    
    def save_tasks(self):
        tasks = []
        for i in range(self.todo_list.count()):
            item = self.todo_list.item(i)
            widget = self.todo_list.itemWidget(item)
            tasks.append({
                "text": widget.text,
                "completed": widget.is_completed,  # 使用重命名后的属性
                "priority": widget.priority,
                "due_date": widget.due_date,
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