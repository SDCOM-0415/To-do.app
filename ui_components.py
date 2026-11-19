"""
UI 组件 - Todo App v0.3.2
自定义界面组件
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date
import calendar
from date_input import format_date_input, parse_date_input
from localize_tk import localize_tk
from i18n import tr
from typing import Callable, Optional
from models import Task
from config import app_config
from font_preferences import current_font_family, ui_font_size

# 统一浅色/深色设计令牌（CustomTkinter 支持 (light, dark) 二元组自动响应系统主题）
THEME_TOKENS = {
    "canvas": ("#F4F6F9", "#11161D"),
    "sidebar": ("#E9EEF4", "#171D26"),
    "surface": ("#FFFFFF", "#1D2530"),
    "card": ("#F8FAFC", "#242E3B"),
    "card_hover": ("#EEF2F7", "#2C3847"),
    "input": ("#FFFFFF", "#171E27"),
    "text": ("#17212B", "#F1F5F9"),
    "secondary": ("#475569", "#CBD5E1"),
    "muted": ("#64748B", "#94A3B8"),
    "accent": ("#2563EB", "#3B82F6"),
    "accent_hover": ("#1D4ED8", "#2563EB"),
    "on_accent": ("#FFFFFF", "#FFFFFF"),
    "selected": ("#DCE8F8", "#263549"),
    "line": ("#DCE3EC", "#2D3948"),
    "danger": ("#DC2626", "#EF4444"),
    "danger_hover": ("#B91C1C", "#DC2626"),
    "danger_soft": ("#FEE2E2", "#3A2026"),
    "danger_soft_hover": ("#FECACA", "#4C262E"),
    "danger_text": ("#DC2626", "#FCA5A5"),
    "neutral_btn": ("#E2E8F0", "#2A3544"),
    "neutral_btn_hover": ("#CBD5E1", "#354356"),
    "overdue": ("#DC2626", "#F87171"),
    "due_today": ("#D97706", "#FBBF24"),
    "success": ("#16A34A", "#4ADE80"),
}


class TaskEditDialog(ctk.CTkToplevel):
    """任务编辑对话框"""
    
    def __init__(self, parent, task: Optional[Task] = None, callback: Optional[Callable] = None):
        super().__init__(parent)
        
        self.task = task
        self.callback = callback
        self.result = None
        
        # 设置窗口属性
        self.title("编辑任务" if task else "新建任务")
        self.geometry("560x540")
        self.minsize(500, 480)
        self.resizable(True, True)
        self.configure(fg_color=THEME_TOKENS["canvas"])
        
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
        localize_tk(self, app_config.get("language", "zh-cn"))
    
    def center_window(self):
        """窗口居中显示"""
        self.update_idletasks()
        width, height = 560, 540
        x = max(0, (self.winfo_screenwidth() - width) // 2)
        y = max(0, (self.winfo_screenheight() - height) // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """创建界面组件"""
        t = THEME_TOKENS
        family = current_font_family(app_config.get("font_mode", "harmony"))

        # 主框架
        main_frame = ctk.CTkFrame(
            self, fg_color=t["surface"], border_width=1, border_color=t["line"],
            corner_radius=12,
        )
        main_frame.pack(fill="both", expand=True, padx=16, pady=16)
        form = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        
        # 标题输入
        ctk.CTkLabel(
            form, text="任务标题:", text_color=t["text"],
            font=(family, ui_font_size(13), "bold"),
        ).pack(anchor="w", pady=(8, 6))
        self.title_entry = ctk.CTkEntry(
            form, height=38, corner_radius=8, border_width=1,
            fg_color=t["input"], border_color=t["line"], text_color=t["text"],
            font=(family, ui_font_size(12)),
        )
        self.title_entry.pack(fill="x", pady=(0, 14))
        
        # 描述输入
        ctk.CTkLabel(
            form, text="任务描述:", text_color=t["text"],
            font=(family, ui_font_size(13), "bold"),
        ).pack(anchor="w", pady=(0, 6))
        self.description_text = ctk.CTkTextbox(
            form, height=104, corner_radius=8, border_width=1,
            fg_color=t["input"], border_color=t["line"], text_color=t["text"],
            font=(family, ui_font_size(12)),
        )
        self.description_text.pack(fill="x", pady=(0, 14))
        
        # 优先级选择
        priority_frame = ctk.CTkFrame(
            form, fg_color=t["card"], border_width=1, border_color=t["line"],
            corner_radius=10,
        )
        priority_frame.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(
            priority_frame, text="优先级:", text_color=t["text"],
            font=(family, ui_font_size(13), "bold"),
        ).pack(side="left", padx=(14, 16), pady=10)
        
        self.priority_var = ctk.StringVar(value="中")
        language = app_config.get("language", "zh-cn")
        priority_options = ["高", "中", "低"]
        localized_priority = {tr(value, language): value for value in priority_options}
        self.priority_display_var = ctk.StringVar(value=tr("中", language))
        self.priority_menu = ctk.CTkOptionMenu(
            priority_frame,
            values=list(localized_priority),
            variable=self.priority_display_var,
            command=lambda selected: self.priority_var.set(localized_priority[selected]),
            fg_color=t["neutral_btn"], button_color=t["neutral_btn_hover"],
            button_hover_color=t["accent"], text_color=t["text"],
            corner_radius=8, height=32,
            font=(family, ui_font_size(12)),
        )
        self.priority_menu.pack(side="left", padx=(0, 12), pady=10)
        
        # 截止日期
        date_frame = ctk.CTkFrame(
            form, fg_color=t["card"], border_width=1, border_color=t["line"],
            corner_radius=10,
        )
        date_frame.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(
            date_frame, text="截止日期:", text_color=t["text"],
            font=(family, ui_font_size(13), "bold"),
        ).pack(side="left", padx=(14, 16), pady=10)
        
        self.due_date_var = ctk.StringVar()
        self.due_date_entry = ctk.CTkEntry(
            date_frame, textvariable=self.due_date_var,
            placeholder_text="YYYY/MM/DD（可选）",
            height=34, corner_radius=8, border_width=1,
            fg_color=t["input"], border_color=t["line"], text_color=t["text"],
            placeholder_text_color=t["muted"],
            font=(family, ui_font_size(12)),
        )
        self.due_date_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), pady=10)
        self.due_date_var.trace_add("write", self.on_date_input)
        ctk.CTkButton(
            date_frame, text="日历", width=66, height=34, corner_radius=8,
            fg_color=t["neutral_btn"], hover_color=t["neutral_btn_hover"],
            text_color=t["text"],
            font=(family, ui_font_size(12)),
            command=self.show_date_picker,
        ).pack(side="right", padx=(0, 10), pady=10)
        
        # 按钮框架
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(side="bottom", fill="x", padx=12, pady=(8, 12))
        
        # 取消按钮
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="取消",
            command=self.cancel,
            width=92, height=36, corner_radius=8,
            fg_color=t["neutral_btn"],
            hover_color=t["neutral_btn_hover"],
            text_color=t["text"],
            font=(family, ui_font_size(12)),
        )
        cancel_btn.pack(side="right", padx=(8, 0))
        
        # 确认按钮
        confirm_btn = ctk.CTkButton(
            button_frame,
            text="确认",
            command=self.confirm,
            width=96, height=36, corner_radius=8,
            fg_color=t["accent"],
            hover_color=t["accent_hover"],
            text_color=t["on_accent"],
            font=(family, ui_font_size(12), "bold"),
        )
        confirm_btn.pack(side="right")
        # 先分配固定底栏空间，再让表单占用剩余空间。
        form.pack(side="top", fill="both", expand=True, padx=10, pady=(10, 4))
        
        # 焦点设置
        self.title_entry.focus()
    
    def on_date_input(self, *_):
        if getattr(self, "_formatting_date", False):
            return
        raw = self.due_date_var.get()
        formatted = format_date_input(raw)
        if formatted != raw:
            self._formatting_date = True
            try:
                self.due_date_var.set(formatted)
                self.due_date_entry.icursor("end")
            finally:
                self._formatting_date = False

    def show_date_picker(self):
        """中文原生日历，不依赖额外第三方包。"""
        try:
            selected = parse_date_input(self.due_date_var.get())
        except ValueError:
            selected = None
        current = selected or date.today()
        popup = ctk.CTkToplevel(self)
        locale = app_config.get("language", "zh-cn")
        popup.title(tr("选择截止日期", locale))
        popup.geometry("330x350")
        popup.resizable(False, False)
        popup.transient(self)
        self.grab_release()
        family = current_font_family(app_config.get("font_mode", "harmony"))
        outer = ctk.CTkFrame(popup)
        outer.pack(fill="both", expand=True, padx=12, pady=12)
        header = ctk.CTkFrame(outer, fg_color="transparent")
        header.pack(fill="x", padx=6, pady=(6, 10))
        grid = ctk.CTkFrame(outer, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=6)
        display = ctk.StringVar()
        def close_picker():
            popup.grab_release()
            popup.destroy()
            if self.winfo_exists():
                self.grab_set()
                self.due_date_entry.focus_set()
        popup.protocol("WM_DELETE_WINDOW", close_picker)
        def move_month(offset):
            nonlocal current
            year = current.year + (current.month - 1 + offset) // 12
            month = (current.month - 1 + offset) % 12 + 1
            current = date(year, month, 1)
            render()
        def pick(day):
            self.due_date_var.set(f"{current.year:04d}/{current.month:02d}/{day:02d}")
            close_picker()
        ctk.CTkButton(header, text="‹", width=40, command=lambda: move_month(-1)).pack(side="left")
        ctk.CTkLabel(header, textvariable=display, font=(family, 15, "bold")).pack(
            side="left", fill="x", expand=True)
        ctk.CTkButton(header, text="›", width=40, command=lambda: move_month(1)).pack(side="right")
        def render():
            if locale == "en":
                display.set(f"{calendar.month_name[current.month]} {current.year}")
            else:
                display.set(f"{current.year} 年 {current.month} 月" if locale == "zh-cn"
                            else f"{current.year} 年 {current.month} 月")
            for widget in grid.winfo_children():
                widget.destroy()
            weekdays = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun") if locale == "en" else ("一", "二", "三", "四", "五", "六", "日")
            for col, weekday in enumerate(weekdays):
                ctk.CTkLabel(grid, text=weekday, font=(family, 12)).grid(
                    row=0, column=col, padx=2, pady=4)
            today = date.today()
            for row, week in enumerate(calendar.monthcalendar(current.year, current.month), start=1):
                for col, day in enumerate(week):
                    if day:
                        ctk.CTkButton(
                            grid, text=str(day), width=35, height=32,
                            fg_color=None if (day == today.day and current.year == today.year
                            and current.month == today.month) else "transparent",
                            text_color=("gray10", "gray90"),
                            command=lambda day=day: pick(day),
                        ).grid(row=row, column=col, padx=2, pady=2)
        render()
        popup.lift()
        popup.wait_visibility()
        popup.grab_set()

    def load_task_data(self):
        """加载任务数据到表单"""
        if self.task:
            self.title_entry.insert(0, self.task.title)
            self.description_text.insert("1.0", self.task.description)
            self.priority_var.set(self.task.priority)
            self.priority_display_var.set(tr(self.task.priority, app_config.get('language', 'zh-cn')))
            if self.task.due_date:
                # 只显示日期部分
                due_date = self.task.due_date.split('T')[0] if 'T' in self.task.due_date else self.task.due_date
                self.due_date_var.set(format_date_input(due_date))
    
    def validate_input(self) -> bool:
        """验证输入数据"""
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror(tr("错误", app_config.get("language")), tr("请输入任务标题", app_config.get("language")))
            return False
        
        try:
            parse_date_input(self.due_date_entry.get())
        except ValueError:
            messagebox.showerror(tr("日期无效", app_config.get("language")), tr("请使用 YYYY/MM/DD 格式输入有效日期", app_config.get("language")), parent=self)
            return False
        
        return True
    
    def confirm(self):
        """确认操作"""
        if not self.validate_input():
            return
        
        title = self.title_entry.get().strip()
        description = self.description_text.get("1.0", "end-1c").strip()
        priority = self.priority_var.get()
        parsed_date = parse_date_input(self.due_date_entry.get())
        due_date = f"{parsed_date.isoformat()}T23:59:59" if parsed_date else None
        
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
        
        self.destroy()
        if self.callback:
            self.callback(self.result)
    
    def cancel(self):
        """取消操作"""
        self.result = None
        self.destroy()

class TaskItem(ctk.CTkFrame):
    """任务列表项组件"""
    
    def __init__(self, parent, task: Task, on_toggle: Callable, on_edit: Callable, on_delete: Callable):
        t = THEME_TOKENS
        super().__init__(
            parent,
            height=0,
            fg_color=t["card"],
            border_width=1,
            border_color=t["line"],
            corner_radius=10,
        )
        
        self.task = task
        self.on_toggle = on_toggle
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        self.create_widgets()
        self.update_appearance()
    
    def create_widgets(self):
        """创建组件"""
        t = THEME_TOKENS
        family = current_font_family(app_config.get("font_mode", "harmony"))

        # 最左侧：细优先级色条（显式设置紧凑初始高度，避免 CTkFrame 默认 200px 撑高卡片）
        priority_color = app_config.get_priority_color(self.task.priority)
        self.priority_indicator = ctk.CTkFrame(
            self,
            width=4,
            height=34,
            corner_radius=2,
            fg_color=priority_color,
        )
        self.priority_indicator.pack(side="left", fill="y", padx=(10, 6), pady=10)

        # 左侧：复选框
        self.checkbox = ctk.CTkCheckBox(
            self,
            text="",
            command=self.toggle_completed,
            width=22,
            height=22,
            corner_radius=6,
            border_width=2,
            fg_color=t["accent"],
            hover_color=t["accent_hover"],
        )
        self.checkbox.pack(side="left", padx=(4, 8), pady=10)

        # 右侧：水平并排操作按钮（先 pack 右侧，保证标题区占据全部剩余宽度）
        right_frame = ctk.CTkFrame(self, height=0, fg_color="transparent")
        right_frame.pack(side="right", padx=(8, 12), pady=10)

        # 删除按钮
        delete_btn = ctk.CTkButton(
            right_frame,
            text="删除",
            width=50,
            height=28,
            corner_radius=7,
            command=lambda: self.on_delete(self.task),
            fg_color=t["danger_soft"],
            hover_color=t["danger_soft_hover"],
            text_color=t["danger_text"],
            font=(family, ui_font_size(11)),
        )
        delete_btn.pack(side="right", padx=(6, 0))

        # 编辑按钮
        edit_btn = ctk.CTkButton(
            right_frame,
            text="编辑",
            width=50,
            height=28,
            corner_radius=7,
            command=lambda: self.on_edit(self.task),
            fg_color=t["neutral_btn"],
            hover_color=t["neutral_btn_hover"],
            text_color=t["text"],
            font=(family, ui_font_size(11)),
        )
        edit_btn.pack(side="right")

        # 中间：任务信息
        middle_frame = ctk.CTkFrame(self, height=0, fg_color="transparent")
        middle_frame.pack(side="left", fill="both", expand=True, padx=(2, 6), pady=9)

        # 任务标题
        self.title_label = ctk.CTkLabel(
            middle_frame,
            text=self.task.title,
            font=(family, ui_font_size(14), "bold"),
            text_color=t["text"],
            anchor="w",
        )
        self.title_label._i18n_skip = True
        self.title_label.pack(fill="x", pady=(0, 2))

        # 任务描述
        if self.task.description:
            snippet = self.task.description.replace("\n", " ").strip()
            if len(snippet) > 68:
                snippet = snippet[:68] + "..."
            self.desc_label = ctk.CTkLabel(
                middle_frame,
                text=snippet,
                font=(family, ui_font_size(11)),
                anchor="w",
                text_color=t["secondary"],
            )
            self.desc_label._i18n_skip = True
            self.desc_label.pack(fill="x", pady=(0, 2))

        # 截止日期和状态信息
        info_text = []
        days_left = None
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
            if self.task.is_overdue():
                info_color = t["overdue"]
            elif days_left == 0 and not self.task.completed:
                info_color = t["due_today"]
            else:
                info_color = t["muted"]
            self.info_label = ctk.CTkLabel(
                middle_frame,
                text=" | ".join(tr(text, app_config.get("language", "zh-cn")) for text in info_text),
                font=(family, ui_font_size(11)),
                anchor="w",
                text_color=info_color,
            )
            self.info_label.pack(fill="x")
    
    def toggle_completed(self):
        """切换完成状态"""
        self.task.toggle_completed()
        self.on_toggle(self.task)
        self.update_appearance()
    
    def update_appearance(self):
        """更新外观"""
        t = THEME_TOKENS
        self.checkbox.select() if self.task.completed else self.checkbox.deselect()
        
        # 更新标题样式
        if self.task.completed:
            self.title_label.configure(text_color=t["muted"])
        else:
            self.title_label.configure(text_color=t["text"])
        
        # 更新优先级指示器颜色
        priority_color = app_config.get_priority_color(self.task.priority)
        self.priority_indicator.configure(fg_color=priority_color)


class StatisticsFrame(ctk.CTkFrame):
    """统计信息框架"""
    
    def __init__(self, parent):
        t = THEME_TOKENS
        super().__init__(
            parent,
            fg_color=t["surface"],
            border_width=1,
            border_color=t["line"],
            corner_radius=12,
        )
        self.create_widgets()
    
    def create_widgets(self):
        """创建统计组件"""
        t = THEME_TOKENS
        family = current_font_family(app_config.get("font_mode", "harmony"))

        # 标题
        title_label = ctk.CTkLabel(
            self,
            text="任务统计",
            text_color=t["text"],
            font=(family, ui_font_size(14), "bold"),
        )
        title_label.pack(anchor="w", padx=16, pady=(14, 8))
        
        # 统计信息容器
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=16, pady=(0, 8))
        
        # 初始化统计标签
        self.total_label = ctk.CTkLabel(
            self.stats_frame, text="总任务: 0", anchor="w",
            text_color=t["text"], font=(family, ui_font_size(12)),
        )
        self.total_label.pack(fill="x", pady=1)
        
        self.completed_label = ctk.CTkLabel(
            self.stats_frame, text="已完成: 0", anchor="w",
            text_color=t["success"], font=(family, ui_font_size(12)),
        )
        self.completed_label.pack(fill="x", pady=1)
        
        self.pending_label = ctk.CTkLabel(
            self.stats_frame, text="待完成: 0", anchor="w",
            text_color=t["secondary"], font=(family, ui_font_size(12)),
        )
        self.pending_label.pack(fill="x", pady=1)
        
        self.overdue_label = ctk.CTkLabel(
            self.stats_frame, text="已过期: 0", anchor="w",
            text_color=t["overdue"], font=(family, ui_font_size(12)),
        )
        self.overdue_label.pack(fill="x", pady=1)
        
        self.completion_rate_label = ctk.CTkLabel(
            self.stats_frame, text="完成率: 0%", anchor="w",
            text_color=t["muted"], font=(family, ui_font_size(12)),
        )
        self.completion_rate_label.pack(fill="x", pady=(4, 4))

        self.progress_bar = ctk.CTkProgressBar(
            self.stats_frame,
            height=6,
            corner_radius=3,
            fg_color=t["line"],
            progress_color=t["accent"],
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(2, 6))
    
    def update_statistics(self, stats: dict):
        """更新统计信息"""
        self.total_label.configure(text=f"总任务: {stats['total']}")
        self.completed_label.configure(text=f"已完成: {stats['completed']}")
        self.pending_label.configure(text=f"待完成: {stats['pending']}")
        self.overdue_label.configure(text=f"已过期: {stats['overdue']}")
        rate = float(stats.get("completion_rate", 0.0))
        self.completion_rate_label.configure(text=f"完成率: {rate:.1f}%")
        if hasattr(self, "progress_bar"):
            self.progress_bar.set(max(0.0, min(1.0, rate / 100.0)))