"""Tk 现代工作空间布局；与经典布局共用 TodoApp 的任务操作和数据。"""
from __future__ import annotations

import customtkinter as ctk

from config import app_config
from ui_components import TaskItem, StatisticsFrame
from font_preferences import current_font_family

VIEWS = ("全部任务", "进行中", "已完成")
LAYOUTS = ("classic", "modern")


def normalize_layout(value):
    """旧配置默认沿用经典 UI，未知值安全回退。"""
    return value if value in LAYOUTS else "classic"


def palette():
    """随 CustomTkinter 的深浅主题切换工作空间表面。"""
    if ctk.get_appearance_mode().lower() == "dark":
        return dict(canvas="#14171C", sidebar="#1C222A", surface="#222A34",
                    text="#F2F4F7", muted="#9BA7B7", accent="#8FAFE8",
                    selected="#303D4E", line="#35404D")
    return dict(canvas="#F5F7F9", sidebar="#E9EEF3", surface="#FFFFFF",
                text="#1E2936", muted="#66788C", accent="#416C9D",
                selected="#D6E3F0", line="#D9E1E8")


def create_modern_widgets(app):
    """构建新版左右分栏；所有数据操作仍调用主程序已有回调。"""
    c = palette()
    app.current_view = "全部任务"
    app.nav_buttons = {}

    app.main_container = ctk.CTkFrame(app, fg_color=c["canvas"], corner_radius=0)
    app.main_container.pack(fill="both", expand=True)
    main = app.main_container

    sidebar = ctk.CTkFrame(main, width=214, fg_color=c["sidebar"], corner_radius=0)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    ctk.CTkLabel(sidebar, text="TODOAPP", text_color=c["text"],
                 font=ctk.CTkFont(family=current_font_family(app_config.get("font_mode", "harmony")), size=19, weight="bold")).pack(anchor="w", padx=26, pady=(34, 4))
    ctk.CTkLabel(sidebar, text="你的个人工作空间", text_color=c["muted"],
                 font=ctk.CTkFont(family=current_font_family(app_config.get("font_mode", "harmony")), size=11)).pack(anchor="w", padx=26, pady=(0, 37))

    ctk.CTkLabel(sidebar, text="工作空间", text_color=c["muted"],
                 font=ctk.CTkFont(family=current_font_family(app_config.get("font_mode", "harmony")), size=11, weight="bold")).pack(anchor="w", padx=26, pady=(0, 14))

    for label in VIEWS:
        button = ctk.CTkButton(
            sidebar, text=label, anchor="w", height=39, corner_radius=8,
            fg_color="transparent", hover_color=c["selected"], text_color=c["text"],
            font=ctk.CTkFont(family=current_font_family(app_config.get("font_mode", "harmony")), size=13),
            command=lambda name=label: switch_view(app, name),
        )
        button.pack(fill="x", padx=15, pady=3)
        app.nav_buttons[label] = button

    ctk.CTkLabel(sidebar, text="────────────────", text_color=c["line"]).pack(
        padx=24, pady=(24, 18))
    ctk.CTkButton(sidebar, text="应用设置", height=38, anchor="w",
                  fg_color="transparent", hover_color=c["selected"],
                  text_color=c["text"], command=app.show_settings).pack(
                      fill="x", padx=15, pady=3)
    ctk.CTkLabel(sidebar, text="TodoApp · Tk 0.3.2", text_color=c["muted"],
                 font=ctk.CTkFont(family=current_font_family(app_config.get("font_mode", "harmony")), size=10)).pack(side="bottom", anchor="w",
                                                 padx=26, pady=23)

    workspace = ctk.CTkFrame(main, fg_color=c["canvas"], corner_radius=0)
    workspace.pack(side="left", fill="both", expand=True, padx=34, pady=30)

    header = ctk.CTkFrame(workspace, fg_color="transparent")
    header.pack(fill="x", pady=(0, 26))
    ctk.CTkLabel(header, text="我的工作空间", text_color=c["accent"],
                 font=ctk.CTkFont(family=current_font_family(app_config.get("font_mode", "harmony")), size=12, weight="bold")).pack(anchor="w")
    app.view_title = ctk.CTkLabel(header, text="全部任务", text_color=c["text"],
                                  font=ctk.CTkFont(family=current_font_family(app_config.get("font_mode", "harmony")), size=28, weight="bold"))
    app.view_title.pack(anchor="w", pady=(5, 3))
    ctk.CTkLabel(header, text="整理任务，专注当下。", text_color=c["muted"],
                 font=ctk.CTkFont(family=current_font_family(app_config.get("font_mode", "harmony")), size=12)).pack(anchor="w")

    # 搜索、排序、快速新建与经典模式使用同样的事件处理方法。
    tools = ctk.CTkFrame(workspace, fg_color="transparent")
    tools.pack(fill="x", pady=(0, 18))

    app.task_entry = ctk.CTkEntry(
        tools, height=41, width=240, placeholder_text="输入任务并按回车添加…",
        fg_color=c["surface"], border_color=c["line"])
    app.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 9))
    app.task_entry.bind("<Return>", app.quick_add_task)

    ctk.CTkButton(tools, text="新建任务", width=102, height=41,
                  fg_color=c["accent"], text_color="#111923",
                  command=app.show_add_dialog).pack(side="right")

    filters = ctk.CTkFrame(workspace, fg_color="transparent")
    filters.pack(fill="x", pady=(0, 13))
    app.show_completed_var = ctk.BooleanVar(
        value=app_config.get("show_completed", True))
    ctk.CTkCheckBox(filters, text="显示已完成", variable=app.show_completed_var,
                    command=app.refresh_tasks, width=120).pack(side="left")

    app.sort_var = ctk.StringVar(value="创建时间")
    ctk.CTkOptionMenu(filters, width=104, variable=app.sort_var,
                      values=["创建时间", "优先级", "截止日期", "标题", "完成状态"],
                      command=app.on_sort_changed).pack(side="right")
    app.search_entry = ctk.CTkEntry(filters, width=175, height=33,
                                    placeholder_text="搜索任务…",
                                    fg_color=c["surface"], border_color=c["line"])
    app.search_entry.pack(side="right", padx=(0, 10))
    app.search_entry.bind("<KeyRelease>", app.on_search_changed)

    body = ctk.CTkFrame(workspace, fg_color="transparent")
    body.pack(fill="both", expand=True)

    left = ctk.CTkFrame(body, fg_color=c["surface"], corner_radius=12)
    left.pack(side="left", fill="both", expand=True, padx=(0, 15))
    ctk.CTkLabel(left, text="任务清单", text_color=c["text"],
                 font=ctk.CTkFont(family=current_font_family(app_config.get("font_mode", "harmony")), size=15, weight="bold")).pack(
                     anchor="w", padx=20, pady=(19, 9))
    app.task_list_frame = ctk.CTkScrollableFrame(left, fg_color="transparent")
    app.task_list_frame.pack(fill="both", expand=True, padx=12, pady=(0, 13))

    right = ctk.CTkFrame(body, width=225, fg_color="transparent")
    right.pack(side="right", fill="y")
    right.pack_propagate(False)
    app.stats_frame = StatisticsFrame(right)
    app.stats_frame.pack(fill="x", pady=(0, 14))
    if not app_config.get("show_statistics", True):
        app.stats_frame.pack_forget()

    actions = ctk.CTkFrame(right, fg_color=c["surface"], corner_radius=12)
    actions.pack(fill="x")
    ctk.CTkLabel(actions, text="快捷操作", text_color=c["text"],
                 font=ctk.CTkFont(family=current_font_family(app_config.get("font_mode", "harmony")), size=15, weight="bold")).pack(
                     anchor="w", padx=16, pady=(17, 12))
    for text, action in (
        ("导出任务", app.export_tasks),
        ("清除已完成", app.clear_completed_tasks),
        ("清除所有任务", app.clear_all_tasks),
    ):
        ctk.CTkButton(actions, text=text, height=34, anchor="w",
                      fg_color="transparent", hover_color=c["selected"],
                      text_color=c["text"], command=action).pack(
                          fill="x", padx=12, pady=(0, 7))
    ctk.CTkFrame(actions, height=8, fg_color="transparent").pack()

    app.status_label = ctk.CTkLabel(
        workspace, text="任务存储在本地 · 与 Flet 版共享数据",
        text_color=c["muted"], font=ctk.CTkFont(family=current_font_family(app_config.get("font_mode", "harmony")), size=11))
    app.status_label.pack(anchor="w", pady=(15, 0))
    switch_view(app, "全部任务", refresh=False)


def switch_view(app, view, refresh=True):
    app.current_view = view if view in VIEWS else "全部任务"
    c = palette()
    for name, button in app.nav_buttons.items():
        button.configure(fg_color=c["selected"] if name == app.current_view else "transparent")
    app.view_title.configure(text=app.current_view)
    if refresh:
        app.refresh_tasks()
