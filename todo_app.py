#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
待办事项应用程序
使用 PySide6 (Qt for Python) 构建的现代化跨平台待办事项应用
支持 Windows, macOS 和 Linux
支持深色/浅色模式自动切换
彻底去除所有界面元素边框
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
    QComboBox, QDateEdit, QDialog, QFormLayout, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, Slot, QSize, QTimer, QDate
from PySide6.QtGui import QIcon, QFont, QColor, QPalette, QAction, QFontDatabase, QPainter

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
                    border: none;
                    background: transparent;
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
    task_completed = Signal(QListWidgetItem, bool)
    edited = Signal(QListWidgetItem)
    
    def __init__(self, text, parent=None, completed=False, is_dark_mode=False, priority="中", due_date=None):
        super().__init__(parent)
        self.text = text
        self.is_completed = completed
        self.is_dark_mode = is_dark_mode
        self.priority = priority
        self.due_date = due_date if due_date else ""
        
        # 创建布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
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
        # 使用应用程序的默认字体
        font = QApplication.font()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignVCenter)
        self.label.setFixedHeight(44)
        
        # 强制设置QFrame属性，彻底去除边框
        self.label.setFrameShape(QLabel.NoFrame)
        self.label.setFrameShadow(QLabel.Plain)
        self.label.setLineWidth(0)
        self.label.setMidLineWidth(0)
        
        # 阻断父样式继承和系统样式
        self.label.setAttribute(Qt.WA_StyledBackground, False)
        self.label.setAttribute(Qt.WA_NoSystemBackground, True)
        
        # 设置布局边距为0，防止被误认为边框
        self.label.setContentsMargins(0, 0, 0, 0)
        
        # 简化的无边框样式 - 避免过度复杂化，去除文字阴影
        self.label.setStyleSheet("border: none; background: transparent; padding: 12px 0px; text-shadow: none;")
        layout.addWidget(self.label, 1)
        
        # 创建截止日期标签
        if due_date:
            self.date_label = QLabel(f"截止: {due_date}")
            self.date_label.setStyleSheet("color: gray; font-size: 9pt; border: none; background: transparent;")
            layout.addWidget(self.date_label)
        
        # 创建按钮容器
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        
        # 创建编辑按钮
        self.edit_button = QPushButton()
        self.edit_button.setFixedSize(28, 28)
        self.edit_button.setIcon(QIcon.fromTheme("document-edit", 
                                               QApplication.style().standardIcon(QStyle.SP_FileDialogDetailedView)))
        self.edit_button.setIconSize(QSize(18, 18))
        self.edit_button.setToolTip("编辑")
        button_layout.addWidget(self.edit_button)
        
        # 创建删除按钮
        self.delete_button = QPushButton()
        self.delete_button.setFixedSize(28, 28)
        self.delete_button.setIcon(QIcon.fromTheme("edit-delete", 
                                                 QApplication.style().standardIcon(QStyle.SP_TrashIcon)))
        self.delete_button.setIconSize(QSize(18, 18))
        self.delete_button.setToolTip("删除")
        button_layout.addWidget(self.delete_button)
        
        layout.addWidget(button_container, 0, Qt.AlignTop)
        
        # 设置按钮样式
        if self.is_dark_mode:
            self.update_button_dark_mode()
        else:
            self.update_button_light_mode()
            
        # 连接按钮信号
        self.edit_button.clicked.connect(self.on_edit_clicked)
        self.delete_button.clicked.connect(self.on_delete_clicked)
        
        # 更新标签样式
        self.update_label_style()
        
        # 检查截止日期
        if due_date:
            self.check_due_date()
            
        self.setLayout(layout)
    
    def update_priority_label(self):
        color = PRIORITY_COLORS.get(self.priority, "#ffc107")
        self.priority_label.setStyleSheet(f"background-color: {color}; border-radius: 8px;")
        self.priority_label.setToolTip(f"{self.priority}优先级")
    
    def check_due_date(self):
        if not self.due_date:
            return
            
        try:
            due_date = QDate.fromString(self.due_date, "yyyy-MM-dd")
            days_left = QDate.currentDate().daysTo(due_date)
            
            if days_left < 0:
                self.date_label.setStyleSheet("color: #dc3545; font-size: 9pt; font-weight: bold;")
                self.date_label.setText(f"已过期: {self.due_date}")
            elif days_left == 0:
                self.date_label.setStyleSheet("color: #dc3545; font-size: 9pt; font-weight: bold;")
                self.date_label.setText(f"今天到期")
            elif days_left <= 2:
                self.date_label.setStyleSheet("color: #ffc107; font-size: 9pt; font-weight: bold;")
                self.date_label.setText(f"即将到期: {self.due_date}")
            else:
                self.date_label.setStyleSheet("color: gray; font-size: 9pt;")
                self.date_label.setText(f"截止: {self.due_date}")
        except Exception:
            pass
    

    def update_label_style(self):
        """简化的标签样式更新 - 专注于核心功能"""
        
        # 基础样式：删除线和颜色
        base_style = "text-decoration: line-through; " if self.is_completed else ""
        
        # 简洁的无边框样式
        if self.is_completed:
            if self.is_dark_mode:
                self.label.setStyleSheet(f"border: none; background: transparent; padding: 12px 0px; {base_style}color: #888888;")
            else:
                self.label.setStyleSheet(f"border: none; background: transparent; padding: 12px 0px; {base_style}color: gray;")
        else:
            if self.is_dark_mode:
                self.label.setStyleSheet(f"border: none; background: transparent; padding: 12px 0px; {base_style}color: #e0e0e0;")
            else:
                self.label.setStyleSheet(f"border: none; background: transparent; padding: 12px 0px; {base_style}color: #333333;")
    
    def debug_border_detection(self):
        """调试方法：临时设置背景色来检测边框是否存在"""
        print("=== 边框调试信息 ===")
        print(f"Frame Shape: {self.label.frameShape()}")
        print(f"Frame Shadow: {self.label.frameShadow()}")
        print(f"Line Width: {self.label.lineWidth()}")
        print(f"Mid Line Width: {self.label.midLineWidth()}")
        print(f"Contents Margins: {self.label.contentsMargins()}")
        print(f"WA_StyledBackground: {self.label.testAttribute(Qt.WA_StyledBackground)}")
        print(f"WA_NoSystemBackground: {self.label.testAttribute(Qt.WA_NoSystemBackground)}")
        
        # 临时设置红色背景来可视化边框
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 0, 0, 0.3) !important;
                border: 2px solid blue !important;
                margin: 0px;
                padding: 12px 0px;
            }
        """)
        print("已设置调试样式，请检查界面中的红色背景和蓝色边框")
    
    def update_button_dark_mode(self):
        if hasattr(self, 'edit_button') and hasattr(self, 'delete_button'):
            button_style = """
                QPushButton {
                    border: 1px solid #555;
                    border-radius: 3px;
                    padding: 2px;
                    background-color: #444;
                    color: #e0e0e0;
                }
                QPushButton:hover {
                    background-color: #555;
                }
            """
            self.edit_button.setStyleSheet(button_style)
            self.delete_button.setStyleSheet(button_style)
    
    def update_button_light_mode(self):
        if hasattr(self, 'edit_button') and hasattr(self, 'delete_button'):
            button_style = """
                QPushButton {
                    border: 1px solid #aaa;
                    border-radius: 3px;
                    padding: 2px;
                    background-color: #f0f0f0;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """
            self.edit_button.setStyleSheet(button_style)
            self.delete_button.setStyleSheet(button_style)
    
    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.update_label_style()
        if hasattr(self, 'date_label'):
            self.check_due_date()
        
        if is_dark:
            self.update_button_dark_mode()
        else:
            self.update_button_light_mode()
    
    def on_state_changed(self, state):
        self.is_completed = (state == Qt.CheckState.Checked.value)
        self.update_label_style()
        parent_item = self.parent_item if hasattr(self, 'parent_item') else None
        self.task_completed.emit(parent_item, self.is_completed)
    
    def on_delete_clicked(self):
        parent_window = None
        widget = self
        while widget:
            if isinstance(widget, QMainWindow):
                parent_window = widget
                break
            widget = widget.parent()
        
        reply = QMessageBox.question(
            parent_window or self,
            "确认删除",
            f"确定要删除任务 '{self.text}' 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
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
        self.setWindowTitle("SDCOM 待办事项管理器")
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
        # 使用应用程序的默认字体
        title_font = QApplication.font()
        title_font.setPointSize(18)
        title_font.setBold(True)
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
        
        # 彻底去除QListWidget的所有边框、焦点框和装饰性元素
        self.setup_borderless_listwidget()
        
        self.update_list_style(remove_borders=True)
        self.todo_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.todo_list.customContextMenuRequested.connect(self.show_context_menu)
        main_layout.addWidget(self.todo_list, 1)
        
        # 创建输入区域
        input_layout = QHBoxLayout()
        
        # 创建任务输入框
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("输入新任务...")
        self.update_input_style()
        self.task_input.returnPressed.connect(self.show_quick_add_dialog)
        input_layout.addWidget(self.task_input, 1)
        
        # 创建添加按钮
        self.add_button = QPushButton("添加")
        self.update_button_style()
        self.add_button.clicked.connect(self.show_quick_add_dialog)
        input_layout.addWidget(self.add_button)
        
        main_layout.addLayout(input_layout)
        
        # 创建状态栏
        self.statusBar().showMessage("🚀 系统已就绪，开始管理您的待办事项")
        
        # 创建菜单栏
        self.create_menu()
        
        # 加载任务数据
        self.tasks_file = "tasks.json"
        self.load_tasks()
        
        # 设置自动保存定时器
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.timeout.connect(self.save_tasks)
        self.auto_save_timer.start(30000)
    
    def setup_borderless_listwidget(self):
        """彻底去除QListWidget的所有边框、焦点框和装饰性元素"""
        
        # 1. 设置QFrame属性，去除控件边框
        self.todo_list.setFrameShape(QListWidget.NoFrame)
        self.todo_list.setFrameShadow(QListWidget.Plain)
        self.todo_list.setLineWidth(0)
        self.todo_list.setMidLineWidth(0)
        
        # 2. 焦点策略调整 - 保留键盘导航但去除焦点框
        self.todo_list.setFocusPolicy(Qt.StrongFocus)
        
        # 3. 阻断系统样式继承
        self.todo_list.setAttribute(Qt.WA_StyledBackground, False)
        self.todo_list.setAttribute(Qt.WA_NoSystemBackground, True)
        
        # 4. 设置选择行为，保持功能性
        self.todo_list.setSelectionBehavior(QListWidget.SelectRows)
        self.todo_list.setSelectionMode(QListWidget.SingleSelection)
        
        # 5. 终极样式表 - 彻底去除所有边框和焦点框
        borderless_style = """
            QListWidget {
                border: none !important;
                border-top: none !important;
                border-bottom: none !important;
                border-left: none !important;
                border-right: none !important;
                outline: none !important;
                outline-width: 0px !important;
                outline-style: none !important;
                selection-background-color: transparent;
                show-decoration-selected: 0;
                alternate-background-color: transparent;
            }
            QListWidget::item {
                border: none !important;
                border-top: none !important;
                border-bottom: none !important;
                border-left: none !important;
                border-right: none !important;
                outline: none !important;
                outline-width: 0px !important;
                outline-style: none !important;
                padding: 0px;
                margin: 0px;
            }
            QListWidget::item:selected {
                border: none !important;
                outline: none !important;
                background: rgba(33, 150, 243, 0.2) !important;
            }
            QListWidget::item:hover {
                border: none !important;
                outline: none !important;
            }
            QListWidget::item:focus {
                border: none !important;
                outline: none !important;
            }
            QScrollBar:vertical {
                border: none !important;
                background: transparent;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: rgba(128, 128, 128, 0.3);
                border-radius: 6px;
                border: none !important;
            }
        """
        
        self.todo_list.setStyleSheet(borderless_style)
        
        # 6. 调试信息输出
        print(f"当前样式引擎: {QApplication.style().objectName()}")
        print("QListWidget无边框设置完成")
    
    def debug_listwidget_borders(self):
        """调试方法：检测QListWidget边框状态"""
        print("=== QListWidget边框调试信息 ===")
        print(f"Frame Shape: {self.todo_list.frameShape()}")
        print(f"Frame Shadow: {self.todo_list.frameShadow()}")
        print(f"Line Width: {self.todo_list.lineWidth()}")
        print(f"Focus Policy: {self.todo_list.focusPolicy()}")
        print(f"Selection Behavior: {self.todo_list.selectionBehavior()}")
        
        # 临时设置红色边框进行可视化调试
        debug_style = """
            QListWidget {
                border: 2px solid red !important;
                background-color: rgba(255, 255, 0, 0.1) !important;
            }
            QListWidget::item {
                border: 1px solid blue !important;
                background-color: rgba(0, 255, 0, 0.1) !important;
            }
        """
        self.todo_list.setStyleSheet(debug_style)
        print("已设置调试样式，请检查界面中的红色和蓝色边框")

    def detect_dark_mode(self):
        app = QApplication.instance()
        palette = app.palette()
        bg_color = palette.color(QPalette.Window)
        brightness = (bg_color.red() * 299 + bg_color.green() * 587 + bg_color.blue() * 114) / 1000
        return brightness < 128
    
    def setup_style(self):
        # 全局边框重置 - 彻底去除所有边框
        global_border_reset = """
            * {
                border: none !important;
                border-top: none !important;
                border-bottom: none !important;
                border-left: none !important;
                border-right: none !important;
                outline: none !important;
            }
        """
        
        if self.is_dark_mode:
            self.setStyleSheet(global_border_reset + """
                QMainWindow {
                    background-color: #1e1e1e;
                    border: none !important;
                }
                QLabel {
                    color: #e0e0e0;
                    border: none !important;
                    background: transparent;
                }
                QLabel:hover {
                    border: none !important;
                }
                QPushButton {
                    color: #e0e0e0;
                    border: none !important;
                }
                QLineEdit {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: none !important;
                }
                QLineEdit:focus {
                    border: 1px solid #2196f3 !important;
                }
                QListWidget {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: none !important;
                    outline: none !important;
                }
                QListWidget::item {
                    border: none !important;
                    border-top: none !important;
                    border-bottom: none !important;
                    outline: none !important;
                }
                QListWidget::item:selected {
                    border: none !important;
                    outline: none !important;
                }
                QListWidget::item:hover {
                    border: none !important;
                    outline: none !important;
                }
                QMenuBar {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: none !important;
                }
                QMenuBar::item {
                    background: transparent;
                    border: none !important;
                    padding: 4px 8px;
                }
                QMenuBar::item:selected {
                    background-color: #3d3d3d;
                    border: none !important;
                }
                QMenu {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: none !important;
                }
                QMenu::item {
                    background: transparent;
                    border: none !important;
                    padding: 4px 16px;
                }
                QMenu::item:selected {
                    background-color: #3d3d3d;
                    border: none !important;
                }
                QStatusBar {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: none !important;
                }
                QFrame {
                    background-color: #444444;
                    border: none !important;
                }
                QCheckBox {
                    color: #e0e0e0;
                    border: none !important;
                }
                QWidget {
                    border: none !important;
                }
            """)
        else:
            self.setStyleSheet(global_border_reset + """
                QMainWindow {
                    background-color: #f9f9f9;
                    border: none !important;
                }
                QLabel {
                    color: #333333;
                    border: none !important;
                    background: transparent;
                }
                QLabel:hover {
                    border: none !important;
                }
                QPushButton {
                    color: #333333;
                    border: none !important;
                }
                QLineEdit {
                    background-color: #f9f9f9;
                    color: #333333;
                    border: none !important;
                }
                QLineEdit:focus {
                    border: 1px solid #1976d2 !important;
                }
                QListWidget {
                    background-color: #f9f9f9;
                    color: #333333;
                    border: none !important;
                    outline: none !important;
                }
                QListWidget::item {
                    border: none !important;
                    border-top: none !important;
                    border-bottom: none !important;
                    outline: none !important;
                }
                QListWidget::item:selected {
                    border: none !important;
                    outline: none !important;
                }
                QListWidget::item:hover {
                    border: none !important;
                    outline: none !important;
                }
                QMenuBar {
                    background-color: #f9f9f9;
                    color: #333333;
                    border: none !important;
                }
                QMenuBar::item {
                    background: transparent;
                    border: none !important;
                    padding: 4px 8px;
                }
                QMenuBar::item:selected {
                    background-color: #e0e0e0;
                    border: none !important;
                }
                QMenu {
                    background-color: #f9f9f9;
                    color: #333333;
                    border: none !important;
                }
                QMenu::item {
                    background: transparent;
                    border: none !important;
                    padding: 4px 16px;
                }
                QMenu::item:selected {
                    background-color: #e0e0e0;
                    border: none !important;
                }
                QStatusBar {
                    color: #333333;
                    border: none !important;
                    background: transparent;
                }
                QCheckBox {
                    color: #333333;
                    border: none !important;
                    background: transparent;
                }
                QWidget {
                    border: none !important;
                }
            """)
    
    def update_list_style(self, remove_borders=False):
        # 彻底的边框重置样式
        border_reset = """
            border: none !important;
            border-top: none !important;
            border-bottom: none !important;
            border-left: none !important;
            border-right: none !important;
            outline: none !important;
        """
        
        if self.is_dark_mode:
            if remove_borders:
                self.todo_list.setStyleSheet(f"""
                    QListWidget {{
                        background-color: #2d2d2d;
                        padding: 5px;
                        {border_reset}
                    }}
                    QListWidget::item {{
                        padding: 5px;
                        {border_reset}
                    }}
                    QListWidget::item:selected {{
                        background-color: #3d3d3d;
                        color: #2196f3;
                        {border_reset}
                    }}
                    QListWidget::item:hover {{
                        {border_reset}
                    }}
                    QListWidget::item:focus {{
                        {border_reset}
                    }}
                """)
            else:
                self.todo_list.setStyleSheet(f"""
                    QListWidget {{
                        background-color: #2d2d2d;
                        padding: 5px;
                        {border_reset}
                    }}
                    QListWidget::item {{
                        border-bottom: 1px solid #444444;
                        padding: 5px;
                        border-top: none !important;
                        border-left: none !important;
                        border-right: none !important;
                        outline: none !important;
                    }}
                    QListWidget::item:selected {{
                        background-color: #3d3d3d;
                        color: #2196f3;
                        border-top: none !important;
                        border-left: none !important;
                        border-right: none !important;
                        outline: none !important;
                    }}
                    QListWidget::item:hover {{
                        border-top: none !important;
                        border-left: none !important;
                        border-right: none !important;
                        outline: none !important;
                    }}
                """)
        else:
            if remove_borders:
                self.todo_list.setStyleSheet(f"""
                    QListWidget {{
                        background-color: #f9f9f9;
                        padding: 5px;
                        {border_reset}
                    }}
                    QListWidget::item {{
                        padding: 5px;
                        {border_reset}
                    }}
                    QListWidget::item:selected {{
                        background-color: #e3f2fd;
                        color: #1976d2;
                        {border_reset}
                    }}
                    QListWidget::item:hover {{
                        {border_reset}
                    }}
                    QListWidget::item:focus {{
                        {border_reset}
                    }}
                """)
            else:
                self.todo_list.setStyleSheet(f"""
                    QListWidget {{
                        background-color: #f5f5f5;
                        padding: 5px;
                        {border_reset}
                    }}
                    QListWidget::item {{
                        border-bottom: 1px solid #e0e0e0;
                        padding: 5px;
                        border-top: none !important;
                        border-left: none !important;
                        border-right: none !important;
                        outline: none !important;
                    }}
                    QListWidget::item:selected {{
                        background-color: #e3f2fd;
                        color: #1976d2;
                        border-top: none !important;
                        border-left: none !important;
                        border-right: none !important;
                        outline: none !important;
                    }}
                    QListWidget::item:hover {{
                        border-top: none !important;
                        border-left: none !important;
                        border-right: none !important;
                        outline: none !important;
                    }}
                """)
    
    def update_input_style(self):
        # 彻底的边框重置，包括所有状态
        border_reset = """
            border: none !important;
            border-top: none !important;
            border-bottom: none !important;
            border-left: none !important;
            border-right: none !important;
            outline: none !important;
        """
        
        if self.is_dark_mode:
            self.task_input.setStyleSheet(f"""
                QLineEdit {{
                    {border_reset}
                    border-radius: 4px;
                    padding: 8px;
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                }}
                QLineEdit:focus {{
                    border: 1px solid #2196f3 !important;
                    border-radius: 4px;
                }}
                QLineEdit:hover {{
                    {border_reset}
                }}
            """)
        else:
            self.task_input.setStyleSheet(f"""
                QLineEdit {{
                    {border_reset}
                    border-radius: 4px;
                    padding: 8px;
                    background-color: white;
                    color: #333333;
                }}
                QLineEdit:focus {{
                    border: 1px solid #1976d2 !important;
                    border-radius: 4px;
                }}
                QLineEdit:hover {{
                    {border_reset}
                }}
            """)
    
    def update_button_style(self):
        button_style = """
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """
        self.add_button.setStyleSheet(button_style)
    
    def create_menu(self):
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("📁 文件")
        
        new_task_action = QAction("📝 新建任务", self)
        new_task_action.setShortcut("Ctrl+N")
        new_task_action.triggered.connect(self.show_new_task_dialog)
        file_menu.addAction(new_task_action)
        
        save_action = QAction("💾 保存任务", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_tasks)
        file_menu.addAction(save_action)
        
        clear_action = QAction("🗑️ 清空所有任务", self)
        clear_action.triggered.connect(self.clear_tasks)
        file_menu.addAction(clear_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("🚪 退出程序", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 视图菜单
        view_menu = menubar.addMenu("视图")
        
        self.show_completed_action = QAction("显示已完成任务", self)
        self.show_completed_action.setCheckable(True)
        self.show_completed_action.setChecked(True)
        self.show_completed_action.triggered.connect(self.filter_tasks)
        view_menu.addAction(self.show_completed_action)
        
        sort_priority_action = QAction("按优先级排序", self)
        sort_priority_action.triggered.connect(lambda: self.sort_tasks("priority"))
        view_menu.addAction(sort_priority_action)
        
        sort_date_action = QAction("按截止日期排序", self)
        sort_date_action.triggered.connect(lambda: self.sort_tasks("due_date"))
        view_menu.addAction(sort_date_action)
        
        view_menu.addSeparator()
        
        self.toggle_theme_action = QAction("切换深色/浅色模式", self)
        self.toggle_theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(self.toggle_theme_action)
        
        # 调试菜单
        debug_menu = menubar.addMenu("调试")
        
        debug_borders_action = QAction("检测边框状态", self)
        debug_borders_action.triggered.connect(self.debug_listwidget_borders)
        debug_menu.addAction(debug_borders_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.setup_style()
        self.setup_borderless_listwidget()  # 重新设置无边框样式
        self.update_list_style(remove_borders=True)
        self.update_input_style()
        self.update_button_style()
        
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
    
    def show_quick_add_dialog(self):
        task_text = self.task_input.text().strip()
        if not task_text:
            QMessageBox.warning(self, "提示", "请输入任务内容")
            return
            
        dialog = TaskEditDialog(
            self,
            task_text=task_text,
            priority="中",
            due_date=QDate.currentDate().addDays(1),
            is_dark_mode=self.is_dark_mode
        )
        
        if dialog.exec():
            task_data = dialog.get_task_data()
            self.add_task_to_list(
                task_data["text"], 
                completed=False,
                priority=task_data["priority"],
                due_date=task_data["due_date"]
            )
            self.task_input.clear()
            self.save_tasks()
            self.statusBar().showMessage(f"已添加任务: {task_data['text']}", 3000)
    
    def add_task_to_list(self, text, completed=False, priority="中", due_date=None):
        item = QListWidgetItem()
        self.todo_list.addItem(item)
        
        widget = TodoListItem(
            text, 
            completed=completed, 
            is_dark_mode=self.is_dark_mode,
            priority=priority,
            due_date=due_date
        )
        widget.parent_item = item
        widget.deleted.connect(self.remove_task)
        widget.task_completed.connect(self.task_completed)
        widget.edited.connect(self.edit_task)
        
        item.setSizeHint(widget.sizeHint())
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
                
                widget.text = task_data["text"]
                widget.priority = task_data["priority"]
                widget.due_date = task_data["due_date"]
                
                widget.label.setText(task_data["text"])
                widget.update_priority_label()
                
                if hasattr(widget, 'date_label'):
                    widget.date_label.setText(f"截止: {task_data['due_date']}")
                    widget.check_due_date()
                else:
                    widget.date_label = QLabel(f"截止: {task_data['due_date']}")
                    widget.date_label.setStyleSheet("color: gray; font-size: 9pt; border: none; background: transparent;")
                    widget.layout().insertWidget(widget.layout().count() - 2, widget.date_label)
                    widget.check_due_date()
                
                self.save_tasks()
                self.statusBar().showMessage(f"任务已更新: {task_data['text']}", 3000)
    
    def show_context_menu(self, position):
        item = self.todo_list.itemAt(position)
        if item:
            context_menu = QMenu(self)
            
            edit_action = QAction("编辑", self)
            edit_action.triggered.connect(lambda: self.edit_task(item))
            context_menu.addAction(edit_action)
            
            delete_action = QAction("删除", self)
            delete_action.triggered.connect(lambda: self.remove_task(item))
            context_menu.addAction(delete_action)
            
            context_menu.exec_(self.todo_list.mapToGlobal(position))
    
    def filter_tasks(self):
        show_completed = self.show_completed_action.isChecked()
        for i in range(self.todo_list.count()):
            item = self.todo_list.item(i)
            widget = self.todo_list.itemWidget(item)
            if widget.is_completed:
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
            "SDCOM的待办项目 v2.0\n\n"
            "一个简单而美观的跨平台待办事项应用\n"
            "使用 PySide6 (Qt for Python) 构建\n\n"
            "支持 Windows, macOS 和 Linux\n"
            "支持深色/浅色模式自动切换\n"
            "彻底去除所有界面元素边框"
        )
    
    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, "r", encoding="utf-8") as f:
                    tasks = json.load(f)
                    for task in tasks:
                        text = task.get("text", "")
                        completed = task.get("completed", False)
                        priority = task.get("priority", "中")
                        due_date = task.get("due_date", "")
                        
                        self.add_task_to_list(text, completed, priority, due_date)
                self.statusBar().showMessage("任务已加载", 3000)
            except Exception as e:
                QMessageBox.warning(self, "加载错误", f"无法加载任务: {str(e)}")
    
    def sort_tasks(self, sort_by):
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
        
        self.todo_list.clear()
        
        if sort_by == "priority":
            priority_order = {"高": 0, "中": 1, "低": 2}
            tasks.sort(key=lambda x: (x["completed"], priority_order.get(x["priority"], 1)))
        elif sort_by == "due_date":
            tasks.sort(key=lambda x: (x["completed"], x["due_date"] if x["due_date"] else "9999-99-99"))
        
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
                "completed": widget.is_completed,
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
    
    # 强制设置样式引擎，确保跨平台一致性
    app.setStyle("Fusion")
    
    # 全局边框重置 - 彻底去除系统默认边框
    app.setStyleSheet("""
        * {
            border: none !important;
            border-top: none !important;
            border-bottom: none !important;
            border-left: none !important;
            border-right: none !important;
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
    
    # 加载自定义字体
    font_path = source_path("res/NotoSansSC.ttf")
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                # 使用加载的中文字体
                default_font = QFont(font_families[0], 10)
                app.setFont(default_font)
                QApplication.setFont(default_font)
                print(f"已加载字体: {font_families[0]}")
            else:
                print("字体加载失败，使用默认字体")
                default_font = QFont("Arial", 10)
                app.setFont(default_font)
        else:
            print("字体文件加载失败，使用默认字体")
            default_font = QFont("Arial", 10)
            app.setFont(default_font)
    else:
        print(f"字体文件不存在: {font_path}，使用默认字体")
        default_font = QFont("Arial", 10)
        app.setFont(default_font)
    
    window = TodoApp()
    window.show()
    sys.exit(app.exec())
