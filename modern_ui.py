"""Tk 现代工作空间布局；与经典布局共用 TodoApp 的任务操作和数据。"""
from __future__ import annotations

import customtkinter as ctk

from config import app_config
from i18n import tr
from ui_components import TaskItem, StatisticsFrame, THEME_TOKENS
from font_preferences import current_font_family, ui_font_size

VIEWS = ("全部任务", "进行中", "已完成")
LAYOUTS = ("classic", "modern")


def normalize_layout(value):
    """旧配置默认沿用经典 UI，未知值安全回退。"""
    return value if value in LAYOUTS else "classic"


def palette():
    """随 CustomTkinter 的深浅主题返回当前模式对应的色板。"""
    idx = 1 if ctk.get_appearance_mode().lower() == "dark" else 0
    return {key: pair[idx] for key, pair in THEME_TOKENS.items()}


def create_modern_widgets(app):
    """构建新版左右分栏；所有数据操作仍调用主程序已有回调。"""
    t = THEME_TOKENS
    font_family = current_font_family(app_config.get("font_mode", "harmony"))
    app.current_view = "全部任务"
    app.nav_buttons = {}

    app.main_container = ctk.CTkFrame(app, fg_color=t["canvas"], corner_radius=0)
    app.main_container.pack(fill="both", expand=True)
    main = app.main_container

    sidebar = ctk.CTkFrame(main, width=216, fg_color=t["sidebar"], corner_radius=0)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # 侧边栏右边界细线
    ctk.CTkFrame(main, width=1, fg_color=t["line"], corner_radius=0).pack(
        side="left", fill="y"
    )

    ctk.CTkLabel(
        sidebar, text="TODOAPP", text_color=t["text"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(18), weight="bold"),
    ).pack(anchor="w", padx=24, pady=(28, 2))
    ctk.CTkLabel(
        sidebar, text="你的个人工作空间", text_color=t["muted"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(11)),
    ).pack(anchor="w", padx=24, pady=(0, 28))

    ctk.CTkLabel(
        sidebar, text="工作空间", text_color=t["muted"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(11), weight="bold"),
    ).pack(anchor="w", padx=24, pady=(0, 10))

    for label in VIEWS:
        button = ctk.CTkButton(
            sidebar, text=label, anchor="w", height=38, corner_radius=9,
            fg_color="transparent", hover_color=t["selected"], text_color=t["text"],
            font=ctk.CTkFont(family=font_family, size=ui_font_size(13)),
            command=lambda name=label: switch_view(app, name),
        )
        button.pack(fill="x", padx=14, pady=2)
        app.nav_buttons[label] = button

    ctk.CTkFrame(sidebar, height=1, fg_color=t["line"], corner_radius=0).pack(
        fill="x", padx=20, pady=(20, 16)
    )
    ctk.CTkButton(
        sidebar, text="应用设置", height=38, anchor="w", corner_radius=9,
        fg_color="transparent", hover_color=t["selected"], text_color=t["text"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(13)),
        command=app.show_settings,
    ).pack(fill="x", padx=14, pady=2)
    ctk.CTkLabel(
        sidebar, text="TodoApp · Tk 0.3.2", text_color=t["muted"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(10)),
    ).pack(side="bottom", anchor="w", padx=24, pady=20)

    workspace = ctk.CTkFrame(main, fg_color=t["canvas"], corner_radius=0)
    workspace.pack(side="left", fill="both", expand=True, padx=28, pady=(22, 16))

    header = ctk.CTkFrame(workspace, fg_color="transparent")
    header.pack(fill="x", pady=(0, 16))
    ctk.CTkLabel(
        header, text="我的工作空间", text_color=t["accent"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(11), weight="bold"),
    ).pack(anchor="w")
    app.view_title = ctk.CTkLabel(
        header, text="全部任务", text_color=t["text"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(26), weight="bold"),
    )
    app.view_title.pack(anchor="w", pady=(3, 2))
    ctk.CTkLabel(
        header, text="整理任务，专注当下。", text_color=t["muted"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(12)),
    ).pack(anchor="w")

    # 搜索、排序、快速新建与经典模式使用同样的事件处理方法。
    tools = ctk.CTkFrame(workspace, fg_color="transparent")
    tools.pack(fill="x", pady=(0, 12))

    app.task_entry = ctk.CTkEntry(
        tools, height=40, width=240, corner_radius=10, border_width=1,
        placeholder_text="输入任务并按回车添加…",
        fg_color=t["input"], border_color=t["line"], text_color=t["text"],
        placeholder_text_color=t["muted"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(13)),
    )
    app.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    app.task_entry.bind("<Return>", app.quick_add_task)

    ctk.CTkButton(
        tools, text="新建任务", width=106, height=40, corner_radius=10,
        fg_color=t["accent"], hover_color=t["accent_hover"],
        text_color=t["on_accent"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(13), weight="bold"),
        command=app.show_add_dialog,
    ).pack(side="right")

    filters = ctk.CTkFrame(workspace, fg_color="transparent")
    filters.pack(fill="x", pady=(0, 12))
    app.show_completed_var = ctk.BooleanVar(
        value=app_config.get("show_completed", True)
    )
    ctk.CTkCheckBox(
        filters, text="显示已完成", variable=app.show_completed_var,
        command=app.refresh_tasks, width=120, corner_radius=6, border_width=2,
        fg_color=t["accent"], hover_color=t["accent_hover"],
        text_color=t["text"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(12)),
    ).pack(side="left")

    app.sort_var = ctk.StringVar(value="创建时间")
    ctk.CTkOptionMenu(
        filters, width=112, height=34, corner_radius=8,
        variable=app.sort_var,
        values=["创建时间", "优先级", "截止日期", "标题", "完成状态"],
        fg_color=t["neutral_btn"], button_color=t["neutral_btn_hover"],
        button_hover_color=t["accent"], text_color=t["text"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(12)),
        command=app.on_sort_changed,
    ).pack(side="right")
    app.search_entry = ctk.CTkEntry(
        filters, width=190, height=34, corner_radius=8, border_width=1,
        placeholder_text="搜索任务…",
        fg_color=t["input"], border_color=t["line"], text_color=t["text"],
        placeholder_text_color=t["muted"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(12)),
    )
    app.search_entry.pack(side="right", padx=(0, 10))
    app.search_entry.bind("<KeyRelease>", app.on_search_changed)

    body = ctk.CTkFrame(workspace, fg_color="transparent")
    body.pack(fill="both", expand=True)

    left = ctk.CTkFrame(
        body, fg_color=t["surface"], border_width=1, border_color=t["line"],
        corner_radius=12,
    )
    left.pack(side="left", fill="both", expand=True, padx=(0, 14))
    ctk.CTkLabel(
        left, text="任务清单", text_color=t["text"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(15), weight="bold"),
    ).pack(anchor="w", padx=18, pady=(14, 6))
    ctk.CTkFrame(left, height=1, fg_color=t["line"], corner_radius=0).pack(
        fill="x", padx=14, pady=(0, 6)
    )
    app.task_list_frame = ctk.CTkScrollableFrame(
        left, fg_color="transparent", scrollbar_button_color=t["line"],
        scrollbar_button_hover_color=t["muted"],
    )
    app.task_list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    right = ctk.CTkFrame(body, width=232, fg_color="transparent")
    right.pack(side="right", fill="y")
    right.pack_propagate(False)
    app.stats_frame = StatisticsFrame(right)
    app.stats_frame.pack(fill="x", pady=(0, 12))
    if not app_config.get("show_statistics", True):
        app.stats_frame.pack_forget()

    actions = ctk.CTkFrame(
        right, fg_color=t["surface"], border_width=1, border_color=t["line"],
        corner_radius=12,
    )
    actions.pack(fill="x")
    ctk.CTkLabel(
        actions, text="快捷操作", text_color=t["text"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(14), weight="bold"),
    ).pack(anchor="w", padx=16, pady=(14, 10))
    for text, action, danger in (
        ("导出任务", app.export_tasks, False),
        ("清除已完成", app.clear_completed_tasks, False),
        ("清除所有任务", app.clear_all_tasks, True),
    ):
        ctk.CTkButton(
            actions, text=text, height=34, anchor="w", corner_radius=8,
            fg_color="transparent",
            hover_color=t["danger_soft"] if danger else t["selected"],
            text_color=t["danger_text"] if danger else t["text"],
            font=ctk.CTkFont(family=font_family, size=ui_font_size(12)),
            command=action,
        ).pack(fill="x", padx=10, pady=(0, 5))
    ctk.CTkFrame(actions, height=6, fg_color="transparent").pack()

    app.status_label = ctk.CTkLabel(
        workspace, text="任务存储在本地 · 与 Flet 版共享数据",
        text_color=t["muted"],
        font=ctk.CTkFont(family=font_family, size=ui_font_size(11)),
    )
    app.status_label.pack(anchor="w", pady=(10, 0))
    switch_view(app, "全部任务", refresh=False)


def switch_view(app, view, refresh=True):
    app.current_view = view if view in VIEWS else "全部任务"
    t = THEME_TOKENS
    font_family = current_font_family(app_config.get("font_mode", "harmony"))
    for name, button in app.nav_buttons.items():
        active = name == app.current_view
        button.configure(
            fg_color=t["selected"] if active else "transparent",
            text_color=t["accent"] if active else t["text"],
            font=ctk.CTkFont(
                family=font_family,
                size=ui_font_size(13),
                weight="bold" if active else "normal",
            ),
        )
    app.view_title.configure(text=tr(app.current_view, app_config.get("language", "zh-cn")))
    if refresh:
        app.refresh_tasks()
