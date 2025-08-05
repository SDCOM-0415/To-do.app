"""
UI组件模块
包含自定义的UI组件和对话框
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QListWidget, QListWidgetItem, QLabel, QCheckBox, QComboBox, 
    QDateEdit, QDialog, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QSize, QDate
from PySide6.QtGui import QIcon, QFont
from config import COLORS, PRIORITY_LEVELS, TASK_STATUS
from text_config import TextConfig

class TaskEditDialog(QDialog):
    """任务编辑对话框"""
    
    def __init__(self, parent=None, task_text="", priority="MEDIUM", due_date=None, is_dark_mode=False):
        super().__init__(parent)
        self.setWindowTitle(TextConfig.EDIT_DIALOG_TITLE)
        self.is_dark_mode = is_dark_mode
        self.setup_ui()
        self.setup_style()
        
        # 设置初始值
        self.text_input.setText(task_text)
        self.priority_combo.setCurrentText(PRIORITY_LEVELS.get(priority, "中"))
        
        if due_date:
            if isinstance(due_date, str):
                self.date_edit.setDate(QDate.fromString(due_date, "yyyy-MM-dd"))
            else:
                self.date_edit.setDate(due_date)
        else:
            self.date_edit.setDate(QDate.currentDate().addDays(1))
    
    def setup_ui(self):
        """设置UI布局"""
        layout = QFormLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 任务文本输入
        self.text_input = QLineEdit()
        layout.addRow(TextConfig.TASK_CONTENT_LABEL, self.text_input)
        
        # 优先级选择
        self.priority_combo = QComboBox()
        self.priority_combo.addItems([PRIORITY_LEVELS[key] for key in ["LOW", "MEDIUM", "HIGH"]])
        layout.addRow(TextConfig.PRIORITY_LABEL, self.priority_combo)
        
        # 截止日期选择
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        layout.addRow(TextConfig.DUE_DATE_LABEL, self.date_edit)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton(TextConfig.CONFIRM_BUTTON)
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton(TextConfig.CANCEL_BUTTON)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addRow("", button_layout)
        self.setMinimumWidth(300)
    
    def setup_style(self):
        """设置样式"""
        if self.is_dark_mode:
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
                    border-radius: 3px;
                }
                QPushButton {
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #1976d2;
                }
                QComboBox, QDateEdit {
                    background-color: #3d3d3d;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                    padding: 5px;
                    border-radius: 3px;
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
                    border-radius: 3px;
                }
                QPushButton {
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #1976d2;
                }
                QComboBox, QDateEdit {
                    background-color: white;
                    color: #333333;
                    border: 1px solid #cccccc;
                    padding: 5px;
                    border-radius: 3px;
                }
            """)
    
    def get_task_data(self):
        """获取任务数据"""
        # 将中文优先级转换为英文
        priority_map = {"低": "LOW", "中": "MEDIUM", "高": "HIGH"}
        priority_text = self.priority_combo.currentText()
        priority = priority_map.get(priority_text, "MEDIUM")
        
        return {
            "text": self.text_input.text(),
            "priority": priority,
            "due_date": self.date_edit.date().toString("yyyy-MM-dd")
        }

class TodoListItem(QWidget):
    """待办事项列表项组件"""
    
    deleted = Signal(QListWidgetItem)
    task_completed = Signal(QListWidgetItem, bool)
    edited = Signal(QListWidgetItem)
    
    def __init__(self, task, parent=None, is_dark_mode=False):
        super().__init__(parent)
        self.task = task
        self.is_dark_mode = is_dark_mode
        self.setup_ui()
        self.setup_style()
        self.update_display()
    
    def setup_ui(self):
        """设置UI布局"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # 完成复选框
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.task.status == "COMPLETED")
        self.checkbox.stateChanged.connect(self.on_state_changed)
        layout.addWidget(self.checkbox)
        
        # 优先级标签
        self.priority_label = QLabel()
        self.priority_label.setFixedSize(16, 16)
        self.update_priority_label()
        layout.addWidget(self.priority_label)
        
        # 任务文本标签
        self.label = QLabel(self.task.title)
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignVCenter)
        self.label.setFixedHeight(44)
        layout.addWidget(self.label, 1)
        
        # 截止日期标签
        if self.task.due_date:
            self.date_label = QLabel()
            self.update_date_label()
            layout.addWidget(self.date_label)
        
        # 按钮容器
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        
        # 编辑按钮
        self.edit_button = QPushButton()
        self.edit_button.setFixedSize(28, 28)
        self.edit_button.setToolTip(TextConfig.EDIT_TOOLTIP)
        self.edit_button.clicked.connect(self.on_edit_clicked)
        button_layout.addWidget(self.edit_button)
        
        # 删除按钮
        self.delete_button = QPushButton()
        self.delete_button.setFixedSize(28, 28)
        self.delete_button.setToolTip(TextConfig.DELETE_TOOLTIP)
        self.delete_button.clicked.connect(self.on_delete_clicked)
        button_layout.addWidget(self.delete_button)
        
        layout.addWidget(button_container, 0, Qt.AlignTop)
    
    def setup_style(self):
        """设置样式"""
        self.update_label_style()
        self.update_button_style()
    
    def update_display(self):
        """更新显示内容"""
        self.label.setText(self.task.title)
        self.checkbox.setChecked(self.task.status == "COMPLETED")
        self.update_priority_label()
        if hasattr(self, 'date_label'):
            self.update_date_label()
        self.update_label_style()
    
    def update_priority_label(self):
        """更新优先级标签"""
        priority_text = PRIORITY_LEVELS.get(self.task.priority, "中")
        color = TextConfig.PRIORITY_COLORS.get(priority_text, "#ffc107")
        self.priority_label.setStyleSheet(f"background-color: {color}; border-radius: 8px;")
        self.priority_label.setToolTip(TextConfig.get_priority_tooltip(priority_text))
    
    def update_date_label(self):
        """更新日期标签"""
        if not hasattr(self, 'date_label') or not self.task.due_date:
            return
        
        try:
            due_date = QDate.fromString(self.task.due_date, "yyyy-MM-dd")
            days_left = QDate.currentDate().daysTo(due_date)
            
            if days_left < 0:
                self.date_label.setStyleSheet("color: #dc3545; font-size: 9pt; font-weight: bold;")
                self.date_label.setText(f"{TextConfig.DUE_OVERDUE}{self.task.due_date}")
            elif days_left == 0:
                self.date_label.setStyleSheet("color: #dc3545; font-size: 9pt; font-weight: bold;")
                self.date_label.setText(TextConfig.DUE_TODAY)
            elif days_left <= 2:
                self.date_label.setStyleSheet("color: #ffc107; font-size: 9pt; font-weight: bold;")
                self.date_label.setText(f"{TextConfig.DUE_SOON}{self.task.due_date}")
            else:
                self.date_label.setStyleSheet("color: gray; font-size: 9pt;")
                self.date_label.setText(f"{TextConfig.DUE_DATE_PREFIX}{self.task.due_date}")
        except Exception:
            pass
    
    def update_label_style(self):
        """更新标签样式"""
        is_completed = self.task.status == "COMPLETED"
        base_style = "text-decoration: line-through; " if is_completed else ""
        
        if is_completed:
            color = "#888888" if self.is_dark_mode else "gray"
        else:
            color = "#e0e0e0" if self.is_dark_mode else "#333333"
        
        self.label.setStyleSheet(f"border: none; background: transparent; padding: 12px 0px; {base_style}color: {color};")
    
    def update_button_style(self):
        """更新按钮样式"""
        if self.is_dark_mode:
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
        else:
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
        """设置深色模式"""
        self.is_dark_mode = is_dark
        self.update_label_style()
        self.update_button_style()
        if hasattr(self, 'date_label'):
            self.update_date_label()
    
    def on_state_changed(self, state):
        """复选框状态改变"""
        is_completed = (state == Qt.CheckState.Checked.value)
        if is_completed:
            self.task.mark_completed()
        else:
            self.task.mark_pending()
        
        self.update_label_style()
        parent_item = getattr(self, 'parent_item', None)
        self.task_completed.emit(parent_item, is_completed)
    
    def on_delete_clicked(self):
        """删除按钮点击"""
        parent_window = self.window()
        reply = QMessageBox.question(
            parent_window,
            TextConfig.CONFIRM_DELETE_TITLE,
            TextConfig.CONFIRM_DELETE_MESSAGE.format(self.task.title),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            parent_item = getattr(self, 'parent_item', None)
            self.deleted.emit(parent_item)
    
    def on_edit_clicked(self):
        """编辑按钮点击"""
        parent_item = getattr(self, 'parent_item', None)
        self.edited.emit(parent_item)