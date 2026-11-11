"""
主应用程序 - Todo App v0.3.2
现代化跨平台待办事项管理器
支持 Windows、Linux、macOS 和深色模式
"""
import customtkinter as ctk
from tkinter import messagebox
import threading
import time
from typing import List, Optional
from models import Task
from database import task_db
from config import app_config
from ui_components import TaskEditDialog, TaskItem, StatisticsFrame
from settings_dialog import SettingsDialog
from modern_ui import create_modern_widgets, normalize_layout
from font_preferences import apply_tk_font, current_font_family, ui_font_size
from localize_tk import localize_tk
from i18n import tr

class TodoApp(ctk.CTk):
    """主应用程序类"""
    
    def localized_messagebox(self, kind: str, title: str, message: str, **options):
        language = app_config.get("language", "zh-cn")
        return getattr(messagebox, kind)(tr(title, language), tr(message, language), **options)

    def __init__(self):
        super().__init__()
        
        # 设置主题
        self.setup_theme()
        self.current_theme = app_config.get("theme", "system")
        self.current_font_mode = app_config.get("font_mode", "harmony")
        self.current_font_size = int(app_config.get("font_size", 14))
        self.current_language = app_config.get("language", "zh-cn")
        
        # 设置窗口属性
        self.setup_window()
        
        # 创建界面
        self.create_widgets()
        
        # 首次启动也必须应用已保存的语言，而不只在保存设置后翻译。
        localize_tk(self, self.current_language)

        # 加载任务
        self.refresh_tasks()
        
        # 启动自动保存
        self.start_auto_save()
        
        # 绑定关闭事件
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_theme(self):
        """设置主题"""
        theme = app_config.get("theme", "dark")
        if theme == "system":
            ctk.set_appearance_mode("system")
        else:
            ctk.set_appearance_mode(theme)
        
        ctk.set_default_color_theme("blue")
        apply_tk_font(self, app_config.get("font_mode", "harmony"))
    
    def setup_window(self):
        """设置窗口属性"""
        self.title(f"{app_config.app_name} - {tr('现代化待办事项管理器', app_config.get('language', 'zh-cn'))}")
        
        # 设置窗口大小和位置
        window_size = app_config.get("window_size", "900x700")
        self.geometry(window_size)
        self.minsize(800, 600)
        
        # 设置窗口图标（如果有的话）
        try:
            self.iconbitmap("icon.ico")
        except:
            pass
    
    def create_widgets(self):
        """根据偏好构建经典或现代工作空间。"""
        self.ui_layout = normalize_layout(app_config.get("ui_layout", "classic"))
        if self.ui_layout == "modern":
            create_modern_widgets(self)
        else:
            self.create_classic_widgets()

    def create_classic_widgets(self):
        """保留原版 Tk UI，不改变其任务操作。"""
        # 主容器
        main_container = ctk.CTkFrame(self)
        self.main_container = main_container
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 顶部工具栏
        self.create_toolbar(main_container)
        
        # 主内容区域
        content_frame = ctk.CTkFrame(main_container)
        content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # 左侧：任务列表
        self.create_task_list(content_frame)
        
        # 右侧：统计和控制面板
        self.create_control_panel(content_frame)
    
    def create_toolbar(self, parent):
        """创建工具栏"""
        toolbar = ctk.CTkFrame(parent, height=60)
        toolbar.pack(fill="x", pady=(0, 10))
        toolbar.pack_propagate(False)
        
        # 左侧：标题
        title_label = ctk.CTkLabel(
            toolbar,
            text=f"📝 Todo App v{app_config.version}",
            font=(current_font_family(app_config.get("font_mode", "harmony")), ui_font_size(20), "bold")
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # 右侧：主题切换和设置按钮
        # 右侧：设置按钮
        right_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        right_frame.pack(side="right", padx=20, pady=10)
        
        # 设置按钮
        settings_btn = ctk.CTkButton(
            right_frame,
            text="⚙️",
            width=40,
            height=40,
            command=self.show_settings,
            font=(current_font_family(app_config.get("font_mode", "harmony")), ui_font_size(16))
        )
        settings_btn.pack(side="right")
    
    def create_task_list(self, parent):
        """创建任务列表区域"""
        # 左侧框架
        left_frame = ctk.CTkFrame(parent)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # 任务输入区域
        input_frame = ctk.CTkFrame(left_frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # 快速添加输入框
        self.task_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="输入新任务，按回车快速添加...",
            height=40,
            font=(current_font_family(app_config.get("font_mode", "harmony")), ui_font_size(14))
        )
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        self.task_entry.bind("<Return>", self.quick_add_task)
        
        # 详细添加按钮
        add_btn = ctk.CTkButton(
            input_frame,
            text="详细添加",
            width=100,
            height=40,
            command=self.show_add_dialog,
            font=(current_font_family(app_config.get("font_mode", "harmony")), ui_font_size(12))
        )
        add_btn.pack(side="right", padx=(5, 10), pady=10)
        
        # 过滤和排序控制
        filter_frame = ctk.CTkFrame(left_frame)
        filter_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # 显示选项
        self.show_completed_var = ctk.BooleanVar(value=app_config.get("show_completed", True))
        show_completed_cb = ctk.CTkCheckBox(
            filter_frame,
            text="显示已完成",
            variable=self.show_completed_var,
            command=self.refresh_tasks,
            font=(current_font_family(app_config.get("font_mode", "harmony")), ui_font_size(12))
        )
        show_completed_cb.pack(side="left", padx=10, pady=10)
        
        # 排序选项
        ctk.CTkLabel(filter_frame, text="排序:", font=(current_font_family(app_config.get("font_mode", "harmony")), ui_font_size(12))).pack(side="left", padx=(20, 5), pady=10)
        
        self.sort_var = ctk.StringVar(value="创建时间")
        language = app_config.get("language", "zh-cn")
        sort_choices = ["创建时间", "优先级", "截止日期", "标题", "完成状态"]
        sort_display = {tr(key, language): key for key in sort_choices}
        self.sort_display_var = ctk.StringVar(value=tr("创建时间", language))
        sort_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=list(sort_display),
            variable=self.sort_display_var,
            command=lambda selected: (
                self.sort_var.set(sort_display[selected]), self.on_sort_changed(selected)),

            font=(current_font_family(app_config.get("font_mode", "harmony")), ui_font_size(12))
        )
        sort_menu.pack(side="left", padx=5, pady=10)
        
        # 搜索框
        self.search_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="搜索任务...",
            width=150,
            font=(current_font_family(app_config.get("font_mode", "harmony")), ui_font_size(12))
        )
        self.search_entry.pack(side="right", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", self.on_search_changed)
        
        # 任务列表滚动区域
        self.task_list_frame = ctk.CTkScrollableFrame(left_frame)
        self.task_list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def create_control_panel(self, parent):
        """创建控制面板"""
        # 右侧框架
        right_frame = ctk.CTkFrame(parent, width=250)
        right_frame.pack(side="right", fill="y", padx=(5, 0))
        right_frame.pack_propagate(False)
        
        # 统计信息
        self.stats_frame = StatisticsFrame(right_frame)
        self.stats_frame.pack(fill="x", padx=10, pady=10)
        
        # 快捷操作
        actions_frame = ctk.CTkFrame(right_frame)
        actions_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(actions_frame, text="快捷操作", font=(current_font_family(app_config.get("font_mode", "harmony")), ui_font_size(16), "bold")).pack(pady=(10, 15))
        
        # 清除已完成任务
        clear_completed_btn = ctk.CTkButton(
            actions_frame,
            text="清除已完成任务",
            command=self.clear_completed_tasks,
            font=(current_font_family(app_config.get("font_mode", "harmony")), ui_font_size(12))
        )
        clear_completed_btn.pack(fill="x", padx=10, pady=5)
        
        # 清除所有任务
        clear_all_btn = ctk.CTkButton(
            actions_frame,
            text="清除所有任务",
            command=self.clear_all_tasks,
            fg_color="red",
            hover_color="darkred",
            font=(current_font_family(app_config.get("font_mode", "harmony")), ui_font_size(12))
        )
        clear_all_btn.pack(fill="x", padx=10, pady=5)
        
        # 导出任务
        export_btn = ctk.CTkButton(
            actions_frame,
            text="导出任务",
            command=self.export_tasks,
            font=(current_font_family(app_config.get("font_mode", "harmony")), ui_font_size(12))
        )
        export_btn.pack(fill="x", padx=10, pady=(5, 15))
    
    def quick_add_task(self, event=None):
        """快速添加任务"""
        title = self.task_entry.get().strip()
        if not title:
            return
        
        task = Task(id="", title=title)
        if task_db.add_task(task):
            self.task_entry.delete(0, "end")
            self.refresh_tasks()
            self.show_status_message(f"已添加任务: {title}")
        else:
            self.localized_messagebox("showerror", "错误", "添加任务失败")
    
    def show_add_dialog(self):
        """显示详细添加对话框"""
        dialog = TaskEditDialog(self, callback=self.on_task_added)
    
    def on_task_added(self, task: Task):
        """任务添加回调"""
        if task_db.add_task(task):
            self.refresh_tasks()
            self.show_status_message(f"已添加任务: {task.title}")
        else:
            self.localized_messagebox("showerror", "错误", "添加任务失败")
    
    def on_task_toggle(self, task: Task):
        """任务状态切换回调"""
        if task_db.update_task(task.id, completed=task.completed):
            self.refresh_tasks()
            status = "完成" if task.completed else "未完成"
            self.show_status_message(f"任务已标记为{status}")
    
    def on_task_edit(self, task: Task):
        """编辑任务"""
        dialog = TaskEditDialog(self, task, self.on_task_edited)
    
    def on_task_edited(self, task: Task):
        """任务编辑回调"""
        if task_db.save_tasks():
            self.refresh_tasks()
            self.show_status_message(f"已更新任务: {task.title}")
        else:
            self.localized_messagebox("showerror", "错误", "更新任务失败")
    
    def on_task_delete(self, task: Task):
        """删除任务"""
        if self.localized_messagebox("askyesno", "确认删除", f"确定要删除任务 '{task.title}' 吗？"):
            if task_db.delete_task(task.id):
                self.refresh_tasks()
                self.show_status_message(f"已删除任务: {task.title}")
            else:
                self.localized_messagebox("showerror", "错误", "删除任务失败")
    
    def refresh_tasks(self):
        """刷新任务列表"""
        # 清空现有任务项
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        
        # 获取任务列表
        tasks = self.get_filtered_and_sorted_tasks()
        
        # 创建任务项
        for task in tasks:
            # “已完成”专用视图不受全局显示开关影响。
            completed_view = (getattr(self, "ui_layout", "classic") == "modern"
                              and getattr(self, "current_view", "") == "已完成")
            if not completed_view and not self.show_completed_var.get() and task.completed:
                continue
            
            task_item = TaskItem(
                self.task_list_frame,
                task,
                self.on_task_toggle,
                self.on_task_edit,
                self.on_task_delete
            )
            task_item.pack(fill="x", padx=5, pady=2)
        
        # 更新统计信息
        self.update_statistics()
        # Newly created task cards and refreshed counters also need the
        # current locale, not only the initial settings callback.
        localize_tk(self.task_list_frame, app_config.get("language", "zh-cn"))
        if hasattr(self, "stats_frame"):
            localize_tk(self.stats_frame, app_config.get("language", "zh-cn"))

    def get_filtered_and_sorted_tasks(self) -> List[Task]:
        """获取过滤和排序后的任务列表"""
        # 搜索过滤
        search_query = self.search_entry.get().strip()
        if search_query:
            tasks = task_db.search_tasks(search_query)
        else:
            tasks = task_db.get_all_tasks()
        
        # 现代导航可按任务状态进一步筛选，不改变原始任务数据。
        if getattr(self, "ui_layout", "classic") == "modern":
            view = getattr(self, "current_view", "全部任务")
            if view == "进行中":
                tasks = [task for task in tasks if not task.completed]
            elif view == "已完成":
                tasks = [task for task in tasks if task.completed]

        # 排序
        sort_mapping = {
            "创建时间": "created_at",
            "优先级": "priority", 
            "截止日期": "due_date",
            "标题": "title",
            "完成状态": "completed"
        }
        sort_key = sort_mapping.get(tr(self.sort_var.get(), "zh-cn"), "created_at")
        
        if sort_key == "priority":
            tasks = sorted(tasks, key=lambda x: (x.completed, -x.get_priority_weight()))
        elif sort_key == "due_date":
            tasks = sorted(tasks, key=lambda x: (x.completed, x.due_date or "9999-12-31"))
        elif sort_key == "title":
            tasks = sorted(tasks, key=lambda x: (x.completed, x.title.lower()))
        elif sort_key == "completed":
            tasks = sorted(tasks, key=lambda x: x.completed)
        else:  # created_at
            tasks = sorted(tasks, key=lambda x: x.created_at, reverse=True)
        
        return tasks
    
    def on_sort_changed(self, value):
        """排序选项改变"""
        self.refresh_tasks()
    
    def on_search_changed(self, event=None):
        """搜索内容改变"""
        self.refresh_tasks()
    
    def update_statistics(self):
        """更新统计信息"""
        stats = task_db.get_statistics()
        self.stats_frame.update_statistics(stats)
    
    def show_settings(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self, callback=self.on_settings_changed)
    
    def on_settings_changed(self):
        """设置更改后的回调"""
        try:
            # 重新应用主题
            self.setup_theme()
            
            # 仅重建主布局容器，不销毁当前打开的设置对话框。
            new_layout = normalize_layout(app_config.get("ui_layout", "classic"))
            new_theme = app_config.get("theme", "system")
            new_font_mode = app_config.get("font_mode", "harmony")
            new_font_size = int(app_config.get("font_size", 14))
            new_language = app_config.get("language", "zh-cn")
            if new_layout != getattr(self, "ui_layout", "classic") or (
                (new_layout == "modern" and new_theme != self.current_theme)
                or new_font_mode != self.current_font_mode
                or new_font_size != self.current_font_size
                or new_language != self.current_language
            ):
                self.main_container.destroy()
                self.create_widgets()
            self.current_theme = new_theme
            self.current_font_mode = new_font_mode
            self.current_font_size = new_font_size
            self.current_language = new_language
            self.title(f"{app_config.app_name} - {tr('现代化待办事项管理器', new_language)}")
            self.refresh_tasks()
            localize_tk(self, new_language)

            # 更新窗口大小（如果需要）
            window_size = app_config.get("window_size", "900x700")
            current_geometry = self.geometry()
            current_size = current_geometry.split('+')[0]  # 获取当前窗口大小部分
            if current_size != window_size:
                self.geometry(window_size)
            
            # 更新显示选项
            show_completed = app_config.get("show_completed", True)
            self.show_completed_var.set(show_completed)
            
            # 更新统计面板显示状态
            show_statistics = app_config.get("show_statistics", True)
            if hasattr(self, 'stats_frame'):
                if show_statistics:
                    self.stats_frame.pack(fill="x", padx=10, pady=10)
                else:
                    self.stats_frame.pack_forget()
            
            self.show_status_message("设置已应用")
            
        except Exception as e:
            print(f"应用设置时发生错误: {e}")
            self.show_status_message("设置应用时发生错误")
    
    def clear_completed_tasks(self):
        """清除已完成的任务"""
        if self.localized_messagebox("askyesno", "确认清除", "确定要清除所有已完成的任务吗？"):
            if task_db.clear_completed_tasks():
                self.refresh_tasks()
                self.show_status_message("已清除所有已完成任务")
            else:
                self.localized_messagebox("showerror", "错误", "清除任务失败")
    
    def clear_all_tasks(self):
        """清除所有任务"""
        if self.localized_messagebox("askyesno", "确认清除", "确定要清除所有任务吗？此操作不可恢复！"):
            if task_db.clear_all_tasks():
                self.refresh_tasks()
                self.show_status_message("已清除所有任务")
            else:
                self.localized_messagebox("showerror", "错误", "清除任务失败")
    
    def export_tasks(self):
        """导出任务"""
        try:
            from tkinter import filedialog
            import json
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="导出任务"
            )
            
            if filename:
                tasks = task_db.get_all_tasks()
                export_data = {
                    "app_version": app_config.version,
                    "export_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "tasks": [task.to_dict() for task in tasks]
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                self.show_status_message(f"任务已导出到: {filename}")
        except Exception as e:
            self.localized_messagebox("showerror", "导出失败", f"导出任务时发生错误: {str(e)}")
    
    def show_status_message(self, message: str, duration: int = 3000):
        """显示状态消息"""
        message = tr(message, app_config.get("language", "zh-cn"))
        if getattr(self, "ui_layout", "classic") == "modern" and hasattr(self, "status_label"):
            self.status_label.configure(text=message)
            self.after(duration, lambda: self.status_label.winfo_exists() and
                       self.status_label.configure(text=tr("任务存储在本地 · 与 Flet 版共享数据", app_config.get("language", "zh-cn"))))
        else:
            print(f"状态: {message}")
    
    def start_auto_save(self):
        """启动自动保存"""
        if app_config.get("auto_save", True):
            def auto_save_worker():
                while True:
                    time.sleep(30)  # 每30秒自动保存一次
                    task_db.save_tasks()
            
            auto_save_thread = threading.Thread(target=auto_save_worker, daemon=True)
            auto_save_thread.start()
    
    def on_closing(self):
        """程序关闭时的处理"""
        # 保存当前窗口大小和位置
        geometry = self.geometry()
        app_config.set("window_size", geometry.split('+')[0])
        
        # 保存显示设置
        app_config.set("show_completed", self.show_completed_var.get())
        
        # 最终保存任务
        task_db.save_tasks()
        
        # 关闭程序
        self.destroy()

def main():
    """主函数"""
    try:
        app = TodoApp()
        app.mainloop()
    except Exception as e:
        print(f"程序启动失败: {e}")
        messagebox.showerror("启动错误", f"程序启动失败: {str(e)}")

if __name__ == "__main__":
    main()
