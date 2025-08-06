"""
设置对话框 - Todo App v0.3
完整的应用程序设置界面
"""
import customtkinter as ctk
from tkinter import messagebox, colorchooser, filedialog
from typing import Dict, Any
import json
from config import app_config
from settings_manager import settings_manager

class SettingsDialog(ctk.CTkToplevel):
    """设置对话框"""
    
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        
        self.parent = parent
        self.callback = callback
        self.original_config = app_config.config.copy()
        
        # 设置窗口属性
        self.title("应用设置")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # 设置为模态窗口
        self.transient(parent)
        
        # 居中显示
        self.center_window()
        
        # 创建界面
        self.create_widgets()
        
        # 加载当前设置
        self.load_current_settings()
        
        # 确保窗口完全显示后再设置模态
        self.after(100, self.setup_modal)
    
    def center_window(self):
        """窗口居中显示"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"600x500+{x}+{y}")
    
    def setup_modal(self):
        """设置模态窗口（延迟执行以确保窗口可见）"""
        try:
            self.grab_set()
            self.focus_set()
        except Exception as e:
            print(f"设置模态窗口时发生错误: {e}")
            # 如果grab_set失败，至少确保窗口获得焦点
            try:
                self.focus_set()
            except:
                pass
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ctk.CTkLabel(
            main_frame, 
            text="⚙️ 应用设置", 
            font=("", 20, "bold")
        )
        title_label.pack(pady=(10, 20))
        
        # 创建选项卡
        self.create_tabs(main_frame)
        
        # 底部按钮
        self.create_buttons(main_frame)
    
    def create_tabs(self, parent):
        """创建选项卡"""
        # 选项卡视图
        self.tabview = ctk.CTkTabview(parent, width=550, height=350)
        self.tabview.pack(fill="both", expand=True, pady=(0, 20))
        
        # 外观设置选项卡
        self.create_appearance_tab()
        
        # 行为设置选项卡
        self.create_behavior_tab()
        
        # 颜色设置选项卡
        self.create_color_tab()
        
        # 高级设置选项卡
        self.create_advanced_tab()
    
    def create_appearance_tab(self):
        """创建外观设置选项卡"""
        tab = self.tabview.add("外观")
        
        # 主题设置
        theme_frame = ctk.CTkFrame(tab)
        theme_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(theme_frame, text="主题模式", font=("", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.theme_var = ctk.StringVar(value=app_config.get("theme", "dark"))
        theme_options = [("深色模式", "dark"), ("浅色模式", "light"), ("跟随系统", "system")]
        
        for text, value in theme_options:
            radio = ctk.CTkRadioButton(
                theme_frame,
                text=text,
                variable=self.theme_var,
                value=value,
                command=self.on_theme_changed
            )
            radio.pack(anchor="w", padx=20, pady=2)
        
        # 字体大小设置
        font_frame = ctk.CTkFrame(scroll_frame)
        font_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(font_frame, text="字体大小", font=("", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        font_size_frame = ctk.CTkFrame(font_frame, fg_color="transparent")
        font_size_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.font_size_var = ctk.IntVar(value=app_config.get("font_size", 14))
        self.font_size_slider = ctk.CTkSlider(
            font_size_frame,
            from_=10,
            to=20,
            number_of_steps=10,
            variable=self.font_size_var,
            command=self.on_font_size_changed
        )
        self.font_size_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.font_size_label = ctk.CTkLabel(font_size_frame, text=f"{self.font_size_var.get()}px")
        self.font_size_label.pack(side="right")
        
        # 窗口设置
        window_frame = ctk.CTkFrame(scroll_frame)
        window_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(window_frame, text="窗口设置", font=("", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        # 窗口大小
        size_frame = ctk.CTkFrame(window_frame, fg_color="transparent")
        size_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(size_frame, text="默认窗口大小:").pack(side="left")
        
        current_size = app_config.get("window_size", "900x700")
        width, height = current_size.split('x')
        
        self.width_entry = ctk.CTkEntry(size_frame, width=80, placeholder_text="宽度")
        self.width_entry.pack(side="left", padx=(10, 5))
        self.width_entry.insert(0, width)
        
        ctk.CTkLabel(size_frame, text="×").pack(side="left", padx=5)
        
        self.height_entry = ctk.CTkEntry(size_frame, width=80, placeholder_text="高度")
        self.height_entry.pack(side="left", padx=(5, 10))
        self.height_entry.insert(0, height)
    
    def create_behavior_tab(self):
        """创建行为设置选项卡"""
        tab = self.tabview.add("行为")
        
        # 自动保存设置
        auto_save_frame = ctk.CTkFrame(tab)
        auto_save_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(auto_save_frame, text="自动保存", font=("", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.auto_save_var = ctk.BooleanVar(value=app_config.get("auto_save", True))
        auto_save_cb = ctk.CTkCheckBox(
            auto_save_frame,
            text="启用自动保存（每30秒）",
            variable=self.auto_save_var
        )
        auto_save_cb.pack(anchor="w", padx=20, pady=(0, 10))
        
        # 显示设置
        display_frame = ctk.CTkFrame(scroll_frame)
        display_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(display_frame, text="显示选项", font=("", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.show_completed_var = ctk.BooleanVar(value=app_config.get("show_completed", True))
        show_completed_cb = ctk.CTkCheckBox(
            display_frame,
            text="默认显示已完成任务",
            variable=self.show_completed_var
        )
        show_completed_cb.pack(anchor="w", padx=20, pady=2)
        
        self.show_statistics_var = ctk.BooleanVar(value=app_config.get("show_statistics", True))
        show_stats_cb = ctk.CTkCheckBox(
            display_frame,
            text="显示统计面板",
            variable=self.show_statistics_var
        )
        show_stats_cb.pack(anchor="w", padx=20, pady=2)
        
        self.confirm_delete_var = ctk.BooleanVar(value=app_config.get("confirm_delete", True))
        confirm_delete_cb = ctk.CTkCheckBox(
            display_frame,
            text="删除任务时确认",
            variable=self.confirm_delete_var
        )
        confirm_delete_cb.pack(anchor="w", padx=20, pady=(2, 10))
        
        # 语言设置
        language_frame = ctk.CTkFrame(scroll_frame)
        language_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(language_frame, text="语言设置", font=("", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        lang_frame = ctk.CTkFrame(language_frame, fg_color="transparent")
        lang_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(lang_frame, text="界面语言:").pack(side="left")
        
        self.language_var = ctk.StringVar(value=app_config.get("language", "zh-cn"))
        language_menu = ctk.CTkOptionMenu(
            lang_frame,
            values=["简体中文 (zh-cn)", "English (en)", "繁體中文 (zh-tw)"],
            variable=self.language_var
        )
        language_menu.pack(side="left", padx=(10, 0))
    
    def create_color_tab(self):
        """创建颜色设置选项卡"""
        tab = self.tabview.add("颜色")
        
        # 优先级颜色设置
        priority_frame = ctk.CTkFrame(tab)
        priority_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(priority_frame, text="优先级颜色", font=("", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.priority_colors = app_config.get("priority_colors", {
            "高": "#ff4444",
            "中": "#ffaa00", 
            "低": "#44ff44"
        }).copy()
        
        self.color_buttons = {}
        for priority in ["高", "中", "低"]:
            color_frame = ctk.CTkFrame(priority_frame, fg_color="transparent")
            color_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(color_frame, text=f"{priority}优先级:").pack(side="left", padx=(10, 20))
            
            color_btn = ctk.CTkButton(
                color_frame,
                text="",
                width=40,
                height=30,
                fg_color=self.priority_colors[priority],
                command=lambda p=priority: self.choose_priority_color(p)
            )
            color_btn.pack(side="left", padx=(0, 10))
            self.color_buttons[priority] = color_btn
            
            color_label = ctk.CTkLabel(color_frame, text=self.priority_colors[priority])
            color_label.pack(side="left")
        
        # 重置颜色按钮
        reset_colors_btn = ctk.CTkButton(
            priority_frame,
            text="重置为默认颜色",
            command=self.reset_priority_colors,
            fg_color="gray",
            hover_color="darkgray"
        )
        reset_colors_btn.pack(pady=(10, 15))
    
    def create_advanced_tab(self):
        """创建高级设置选项卡"""
        tab = self.tabview.add("高级")
        
        # 数据管理
        data_frame = ctk.CTkFrame(tab)
        data_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(data_frame, text="数据管理", font=("", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        # 导出设置
        export_btn = ctk.CTkButton(
            data_frame,
            text="导出所有设置",
            command=self.export_settings,
            width=150
        )
        export_btn.pack(anchor="w", padx=20, pady=5)
        
        # 导入设置
        import_btn = ctk.CTkButton(
            data_frame,
            text="导入设置",
            command=self.import_settings,
            width=150
        )
        import_btn.pack(anchor="w", padx=20, pady=5)
        
        # 重置设置
        reset_btn = ctk.CTkButton(
            data_frame,
            text="重置所有设置",
            command=self.reset_all_settings,
            fg_color="red",
            hover_color="darkred",
            width=150
        )
        reset_btn.pack(anchor="w", padx=20, pady=(5, 15))
        
        # 调试信息
        debug_frame = ctk.CTkFrame(scroll_frame)
        debug_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(debug_frame, text="调试信息", font=("", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        # 显示配置文件路径
        config_path_label = ctk.CTkLabel(
            debug_frame,
            text=f"配置文件: {app_config.config_file}",
            font=("", 10),
            text_color="gray"
        )
        config_path_label.pack(anchor="w", padx=20, pady=2)
        
        # 显示任务文件路径
        tasks_path_label = ctk.CTkLabel(
            debug_frame,
            text=f"任务文件: {app_config.tasks_file}",
            font=("", 10),
            text_color="gray"
        )
        tasks_path_label.pack(anchor="w", padx=20, pady=(2, 15))
    
    def create_buttons(self, parent):
        """创建底部按钮"""
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", pady=(0, 10))
        
        # 取消按钮
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="取消",
            command=self.cancel,
            fg_color="gray",
            hover_color="darkgray",
            width=100
        )
        cancel_btn.pack(side="right", padx=(10, 10), pady=10)
        
        # 应用按钮
        apply_btn = ctk.CTkButton(
            button_frame,
            text="应用",
            command=self.apply_settings,
            width=100
        )
        apply_btn.pack(side="right", padx=(0, 5), pady=10)
        
        # 确定按钮
        ok_btn = ctk.CTkButton(
            button_frame,
            text="确定",
            command=self.ok,
            width=100
        )
        ok_btn.pack(side="right", padx=(0, 5), pady=10)
    
    def load_current_settings(self):
        """加载当前设置"""
        # 主题已在创建时设置
        # 字体大小已在创建时设置
        # 其他设置也已在创建时设置
        pass
    
    def on_theme_changed(self):
        """主题改变时的处理"""
        new_theme = self.theme_var.get()
        ctk.set_appearance_mode(new_theme)
    
    def on_font_size_changed(self, value):
        """字体大小改变时的处理"""
        self.font_size_label.configure(text=f"{int(value)}px")
    
    def choose_priority_color(self, priority):
        """选择优先级颜色"""
        current_color = self.priority_colors[priority]
        color = colorchooser.askcolor(
            color=current_color,
            title=f"选择{priority}优先级颜色"
        )
        
        if color[1]:  # 如果用户选择了颜色
            self.priority_colors[priority] = color[1]
            self.color_buttons[priority].configure(fg_color=color[1])
            # 更新颜色标签
            for widget in self.color_buttons[priority].master.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget.cget("text").startswith("#"):
                    widget.configure(text=color[1])
                    break
    
    def reset_priority_colors(self):
        """重置优先级颜色为默认值"""
        default_colors = {
            "高": "#ff4444",
            "中": "#ffaa00", 
            "低": "#44ff44"
        }
        
        for priority, color in default_colors.items():
            self.priority_colors[priority] = color
            self.color_buttons[priority].configure(fg_color=color)
            # 更新颜色标签
            for widget in self.color_buttons[priority].master.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget.cget("text").startswith("#"):
                    widget.configure(text=color)
                    break
    
    def export_settings(self):
        """导出设置"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="导出设置"
        )
        
        if filename:
            success, message = settings_manager.export_settings(filename)
            if success:
                messagebox.showinfo("导出成功", message)
            else:
                messagebox.showerror("导出失败", message)

    def import_settings(self):
        """导入设置"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="导入设置"
        )
        
        if filename:
            success, message, settings_data = settings_manager.import_settings(filename)
            
            if success and settings_data:
                # 确认导入
                if messagebox.askyesno("确认导入", "导入设置将覆盖当前设置，是否继续？"):
                    apply_success, apply_errors = settings_manager.apply_settings(settings_data)
                    if apply_success:
                        messagebox.showinfo("导入成功", "设置已导入，请重启应用程序以应用所有更改")
                        self.destroy()
                    else:
                        error_msg = "应用导入的设置时发生错误:\n" + "\n".join(apply_errors)
                        messagebox.showerror("应用失败", error_msg)
            else:
                messagebox.showerror("导入失败", message)

    def reset_all_settings(self):
        """重置所有设置"""
        if messagebox.askyesno("确认重置", "确定要重置所有设置为默认值吗？此操作不可恢复！"):
            success, message = settings_manager.reset_to_defaults()
            if success:
                messagebox.showinfo("重置完成", f"{message}，请重启应用程序")
                self.destroy()
            else:
                messagebox.showerror("重置失败", message)
    
    def apply_settings(self):
        """应用设置"""
        try:
            # 保存主题设置
            app_config.set("theme", self.theme_var.get())
            
            # 保存字体大小
            app_config.set("font_size", self.font_size_var.get())
            
            # 保存窗口大小
            width = self.width_entry.get().strip()
            height = self.height_entry.get().strip()
            if width.isdigit() and height.isdigit():
                app_config.set("window_size", f"{width}x{height}")
            
            # 保存行为设置
            app_config.set("auto_save", self.auto_save_var.get())
            app_config.set("show_completed", self.show_completed_var.get())
            app_config.set("show_statistics", self.show_statistics_var.get())
            app_config.set("confirm_delete", self.confirm_delete_var.get())
            
            # 保存语言设置
            lang_mapping = {
                "简体中文 (zh-cn)": "zh-cn",
                "English (en)": "en",
                "繁體中文 (zh-tw)": "zh-tw"
            }
            selected_lang = self.language_var.get()
            if selected_lang in lang_mapping:
                app_config.set("language", lang_mapping[selected_lang])
            
            # 保存优先级颜色
            app_config.set("priority_colors", self.priority_colors)
            
            # 通知父窗口设置已更改
            if self.callback:
                self.callback()
            
            messagebox.showinfo("设置已保存", "设置已成功保存")
            
        except Exception as e:
            messagebox.showerror("保存失败", f"保存设置时发生错误: {str(e)}")
    
    def ok(self):
        """确定按钮处理"""
        self.apply_settings()
        self.destroy()
    
    def cancel(self):
        """取消按钮处理"""
        # 恢复原始主题
        original_theme = self.original_config.get("theme", "dark")
        ctk.set_appearance_mode(original_theme)
        self.destroy()