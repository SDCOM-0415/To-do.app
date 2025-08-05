"""
UI 组件 - Todo App v0.3
自定义界面组件
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date
from typing import Callable, Optional
from models import Task
from config import app_config

class TaskEditDialog(ctk.CTkToplevel):
    """任务编辑对话框"""
    
    def __init__(self, parent, task: Optional[Task] = None, callback: Optional[Callable] = None):
        super().__init__(parent)
        
        self.task = task
        self.callback = callback
        self.result = None
        
        # 设置窗口属性
        self.title("编辑任务" if task else "新建任务")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # 设置为模态窗口
        self.transient(parent)
        self.grab_set()
        
        # 居中显示
        self.center_window()
        
        # 创建界面
        self.create_widgets()
        
        # 如果是编辑模式，填充现有数据
        if task:
            self.load_task_data()
    
    def center_window(self):
        """窗口居中显示"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        self.geometry(f"500x400+{x}+{y}")
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题输入
        ctk.CTkLabel(main_frame, text="任务标题:", font=("", 14)).pack(anchor="w", pady=(10, 5))
        self.title_entry = ctk.CTkEntry(main_frame, height=35, font=("", 12))
        self.title_entry.pack(fill="x", pady=(0, 15))
        
        # 描述输入
        ctk.CTkLabel(main_frame, text="任务描述:", font=("", 14)).pack(anchor="w", pady=(0, 5))
        self.description_text = ctk.CTkTextbox(main_frame, height=100, font=("", 12))
        self.description_text.pack(fill="x", pady=(0, 15))
        
        # 优先级选择
        priority_frame = ctk.CTkFrame(main_frame)
        priority_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(priority_frame, text="优先级:", font=("", 14)).pack(side="left", padx=(10, 20))
        
        self.priority_var = ctk.StringVar(value="中")
        priority_options = ["高", "中", "低"]
        self.priority_menu = ctk.CTkOptionMenu(
            priority_frame, 
            values=priority_options,
            variable=self.priority_var,
            font=("", 12)
        )
        self.priority_menu.pack(side="left", padx=(0, 10))
        
        # 截止日期
        date_frame = ctk.CTkFrame(main_frame)
        date_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(date_frame, text="截止日期:", font=("", 14)).pack(side="left", padx=(10, 20))
        
        self.due_date_entry = ctk.CTkEntry(date_frame, placeholder_text="YYYY-MM-DD (可选)", font=("", 12))
        self.due_date_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # 按钮框架
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=(20, 10))
        
        # 取消按钮
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="取消",
            command=self.cancel,
            fg_color="gray",
            hover_color="darkgray",
            font=("", 12)
        )
        cancel_btn.pack(side="right", padx=(10, 10))
        
        # 确认按钮
        confirm_btn = ctk.CTkButton(
            button_frame,
            text="确认",
            command=self.confirm,
            font=("", 12)
        )
        confirm_btn.pack(side="right")
        
        # 焦点设置
        self.title_entry.focus()
    
    def load_task_data(self):
        """加载任务数据到表单"""
        if self.task:
            self.title_entry.insert(0, self.task.title)
            self.description_text.insert("1.0", self.task.description)
            self.priority_var.set(self.task.priority)
            if self.task.due_date:
                # 只显示日期部分
                due_date = self.task.due_date.split('T')[0] if 'T' in self.task.due_date else self.task.due_date
                self.due_date_entry.insert(0, due_date)
    
    def validate_input(self) -> bool:
        """验证输入数据"""
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("错误", "请输入任务标题")
            return False
        
        due_date = self.due_date_entry.get().strip()
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("错误", "日期格式不正确，请使用 YYYY-MM-DD 格式")
                return False
        
        return True
    
    def confirm(self):
        """确认操作"""
        if not self.validate_input():
            return
        
        title = self.title_entry.get().strip()
        description = self.description_text.get("1.0", "end-1c").strip()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get().strip()
        
        # 处理截止日期
        if due_date:
            due_date = f"{due_date}T23:59:59"
        else:
            due_date = None
        
        if self.task:
            # 编辑模式
            self.task.update(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date
            )
            self.result = self.task
        else:
            # 新建模式
            self.result = Task(
                id="",  # 将在 Task.__post_init__ 中生成
                title=title,
                description=description,
                priority=priority,
                due_date=due_date
            )
        
        if self.callback:
            self.callback(self.result)
        
        self.destroy()
    
    def cancel(self):
        """取消操作"""
        self.result = None
        self.destroy()

class TaskItem(ctk.CTkFrame):
    """任务列表项组件"""
    
    def __init__(self, parent, task: Task, on_toggle: Callable, on_edit: Callable, on_delete: Callable):
        super().__init__(parent)
        
        self.task = task
        self.on_toggle = on_toggle
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        self.create_widgets()
        self.update_appearance()
    
    def create_widgets(self):
        """创建组件"""
        # 主容器
        self.configure(height=80, corner_radius=8)
        self.pack_propagate(False)
        
        # 左侧：复选框和优先级指示器
        left_frame = ctk.CTkFrame(self, width=60, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=(10, 5))
        left_frame.pack_propagate(False)
        
        # 复选框
        self.checkbox = ctk.CTkCheckBox(
            left_frame,
            text="",
            command=self.toggle_completed,
            width=20,
            height=20
        )
        self.checkbox.pack(pady=(15, 5))
        
        # 优先级指示器
        priority_color = app_config.get_priority_color(self.task.priority)
        self.priority_indicator = ctk.CTkFrame(
            left_frame,
            width=20,
            height=20,
            corner_radius=10,
            fg_color=priority_color
        )
        self.priority_indicator.pack()
        
        # 中间：任务信息
        middle_frame = ctk.CTkFrame(self, fg_color="transparent")
        middle_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # 任务标题
        self.title_label = ctk.CTkLabel(
            middle_frame,
            text=self.task.title,
            font=("", 14, "bold"),
            anchor="w"
        )
        self.title_label.pack(fill="x", pady=(10, 2))
        
        # 任务描述
        if self.task.description:
            self.desc_label = ctk.CTkLabel(
                middle_frame,
                text=self.task.description[:50] + ("..." if len(self.task.description) > 50 else ""),
                font=("", 11),
                anchor="w",
                text_color="gray"
            )
            self.desc_label.pack(fill="x", pady=(0, 2))
        
        # 截止日期和状态信息
        info_text = []
        if self.task.due_date:
            due_date = self.task.due_date.split('T')[0]
            days_left = self.task.days_until_due()
            if days_left is not None:
                if days_left < 0:
                    info_text.append(f"已过期 {abs(days_left)} 天")
                elif days_left == 0:
                    info_text.append("今天到期")
                elif days_left <= 3:
                    info_text.append(f"{days_left} 天后到期")
                else:
                    info_text.append(f"截止: {due_date}")
        
        if info_text:
            self.info_label = ctk.CTkLabel(
                middle_frame,
                text=" | ".join(info_text),
                font=("", 10),
                anchor="w",
                text_color="orange" if self.task.is_overdue() else "gray"
            )
            self.info_label.pack(fill="x")
        
        # 右侧：操作按钮
        right_frame = ctk.CTkFrame(self, width=100, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=(5, 10))
        right_frame.pack_propagate(False)
        
        # 编辑按钮
        edit_btn = ctk.CTkButton(
            right_frame,
            text="编辑",
            width=40,
            height=25,
            command=lambda: self.on_edit(self.task),
            font=("", 10)
        )
        edit_btn.pack(pady=(15, 5))
        
        # 删除按钮
        delete_btn = ctk.CTkButton(
            right_frame,
            text="删除",
            width=40,
            height=25,
            command=lambda: self.on_delete(self.task),
            fg_color="red",
            hover_color="darkred",
            font=("", 10)
        )
        delete_btn.pack()
    
    def toggle_completed(self):
        """切换完成状态"""
        self.task.toggle_completed()
        self.on_toggle(self.task)
        self.update_appearance()
    
    def update_appearance(self):
        """更新外观"""
        self.checkbox.select() if self.task.completed else self.checkbox.deselect()
        
        # 更新标题样式
        if self.task.completed:
            self.title_label.configure(text_color="gray")
            # 这里可以添加删除线效果，但 customtkinter 不直接支持
        else:
            self.title_label.configure(text_color=("black", "white"))
        
        # 更新优先级指示器颜色
        priority_color = app_config.get_priority_color(self.task.priority)
        self.priority_indicator.configure(fg_color=priority_color)

class StatisticsFrame(ctk.CTkFrame):
    """统计信息框架"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
    
    def create_widgets(self):
        """创建统计组件"""
        # 标题
        title_label = ctk.CTkLabel(self, text="任务统计", font=("", 16, "bold"))
        title_label.pack(pady=(10, 15))
        
        # 统计信息容器
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # 初始化统计标签
        self.total_label = ctk.CTkLabel(self.stats_frame, text="总任务: 0", font=("", 12))
        self.total_label.pack(pady=2)
        
        self.completed_label = ctk.CTkLabel(self.stats_frame, text="已完成: 0", font=("", 12))
        self.completed_label.pack(pady=2)
        
        self.pending_label = ctk.CTkLabel(self.stats_frame, text="待完成: 0", font=("", 12))
        self.pending_label.pack(pady=2)
        
        self.overdue_label = ctk.CTkLabel(self.stats_frame, text="已过期: 0", font=("", 12))
        self.overdue_label.pack(pady=2)
        
        self.completion_rate_label = ctk.CTkLabel(self.stats_frame, text="完成率: 0%", font=("", 12))
        self.completion_rate_label.pack(pady=2)
    
    def update_statistics(self, stats: dict):
        """更新统计信息"""
        self.total_label.configure(text=f"总任务: {stats['total']}")
        self.completed_label.configure(text=f"已完成: {stats['completed']}")
        self.pending_label.configure(text=f"待完成: {stats['pending']}")
        self.overdue_label.configure(text=f"已过期: {stats['overdue']}")
        self.completion_rate_label.configure(text=f"完成率: {stats['completion_rate']:.1f}%")