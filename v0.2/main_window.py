"""
主窗口模块
包含应用程序的主窗口类和相关功能
"""

import os
import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QPushButton, QListWidget, QListWidgetItem, QLabel, QMessageBox, 
    QMenu, QFrame, QApplication
)
from PySide6.QtCore import Qt, QTimer, QDate
from PySide6.QtGui import QIcon, QFont, QAction, QPalette

from config import *
from text_config import TextConfig
from models import Task
from database import TaskDatabase
from ui_components import TaskEditDialog, TodoListItem

class TodoMainWindow(QMainWindow):
    """待办事项主窗口"""
    
    def __init__(self):
        super().__init__()
        self.db = TaskDatabase()
        self.is_dark_mode = self.detect_dark_mode()
        self.setup_ui()
        self.setup_style()
        self.setup_menu()
        self.load_tasks()
        self.setup_auto_save()
    
    def setup_ui(self):
        """设置UI界面"""
        # 设置窗口属性
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(PADDING * 2, PADDING * 2, PADDING * 2, PADDING * 2)
        main_layout.setSpacing(15)
        
        # 创建标题标签
        title_label = QLabel(TextConfig.MAIN_TITLE)
        title_font = QFont()
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
        self.setup_list_widget()
        main_layout.addWidget(self.todo_list, 1)
        
        # 创建输入区域
        input_layout = QHBoxLayout()
        
        # 任务输入框
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText(TextConfig.INPUT_PLACEHOLDER)
        self.task_input.setFixedHeight(ENTRY_HEIGHT + 10)  # 增加高度
        self.task_input.setMinimumWidth(400)  # 设置最小宽度
        self.task_input.returnPressed.connect(self.show_quick_add_dialog)
        input_layout.addWidget(self.task_input, 1)
        
        # 添加按钮
        self.add_button = QPushButton(TextConfig.ADD_BUTTON)
        self.add_button.setFixedHeight(BUTTON_HEIGHT)
        self.add_button.clicked.connect(self.show_quick_add_dialog)
        input_layout.addWidget(self.add_button)
        
        main_layout.addLayout(input_layout)
        
        # 创建状态栏
        self.statusBar().showMessage(TextConfig.STATUS_READY)
    
    def setup_list_widget(self):
        """设置列表控件"""
        self.todo_list.setFrameShape(QListWidget.NoFrame)
        self.todo_list.setFrameShadow(QListWidget.Plain)
        self.todo_list.setLineWidth(0)
        self.todo_list.setMidLineWidth(0)
        self.todo_list.setFocusPolicy(Qt.StrongFocus)
        self.todo_list.setAttribute(Qt.WA_StyledBackground, False)
        self.todo_list.setAttribute(Qt.WA_NoSystemBackground, True)
        self.todo_list.setSelectionBehavior(QListWidget.SelectRows)
        self.todo_list.setSelectionMode(QListWidget.SingleSelection)
        self.todo_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.todo_list.customContextMenuRequested.connect(self.show_context_menu)
    
    def setup_style(self):
        """设置样式"""
        # 全局边框重置
        global_border_reset = """
            * {
                border: none !important;
                outline: none !important;
            }
        """
        
        if self.is_dark_mode:
            self.setStyleSheet(global_border_reset + """
                QMainWindow {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                }
                QLabel {
                    color: #e0e0e0;
                    background: transparent;
                }
                QLineEdit {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                    padding: 12px 16px;
                    border-radius: 6px;
                    font-size: 12px;
                }
                QLineEdit:focus {
                    border: 1px solid #2196f3;
                }
                QPushButton {
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #1976d2;
                }
                QListWidget {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: none;
                    padding: 5px;
                }
                QListWidget::item {
                    border: none;
                    padding: 5px;
                }
                QListWidget::item:selected {
                    background-color: #3d3d3d;
                    color: #2196f3;
                }
                QMenuBar {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                }
                QMenuBar::item {
                    background: transparent;
                    padding: 4px 8px;
                }
                QMenuBar::item:selected {
                    background-color: #3d3d3d;
                }
                QMenu {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                }
                QMenu::item {
                    background: transparent;
                    padding: 4px 16px;
                }
                QMenu::item:selected {
                    background-color: #3d3d3d;
                }
                QStatusBar {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                }
                QFrame {
                    background-color: #444444;
                }
            """)
        else:
            self.setStyleSheet(global_border_reset + """
                QMainWindow {
                    background-color: #f9f9f9;
                    color: #333333;
                }
                QLabel {
                    color: #333333;
                    background: transparent;
                }
                QLineEdit {
                    background-color: white;
                    color: #333333;
                    border: 1px solid #cccccc;
                    padding: 12px 16px;
                    border-radius: 6px;
                    font-size: 12px;
                }
                QLineEdit:focus {
                    border: 1px solid #1976d2;
                }
                QPushButton {
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #1976d2;
                }
                QListWidget {
                    background-color: #f9f9f9;
                    color: #333333;
                    border: none;
                    padding: 5px;
                }
                QListWidget::item {
                    border: none;
                    padding: 5px;
                }
                QListWidget::item:selected {
                    background-color: #e3f2fd;
                    color: #1976d2;
                }
                QMenuBar {
                    background-color: #f9f9f9;
                    color: #333333;
                }
                QMenuBar::item {
                    background: transparent;
                    padding: 4px 8px;
                }
                QMenuBar::item:selected {
                    background-color: #e0e0e0;
                }
                QMenu {
                    background-color: #f9f9f9;
                    color: #333333;
                }
                QMenu::item {
                    background: transparent;
                    padding: 4px 16px;
                }
                QMenu::item:selected {
                    background-color: #e0e0e0;
                }
                QStatusBar {
                    color: #333333;
                    background: transparent;
                }
            """)
    
    def setup_menu(self):
        """设置菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu(TextConfig.MENU_FILE)
        
        new_task_action = QAction(TextConfig.ACTION_NEW_TASK, self)
        new_task_action.setShortcut("Ctrl+N")
        new_task_action.triggered.connect(self.show_new_task_dialog)
        file_menu.addAction(new_task_action)
        
        save_action = QAction(TextConfig.ACTION_SAVE, self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_tasks)
        file_menu.addAction(save_action)
        
        clear_action = QAction(TextConfig.ACTION_CLEAR_ALL, self)
        clear_action.triggered.connect(self.clear_tasks)
        file_menu.addAction(clear_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(TextConfig.ACTION_EXIT, self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 视图菜单
        view_menu = menubar.addMenu(TextConfig.MENU_VIEW)
        
        self.show_completed_action = QAction(TextConfig.ACTION_SHOW_COMPLETED, self)
        self.show_completed_action.setCheckable(True)
        self.show_completed_action.setChecked(True)
        self.show_completed_action.triggered.connect(self.filter_tasks)
        view_menu.addAction(self.show_completed_action)
        
        sort_priority_action = QAction(TextConfig.ACTION_SORT_PRIORITY, self)
        sort_priority_action.triggered.connect(lambda: self.sort_tasks("priority"))
        view_menu.addAction(sort_priority_action)
        
        sort_date_action = QAction(TextConfig.ACTION_SORT_DATE, self)
        sort_date_action.triggered.connect(lambda: self.sort_tasks("due_date"))
        view_menu.addAction(sort_date_action)
        
        view_menu.addSeparator()
        
        self.toggle_theme_action = QAction(TextConfig.ACTION_TOGGLE_THEME, self)
        self.toggle_theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(self.toggle_theme_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu(TextConfig.MENU_HELP)
        
        about_action = QAction(TextConfig.ACTION_ABOUT, self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_auto_save(self):
        """设置自动保存"""
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.timeout.connect(self.save_tasks)
        self.auto_save_timer.start(30000)  # 30秒自动保存
    
    def detect_dark_mode(self):
        """检测系统深色模式"""
        app = QApplication.instance()
        palette = app.palette()
        bg_color = palette.color(QPalette.Window)
        brightness = (bg_color.red() * 299 + bg_color.green() * 587 + bg_color.blue() * 114) / 1000
        return brightness < 128
    
    def load_tasks(self):
        """加载任务"""
        self.todo_list.clear()
        tasks = self.db.get_all_tasks()
        
        for task in tasks:
            self.add_task_to_list(task)
        
        self.statusBar().showMessage(TextConfig.STATUS_TASKS_LOADED, 3000)
    
    def add_task_to_list(self, task):
        """添加任务到列表"""
        item = QListWidgetItem()
        self.todo_list.addItem(item)
        
        widget = TodoListItem(task, is_dark_mode=self.is_dark_mode)
        widget.parent_item = item
        widget.deleted.connect(self.remove_task)
        widget.task_completed.connect(self.task_completed)
        widget.edited.connect(self.edit_task)
        
        item.setSizeHint(widget.sizeHint())
        self.todo_list.setItemWidget(item, widget)
    
    def show_new_task_dialog(self):
        """显示新建任务对话框"""
        dialog = TaskEditDialog(self, is_dark_mode=self.is_dark_mode)
        if dialog.exec():
            task_data = dialog.get_task_data()
            task = Task(
                id="",
                title=task_data["text"],
                priority=task_data["priority"],
                due_date=task_data["due_date"]
            )
            
            if self.db.add_task(task):
                self.add_task_to_list(task)
                self.statusBar().showMessage(
                    TextConfig.STATUS_TASK_ADDED.format(task.title), 3000
                )
    
    def show_quick_add_dialog(self):
        """显示快速添加对话框"""
        task_text = self.task_input.text().strip()
        if not task_text:
            QMessageBox.warning(self, TextConfig.WARNING_TITLE, TextConfig.WARNING_EMPTY_TASK)
            return
        
        dialog = TaskEditDialog(
            self,
            task_text=task_text,
            priority="MEDIUM",
            due_date=QDate.currentDate().addDays(1),
            is_dark_mode=self.is_dark_mode
        )
        
        if dialog.exec():
            task_data = dialog.get_task_data()
            task = Task(
                id="",
                title=task_data["text"],
                priority=task_data["priority"],
                due_date=task_data["due_date"]
            )
            
            if self.db.add_task(task):
                self.add_task_to_list(task)
                self.task_input.clear()
                self.statusBar().showMessage(
                    TextConfig.STATUS_QUICK_ADD_SUCCESS.format(task.title), 3000
                )
    
    def remove_task(self, item):
        """删除任务"""
        widget = self.todo_list.itemWidget(item)
        if widget and self.db.delete_task(widget.task.id):
            row = self.todo_list.row(item)
            self.todo_list.takeItem(row)
            self.statusBar().showMessage(TextConfig.STATUS_TASK_DELETED, 3000)
    
    def task_completed(self, item, is_completed):
        """任务完成状态改变"""
        widget = self.todo_list.itemWidget(item)
        if widget:
            self.db.update_task(widget.task.id, status=widget.task.status)
            status_msg = TextConfig.get_task_status_message(is_completed)
            self.statusBar().showMessage(status_msg, 3000)
    
    def edit_task(self, item):
        """编辑任务"""
        widget = self.todo_list.itemWidget(item)
        if not widget:
            return
        
        task = widget.task
        dialog = TaskEditDialog(
            self,
            task_text=task.title,
            priority=task.priority,
            due_date=QDate.fromString(task.due_date, "yyyy-MM-dd") if task.due_date else None,
            is_dark_mode=self.is_dark_mode
        )
        
        if dialog.exec():
            task_data = dialog.get_task_data()
            
            # 更新任务数据
            if self.db.update_task(
                task.id,
                title=task_data["text"],
                priority=task_data["priority"],
                due_date=task_data["due_date"]
            ):
                # 更新UI显示
                task.title = task_data["text"]
                task.priority = task_data["priority"]
                task.due_date = task_data["due_date"]
                widget.update_display()
                
                self.statusBar().showMessage(
                    TextConfig.STATUS_TASK_UPDATED.format(task.title), 3000
                )
    
    def show_context_menu(self, position):
        """显示右键菜单"""
        item = self.todo_list.itemAt(position)
        if item:
            context_menu = QMenu(self)
            
            edit_action = QAction(TextConfig.CONTEXT_EDIT, self)
            edit_action.triggered.connect(lambda: self.edit_task(item))
            context_menu.addAction(edit_action)
            
            delete_action = QAction(TextConfig.CONTEXT_DELETE, self)
            delete_action.triggered.connect(lambda: self.remove_task(item))
            context_menu.addAction(delete_action)
            
            context_menu.exec_(self.todo_list.mapToGlobal(position))
    
    def filter_tasks(self):
        """过滤任务"""
        show_completed = self.show_completed_action.isChecked()
        for i in range(self.todo_list.count()):
            item = self.todo_list.item(i)
            widget = self.todo_list.itemWidget(item)
            if widget:
                is_completed = widget.task.status == "COMPLETED"
                item.setHidden(is_completed and not show_completed)
    
    def sort_tasks(self, sort_by):
        """排序任务"""
        if sort_by == "priority":
            sorted_tasks = self.db.sort_tasks_by_priority()
        elif sort_by == "due_date":
            sorted_tasks = self.db.sort_tasks_by_due_date()
        else:
            return
        
        # 重新加载列表
        self.todo_list.clear()
        for task in sorted_tasks:
            self.add_task_to_list(task)
        
        status_msg = TextConfig.get_sort_status_message(sort_by)
        self.statusBar().showMessage(status_msg, 3000)
    
    def clear_tasks(self):
        """清空所有任务"""
        reply = QMessageBox.question(
            self,
            TextConfig.CONFIRM_CLEAR_TITLE,
            TextConfig.CONFIRM_CLEAR_MESSAGE,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.db.clear_all_tasks():
                self.todo_list.clear()
                self.statusBar().showMessage(TextConfig.STATUS_TASKS_CLEARED, 3000)
    
    def toggle_theme(self):
        """切换主题"""
        self.is_dark_mode = not self.is_dark_mode
        self.setup_style()
        
        # 更新所有任务项的主题
        for i in range(self.todo_list.count()):
            item = self.todo_list.item(i)
            widget = self.todo_list.itemWidget(item)
            if widget:
                widget.set_dark_mode(self.is_dark_mode)
        
        theme_name = TextConfig.get_theme_name(self.is_dark_mode)
        self.statusBar().showMessage(
            TextConfig.STATUS_THEME_SWITCHED.format(theme_name), 3000
        )
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, TextConfig.ABOUT_TITLE, TextConfig.ABOUT_MESSAGE)
    
    def save_tasks(self):
        """保存任务"""
        if not self.db.save_tasks():
            QMessageBox.warning(
                self,
                TextConfig.ERROR_SAVE_TITLE,
                TextConfig.ERROR_SAVE_TASKS.format("保存失败")
            )
    
    def closeEvent(self, event):
        """关闭事件"""
        self.save_tasks()
        event.accept()