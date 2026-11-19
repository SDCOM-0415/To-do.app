"""Todo App 0.3.1 Flet desktop edition.

The Tkinter UI remains untouched. This prototype reuses the existing Task
dataclass and JSON schema while writing to per-user application storage.
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

import flet as ft

from models import Task
from task_operations import pop_task_by_id
from date_input import format_date_input, parse_date_input
import storage
from settings_ui import show_settings
from appearance import appearance, normalize_theme
from font_preferences import font_family, register_flet_fonts, scaled_font_size
from window_chrome import configure_window, with_titlebar, update_titlebar_theme, SIDEBAR_WIDTH
from localize_flet import localize_flet
from i18n import tr, normalize_language


def main(page: ft.Page) -> None:
    page.title = "TodoApp Flet 0.3.2"
    page.padding = 0
    page.spacing = 0
    page.locale_configuration = ft.LocaleConfiguration(
        current_locale=ft.Locale("zh", "Hans"),
        supported_locales=[ft.Locale("zh", "Hans"), ft.Locale("en", "US")],
    )
    picker = ft.FilePicker()
    page.services.append(picker)
    page.window.width = 1100
    page.window.height = 760
    page.window.min_width = 750
    page.window.min_height = 540
    configure_window(page)

    dirty = False
    try:
        tasks = storage.load_tasks()
        settings = storage.load_settings()
    except Exception as exc:
        page.add(ft.Text(f"无法读取任务数据：{exc}", color=ft.Colors.RED_400))
        page.add(ft.Text(f"数据目录：{storage.APP_DIR}"))
        return

    register_flet_fonts(page)
    settings["language"] = normalize_language(settings.get("language"))
    page.locale_configuration = ft.LocaleConfiguration(
        current_locale=ft.Locale("en", "US") if settings["language"] == "en"
            else ft.Locale("zh", "TW") if settings["language"] == "zh-tw"
            else ft.Locale("zh", "CN"),
        supported_locales=[ft.Locale("zh", "CN"), ft.Locale("zh", "TW"), ft.Locale("en", "US")],
    )

    theme_surfaces: list[tuple[ft.Container, str]] = []
    theme_borders: list[tuple[ft.Container, str]] = []
    theme_dividers: list[ft.Divider] = []
    theme_texts: list[tuple[ft.Text, str]] = []
    primary_buttons: list[ft.Button] = []
    brand_badge: ft.Container | None = None
    brand_icon: ft.Icon | None = None
    title_surface: ft.Container | None = None
    colors = appearance(settings.get("theme"))

    def primary_button_style(c: dict) -> ft.ButtonStyle:
        return ft.ButtonStyle(
            bgcolor=c["accent"],
            color=c["on_accent"],
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        )

    def apply_theme() -> None:
        nonlocal colors
        settings["theme"] = normalize_theme(settings.get("theme"))
        colors = appearance(settings["theme"])
        page.theme_mode = colors["mode"]
        # 两套主题必须同步设置字体与文本主色：深色模式优先使用 dark_theme，
        # 浅色模式显式绑定 on_surface 颜色，避免部分 Linux 环境下浅色主题退化为白字。
        family = font_family(settings.get("font_mode"))
        preferred_size = int(settings.get("font_size", 14))
        text_color = colors["text"]
        text_theme = ft.TextTheme(
            body_small=ft.TextStyle(size=scaled_font_size(12, preferred_size), color=text_color),
            body_medium=ft.TextStyle(size=scaled_font_size(14, preferred_size), color=text_color),
            body_large=ft.TextStyle(size=scaled_font_size(16, preferred_size), color=text_color),
            label_small=ft.TextStyle(size=scaled_font_size(11, preferred_size), color=text_color),
            label_medium=ft.TextStyle(size=scaled_font_size(12, preferred_size), color=text_color),
            label_large=ft.TextStyle(size=scaled_font_size(14, preferred_size), color=text_color),
            title_small=ft.TextStyle(size=scaled_font_size(14, preferred_size), color=text_color),
            title_medium=ft.TextStyle(size=scaled_font_size(16, preferred_size), color=text_color),
            title_large=ft.TextStyle(size=scaled_font_size(22, preferred_size), color=text_color),
        )
        theme_obj = ft.Theme(
            color_scheme_seed=colors["accent"],
            font_family=family,
            text_theme=text_theme,
        )
        page.theme = theme_obj
        page.dark_theme = theme_obj
        page.bgcolor = colors["canvas"]
        page.window.bgcolor = colors["sidebar"]
        for surface, token in theme_surfaces:
            surface.bgcolor = colors[token]
        for container, side in theme_borders:
            if side == "all":
                container.border = ft.Border.all(1, colors["divider"])
            elif side == "right":
                container.border = ft.Border(right=ft.BorderSide(1, colors["divider"]))
        for divider in theme_dividers:
            divider.color = colors["divider"]
        for label_ctrl, token in theme_texts:
            label_ctrl.color = colors[token]
        for btn in primary_buttons:
            btn.style = primary_button_style(colors)
        if brand_badge is not None:
            brand_badge.bgcolor = colors["accent"]
        if brand_icon is not None:
            brand_icon.color = colors["on_accent"]
        if "search" in locals_ref:
            s_ctrl = locals_ref["search"]
            s_ctrl.bgcolor = colors["surface"]
            s_ctrl.border_color = colors["divider"]
            s_ctrl.focused_border_color = colors["accent"]
            s_ctrl.text_style = ft.TextStyle(color=colors["text"])
            s_ctrl.hint_style = ft.TextStyle(color=colors["muted"])
        if "quick" in locals_ref:
            q_ctrl = locals_ref["quick"]
            q_ctrl.text_style = ft.TextStyle(color=colors["text"])
            q_ctrl.hint_style = ft.TextStyle(color=colors["muted"])
        if "sort" in locals_ref:
            sort_ctrl = locals_ref["sort"]
            sort_ctrl.fill_color = colors["surface"]
            sort_ctrl.border_color = colors["divider"]
            sort_ctrl.focused_border_color = colors["accent"]
            sort_ctrl.text_style = ft.TextStyle(color=colors["text"])
            sort_ctrl.label_style = ft.TextStyle(color=colors["muted"])
        if "show_completed" in locals_ref:
            cb_ctrl = locals_ref["show_completed"]
            cb_ctrl.label_style = ft.TextStyle(color=colors["text"])
            cb_ctrl.active_color = colors["accent"]
            cb_ctrl.check_color = colors["on_accent"]
        if title_surface is not None:
            update_titlebar_theme(title_surface, settings["theme"])
        try:
            width_value, height_value = settings.get("window_size", "900x700").split("x", 1)
            page.window.width = int(width_value)
            page.window.height = int(height_value)
        except (ValueError, TypeError):
            pass

    locals_ref: dict[str, object] = {}
    apply_theme()

    search = ft.TextField(
        hint_text="搜索任务和备注...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        filled=True,
        bgcolor=colors["surface"],
        border_radius=10,
        border_color=colors["divider"],
        focused_border_color=colors["accent"],
        text_style=ft.TextStyle(color=colors["text"]),
        hint_style=ft.TextStyle(color=colors["muted"]),
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        dense=True,
        on_change=lambda e: refresh(),
    )
    quick = ft.TextField(
        hint_text="输入任务，按回车创建",
        expand=True,
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(color=colors["text"]),
        hint_style=ft.TextStyle(color=colors["muted"]),
        content_padding=ft.Padding.symmetric(horizontal=4, vertical=8),
        on_submit=lambda e: quick_add(),
    )
    show_completed = ft.Checkbox(
        label="显示已完成",
        value=bool(settings["show_completed"]),
        active_color=colors["accent"],
        check_color=colors["on_accent"],
        label_style=ft.TextStyle(color=colors["text"]),
        on_change=lambda e: change_setting("show_completed", bool(e.control.value)),
    )
    sort = ft.Dropdown(
        width=176,
        label="排序",
        value=str(settings.get("sort", "created_at")),
        filled=True,
        fill_color=colors["surface"],
        border_radius=10,
        border_color=colors["divider"],
        focused_border_color=colors["accent"],
        text_style=ft.TextStyle(color=colors["text"]),
        label_style=ft.TextStyle(color=colors["muted"]),
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        dense=True,
        options=[
            ft.DropdownOption(key="created_at", text="创建时间"),
            ft.DropdownOption(key="priority", text="优先级"),
            ft.DropdownOption(key="due_date", text="截止日期"),
            ft.DropdownOption(key="title", text="标题"),
            ft.DropdownOption(key="completed", text="完成状态"),
        ],
        on_select=lambda e: change_setting("sort", e.control.value),
    )
    locals_ref.update({"search": search, "quick": quick, "sort": sort, "show_completed": show_completed})
    stats = ft.Text(size=scaled_font_size(12, settings.get("font_size", 14)), color=colors["muted"])
    theme_texts.append((stats, "muted"))
    task_list = ft.ListView(expand=True, spacing=8, padding=ft.Padding.only(top=4, bottom=12))
    view_mode = "all"
    view_title = ft.Text(
        "全部任务",
        size=scaled_font_size(26, settings.get("font_size", 14)),
        weight=ft.FontWeight.BOLD,
        color=colors["text"],
    )
    theme_texts.append((view_title, "text"))
    nav_widgets: dict[str, ft.Container] = {}


    def show_localized_dialog(dialog) -> None:
        localize_flet(dialog, settings.get("language", "zh-cn"))
        page.show_dialog(dialog)

    def message(text: str) -> None:
        text = tr(text, settings.get("language", "zh-cn"))
        # 避免 Paper & Ink 等浅色主题出现默认的深灰色整宽提示条。
        c = appearance(settings.get("theme"))
        show_localized_dialog(ft.SnackBar(
            content=ft.Text(text, color=c["text"]),
            bgcolor=c["surface"],
            behavior=ft.SnackBarBehavior.FLOATING,
            width=300,
        ))

    def save(force: bool = False) -> bool:
        nonlocal dirty
        if not settings.get("auto_save", True) and not force:
            dirty = True
            return True
        try:
            storage.save_tasks(tasks)
            dirty = False
            return True
        except Exception as exc:
            message(f"保存失败：{exc}")
            return False

    def change_setting(name: str, value: object) -> None:
        settings[name] = normalize_theme(value) if name == "theme" else value
        if name == "theme":
            apply_theme()
        try:
            storage.save_settings(settings)
        except Exception as exc:
            message(f"无法保存设置：{exc}")
        refresh()

    def manual_save(e=None) -> None:
        if save(force=True):
            message("任务已保存")

    def quick_add() -> None:
        title = (quick.value or "").strip()
        if not title:
            return
        candidate = Task(id="", title=title)
        tasks.append(candidate)
        if not save():
            tasks.remove(candidate)
            return
        quick.value = ""
        refresh()

    def remove_task(task: Task) -> None:
        # 保存任务 ID，而不是依赖可能失效的界面对象引用。
        task_id = task.id

        def do_delete(e) -> None:
            # 重复确认、旧界面事件以及导入/清空后的过期回调都可能触发这里。
            # 删除应当是幂等操作，不得因对象不在列表中而崩溃。
            removed_entry = pop_task_by_id(tasks, task_id)
            if removed_entry is None:
                return
            index, removed = removed_entry
            if e is not None:
                page.pop_dialog()
            if not save():
                tasks.insert(index, removed)
            refresh()

        if not settings.get("confirm_delete", True):
            do_delete(None)
            return
        show_localized_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("删除任务？"),
            content=ft.Text(f"确定删除「{task.title}」吗？"),
            actions=[
                ft.TextButton("取消", on_click=lambda e: page.pop_dialog()),
                ft.Button("删除", on_click=do_delete),
            ],
        ))

    def clear_completed(e) -> None:
        completed = [t for t in tasks if t.completed]
        if not completed:
            message("暂无已完成任务")
            return

        def confirm(e) -> None:
            page.pop_dialog()
            before = tasks[:]
            tasks[:] = [t for t in tasks if not t.completed]
            if not save():
                tasks[:] = before
            refresh()

        show_localized_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("清除已完成任务"),
            content=ft.Text(f"确定删除 {len(completed)} 项已完成任务吗？"),
            actions=[
                ft.TextButton("取消", on_click=lambda e: page.pop_dialog()),
                ft.Button("确认清除", on_click=confirm),
            ],
        ))

    def edit_task(task: Task | None = None) -> None:
        editing = task is not None
        title = ft.TextField(label="任务名称", value=task.title if task else "", autofocus=True)
        description = ft.TextField(
            label="备注", value=task.description if task else "",
            multiline=True, min_lines=2, max_lines=4,
        )
        priority = ft.Dropdown(
            label="优先级", value=task.priority if task else "中",
            options=[ft.DropdownOption(key=p, text=p) for p in ("高", "中", "低")],
        )
        due = ft.TextField(
            label=tr("截止日期（YYYY/MM/DD，可留空）", settings.get("language")),
            hint_text=tr("例如 2026/11/11，输入数字自动补 /", settings.get("language")),
            value=format_date_input(task.due_date or "") if task else "",
            expand=True,
        )

        def format_due(e) -> None:
            formatted = format_date_input(e.control.value or "")
            if e.control.value != formatted:
                e.control.value = formatted
                e.control.update()

        def set_due_from_calendar(e) -> None:
            if e.control.value is not None:
                due.value = e.control.value.strftime("%Y/%m/%d")
                due.update()

        date_picker = ft.DatePicker(
            on_change=set_due_from_calendar,
            locale=ft.Locale("en", "US") if settings.get("language") == "en"
                else ft.Locale("zh", "TW") if settings.get("language") == "zh-tw"
                else ft.Locale("zh", "CN"),
            help_text=tr("选择截止日期", settings.get("language")),
            confirm_text=tr("确定", settings.get("language")),
            cancel_text=tr("取消", settings.get("language")),
            field_label_text=tr("截止日期", settings.get("language")),
            field_hint_text="YYYY/MM/DD",
            error_format_text={
                "en": "Invalid date format",
                "zh-tw": "日期格式不正確",
            }.get(settings.get("language"), "日期格式不正确"),
            error_invalid_text={
                "en": "Date outside the allowed range",
                "zh-tw": "日期超出允許範圍",
            }.get(settings.get("language"), "日期超出允许范围"),
            first_date=datetime(1900, 1, 1),
            last_date=datetime(2100, 12, 31),
        )

        def open_date_picker(e) -> None:
            try:
                selected = parse_date_input(due.value or "")
            except ValueError:
                selected = None
            if selected:
                date_picker.value = datetime.combine(selected, datetime.min.time())
            show_localized_dialog(date_picker)

        due.on_change = format_due
        due_row = ft.Row(
            controls=[
                due,
                ft.IconButton(
                    icon=ft.Icons.CALENDAR_MONTH,
                    tooltip="打开日期选择器",
                    on_click=open_date_picker,
                ),
            ],
            spacing=4,
        )
        tags = ft.TextField(
            label=tr("标签（逗号分隔）", settings.get("language")),
            value=", ".join(task.tags or []) if task else "",
        )
        error = ft.Text("", color=ft.Colors.RED_400, size=scaled_font_size(12, settings.get("font_size", 14)))

        def submit(e) -> None:
            name = (title.value or "").strip()
            if not name:
                error.value = tr("请填写任务名称", settings.get("language"))
                error.update()
                return
            try:
                parsed_due = parse_date_input(due.value or "")
            except ValueError:
                error.value = tr("请输入有效日期（YYYY/MM/DD）", settings.get("language"))
                error.update()
                return
            due_value = parsed_due.isoformat() if parsed_due else None
            changes = {
                "title": name,
                "description": description.value or "",
                "priority": priority.value or "中",
                "due_date": due_value,
                "tags": [item.strip() for item in (tags.value or "").split(",") if item.strip()],
            }
            if editing:
                original = task.to_dict()
                task.update(**changes)
                if not save():
                    tasks[tasks.index(task)] = Task.from_dict(original)
                    return
            else:
                candidate = Task(id="", **changes)
                tasks.append(candidate)
                if not save():
                    tasks.remove(candidate)
                    return
            page.pop_dialog()
            refresh()

        show_localized_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("编辑任务" if editing else "添加任务"),
            content=ft.Container(
                width=410,
                content=ft.Column(
                    controls=[title, description, priority, due_row, tags, error],
                    spacing=12,
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
            actions=[
                ft.TextButton("取消", on_click=lambda e: page.pop_dialog()),
                ft.Button("保存", icon=ft.Icons.CHECK, on_click=submit),
            ],
        ))

    def toggle_task(task: Task, checked: bool) -> None:
        previous = task.completed
        task.toggle_completed()
        task.completed = checked
        if not save():
            task.completed = previous
        refresh()

    def user_text(value: str, **kwargs) -> ft.Text:
        """Never translate user-created task titles, notes or tags."""
        control = ft.Text(value, **kwargs)
        control._i18n_skip = True
        return control

    def card(task: Task) -> ft.Control:
        tint = {
            "高": ft.Colors.RED_400,
            "中": ft.Colors.AMBER_600,
            "低": ft.Colors.GREEN_500,
        }.get(task.priority, ft.Colors.BLUE_400)
        tint = settings.get("priority_colors", {}).get(task.priority, tint)
        lang = settings.get("language", "zh-cn")
        font_sz = settings.get("font_size", 14)
        priority_label = tr(f"{task.priority}优先级", lang)
        meta_controls: list[ft.Control] = [
            ft.Text(
                f"● {priority_label}",
                color=tint,
                size=scaled_font_size(11, font_sz),
                weight=ft.FontWeight.W_500,
            ),
        ]
        if task.due_date:
            overdue = task.is_overdue()
            meta_controls.append(
                user_text(
                    f"{tr('截止', lang)} {task.due_date}",
                    size=scaled_font_size(11, font_sz),
                    color=colors["danger"] if overdue else colors["muted"],
                    weight=ft.FontWeight.W_600 if overdue else ft.FontWeight.NORMAL,
                )
            )
        for tag in (task.tags or []):
            meta_controls.append(
                ft.Container(
                    bgcolor=colors["sidebar"],
                    border_radius=6,
                    padding=ft.Padding.symmetric(horizontal=7, vertical=2),
                    content=user_text(
                        tag,
                        size=scaled_font_size(10, font_sz),
                        color=colors["muted"],
                    ),
                )
            )

        title_control = user_text(
            task.title,
            size=scaled_font_size(14, font_sz),
            weight=ft.FontWeight.W_600,
            color=colors["muted"] if task.completed else colors["text"],
            style=(
                ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)
                if task.completed else None
            ),
        )
        return ft.Container(
            bgcolor=colors["surface"],
            border_radius=12,
            border=ft.Border.all(1, colors["divider"]),
            padding=ft.Padding.symmetric(horizontal=14, vertical=11),
            content=ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=4,
                        height=38,
                        border_radius=2,
                        bgcolor=tint,
                    ),
                    ft.Checkbox(
                        value=task.completed,
                        active_color=colors["accent"],
                        check_color=colors["on_accent"],
                        on_change=lambda e, item=task: toggle_task(item, bool(e.control.value)),
                    ),
                    ft.Column(
                        expand=True,
                        spacing=5,
                        controls=[
                            title_control,
                            ft.Row(
                                spacing=8,
                                run_spacing=4,
                                wrap=True,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=meta_controls,
                            ),
                            *([user_text(
                                task.description,
                                size=scaled_font_size(12, font_sz),
                                color=colors["muted"],
                            )] if task.description else []),
                        ],
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT_OUTLINED,
                        tooltip="编辑任务",
                        icon_size=18,
                        icon_color=colors["muted"],
                        on_click=lambda e, item=task: edit_task(item),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        tooltip="删除任务",
                        icon_size=18,
                        icon_color=colors["danger"],
                        on_click=lambda e, item=task: remove_task(item),
                    ),
                ],
            ),
        )

    def change_view(target: str) -> None:
        nonlocal view_mode
        view_mode = target
        view_title.value = {
            "all": "全部任务", "active": "进行中", "done": "已完成",
        }[target]
        refresh()

    nav_parts: dict[str, tuple[ft.Icon, ft.Text]] = {}

    def nav_button(title: str, icon: str, target: str) -> ft.Container:
        icon_ctrl = ft.Icon(
            icon,
            size=scaled_font_size(18, settings.get("font_size", 14)),
            color=colors["text"],
        )
        text_ctrl = ft.Text(
            title,
            size=scaled_font_size(13, settings.get("font_size", 14)),
            weight=ft.FontWeight.W_500,
            color=colors["text"],
        )
        button = ft.Container(
            border_radius=10,
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            on_click=lambda e: change_view(target),
            ink=True,
            content=ft.Row([icon_ctrl, text_ctrl], spacing=11),
        )
        nav_widgets[target] = button
        nav_parts[target] = (icon_ctrl, text_ctrl)
        return button

    def visible_tasks() -> list[Task]:
        query = (search.value or "").lower().strip()
        rows = [
            t for t in tasks
            if (settings.get("show_completed", True) or not t.completed or view_mode == "done")
            and (view_mode == "all"
                 or (view_mode == "active" and not t.completed)
                 or (view_mode == "done" and t.completed))
            and (not query or query in t.title.lower()
                 or query in (t.description or "").lower()
                 or any(query in tag.lower() for tag in (t.tags or [])))
        ]
        order = settings.get("sort", "created_at")
        if order == "priority":
            return sorted(rows, key=lambda t: -t.get_priority_weight())
        if order == "due_date":
            return sorted(rows, key=lambda t: t.due_date or "9999-12-31")
        if order == "title":
            return sorted(rows, key=lambda t: t.title.casefold())
        if order == "completed":
            return sorted(rows, key=lambda t: t.completed)
        return sorted(rows, key=lambda t: t.created_at, reverse=True)

    def refresh() -> None:
        complete = sum(1 for t in tasks if t.completed)
        overdue = sum(1 for t in tasks if t.is_overdue())
        stats.value = (f"总计 {len(tasks)} 项  ·  已完成 {complete}  ·  "
                       f"进行中 {len(tasks) - complete}  ·  逾期 {overdue}")
        stats.visible = bool(settings.get("show_statistics", True))
        for key, button in nav_widgets.items():
            active = key == view_mode
            button.bgcolor = (colors["selected"]
                              if active else ft.Colors.TRANSPARENT)
            icon_ctrl, text_ctrl = nav_parts[key]
            icon_ctrl.color = colors["accent"] if active else colors["muted"]
            text_ctrl.color = colors["text"]
            text_ctrl.weight = ft.FontWeight.W_600 if active else ft.FontWeight.W_500
        rows = visible_tasks()
        task_list.controls = [card(t) for t in rows] if rows else [
            ft.Container(
                padding=36,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                    controls=[
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE_OUTLINE,
                            size=scaled_font_size(42, settings.get("font_size", 14)),
                            color=colors["accent"],
                        ),
                        ft.Text(
                            "这里暂时没有任务",
                            size=scaled_font_size(16, settings.get("font_size", 14)),
                            weight=ft.FontWeight.W_600,
                            color=colors["text"],
                        ),
                        ft.Text(
                            "添加一条待办，或调整筛选条件",
                            color=colors["muted"],
                            size=scaled_font_size(13, settings.get("font_size", 14)),
                        ),
                    ],
                ),
            ),
        ]
        # Newly generated task cards and counters must respect the selected locale.
        language = settings.get("language", "zh-cn")
        localize_flet(task_list, language)
        localize_flet(stats, language)
        localize_flet(view_title, language)
        # 更新 Flet 的原生控件树，否则要等切换页面后才看到新任务。
        page.update()

    async def export_tasks(e) -> None:
        payload = json.dumps([t.to_dict() for t in tasks], ensure_ascii=False, indent=2).encode("utf-8")
        try:
            path = await picker.save_file(
                dialog_title=tr("导出待办任务", settings.get("language")), file_name="todo-tasks.json",
                file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["json"],
                src_bytes=payload,
            )
            if path:
                message(f"已导出：{path}")
        except Exception as exc:
            message(f"导出失败：{exc}")

    async def import_tasks(e) -> None:
        try:
            files = await picker.pick_files(
                dialog_title=tr("导入待办任务", settings.get("language")),
                allow_multiple=False,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["json"],
                with_data=True,
            )
            if not files:
                return
            selected = files[0]
            data = selected.bytes if selected.bytes is not None else Path(selected.path).read_bytes()
            payload = json.loads(data.decode("utf-8-sig"))
            if not isinstance(payload, list):
                raise ValueError("任务数据必须是 JSON 数组")
            imported = [Task.from_dict(dict(item)) for item in payload]
        except Exception as exc:
            message(f"导入失败：{exc}")
            return

        def confirm(e) -> None:
            page.pop_dialog()
            backup = tasks[:]
            tasks[:] = imported
            if not save():
                tasks[:] = backup
                return
            refresh()
            message(f"已导入 {len(imported)} 条任务")

        show_localized_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("确认导入"),
            content=ft.Text(f"导入 {len(imported)} 条任务将替换当前全部 {len(tasks)} 条任务。确定吗？"),
            actions=[
                ft.TextButton("取消", on_click=lambda e: page.pop_dialog()),
                ft.Button("确认导入", on_click=confirm),
            ],
        ))

    def on_settings_changed() -> None:
        # Settings update includes language; translate the existing workspace
        # rather than recreating widgets and losing input state.
        apply_theme()
        settings["language"] = normalize_language(settings.get("language"))
        page.locale_configuration = ft.LocaleConfiguration(
            current_locale=ft.Locale("en", "US") if settings["language"] == "en"
                else ft.Locale("zh", "TW") if settings["language"] == "zh-tw"
                else ft.Locale("zh", "CN"),
            supported_locales=[ft.Locale("zh", "CN"), ft.Locale("zh", "TW"), ft.Locale("en", "US")],
        )
        sort.value = settings.get("sort", "created_at")
        show_completed.value = bool(settings.get("show_completed", True))
        refresh()
        localize_flet(workspace, settings["language"])
        page.update()

    quick_add_btn = ft.Button(
        "添加",
        icon=ft.Icons.ADD,
        style=primary_button_style(colors),
        on_click=lambda e: quick_add(),
    )
    new_task_btn = ft.Button(
        "新建任务",
        icon=ft.Icons.ADD,
        style=primary_button_style(colors),
        on_click=lambda e: edit_task(),
    )
    primary_buttons.extend([quick_add_btn, new_task_btn])

    quick_panel = ft.Container(
        bgcolor=colors["surface"],
        border=ft.Border.all(1, colors["divider"]),
        border_radius=12,
        padding=ft.Padding.only(left=14, right=8, top=6, bottom=6),
        content=ft.Row(
            controls=[quick, quick_add_btn],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    font_sz = settings.get("font_size", 14)
    brand_icon = ft.Icon(
        ft.Icons.DONE,
        size=scaled_font_size(19, font_sz),
        color=colors["on_accent"],
    )
    brand_badge = ft.Container(
        bgcolor=colors["accent"],
        border_radius=10,
        padding=8,
        content=brand_icon,
    )
    brand_title = ft.Text(
        "TodoApp Flet",
        weight=ft.FontWeight.BOLD,
        size=scaled_font_size(17, font_sz),
        color=colors["text"],
    )
    sidebar_section_label = ft.Text(
        "工作空间",
        size=scaled_font_size(11, font_sz),
        weight=ft.FontWeight.BOLD,
        color=colors["muted"],
    )
    sidebar_divider = ft.Divider(height=1, color=colors["divider"])
    sidebar_version = ft.Text(
        "TODOAPP FLET · 0.3.2",
        size=scaled_font_size(10, font_sz),
        color=colors["muted"],
    )
    header_eyebrow = ft.Text(
        "我的工作空间",
        size=scaled_font_size(11, font_sz),
        color=colors["accent"],
        weight=ft.FontWeight.BOLD,
    )
    header_subtitle = ft.Text(
        "整理任务，专注当下。",
        color=colors["muted"],
        size=scaled_font_size(12, font_sz),
    )
    top_divider = ft.Divider(height=1, color=colors["divider"])
    bottom_divider = ft.Divider(height=1, color=colors["divider"])
    footer_note = ft.Text(
        "任务保存在本地 · 与 Tk 版共享",
        size=scaled_font_size(11, font_sz),
        expand=True,
        color=colors["muted"],
    )

    theme_texts.extend([
        (brand_title, "text"),
        (sidebar_section_label, "muted"),
        (sidebar_version, "muted"),
        (header_eyebrow, "accent"),
        (header_subtitle, "muted"),
        (footer_note, "muted"),
    ])
    theme_dividers.extend([sidebar_divider, top_divider, bottom_divider])

    sidebar = ft.Container(
        width=SIDEBAR_WIDTH,
        padding=ft.Padding.symmetric(horizontal=14, vertical=24),
        bgcolor=colors["sidebar"],
        border=ft.Border(right=ft.BorderSide(1, colors["divider"])),
        content=ft.Column(
            expand=True,
            spacing=6,
            controls=[
                ft.Row([brand_badge, brand_title], spacing=10),
                ft.Container(height=20),
                sidebar_section_label,
                nav_button("全部任务", ft.Icons.LIST_ALT, "all"),
                nav_button("进行中", ft.Icons.ACCESS_TIME, "active"),
                nav_button("已完成", ft.Icons.CHECK_CIRCLE_OUTLINE, "done"),
                ft.Container(expand=True),
                sidebar_divider,
                ft.TextButton("导入任务", icon=ft.Icons.FILE_UPLOAD_OUTLINED,
                              on_click=import_tasks),
                ft.TextButton("导出任务", icon=ft.Icons.FILE_DOWNLOAD_OUTLINED,
                              on_click=export_tasks),
                ft.TextButton("清除已完成", icon=ft.Icons.DELETE_SWEEP_OUTLINED,
                              on_click=clear_completed),
                ft.TextButton(
                    "应用设置", icon=ft.Icons.SETTINGS_OUTLINED,
                    on_click=lambda e: show_settings(
                        page, settings, on_settings_changed, picker, message),
                ),
                sidebar_version,
            ],
        ),
    )

    theme_surfaces.extend([
        (sidebar, "sidebar"),
        (quick_panel, "surface"),
    ])
    theme_borders.extend([
        (sidebar, "right"),
        (quick_panel, "all"),
    ])

    workspace = ft.SafeArea(
        expand=True,
        content=ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    sidebar,
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            expand=True,
                            spacing=0,
                            controls=[
                                ft.Container(
                                    padding=ft.Padding.only(
                                        left=30, top=24, right=30, bottom=18),
                                    content=ft.Column(
                                        spacing=16,
                                        controls=[
                                            ft.Row(
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Column([
                                                        header_eyebrow,
                                                        view_title,
                                                        header_subtitle,
                                                    ], spacing=4, expand=True),
                                                    new_task_btn,
                                                ],
                                            ),
                                            ft.Row([search, sort, show_completed],
                                                   spacing=12,
                                                   vertical_alignment=ft.CrossAxisAlignment.CENTER),
                                        ],
                                    ),
                                ),
                                top_divider,
                                ft.Container(
                                    expand=True,
                                    padding=ft.Padding.only(
                                        left=30, right=30, top=16, bottom=6),
                                    content=ft.Column(
                                        expand=True, spacing=12,
                                        controls=[
                                            stats,
                                            quick_panel,
                                            task_list,
                                        ],
                                    ),
                                ),
                                bottom_divider,
                                ft.Container(
                                    padding=ft.Padding.symmetric(
                                        horizontal=30, vertical=10),
                                    content=ft.Row([
                                        footer_note,
                                        ft.TextButton("保存更改", icon=ft.Icons.SAVE_OUTLINED,
                                                      on_click=manual_save),
                                    ]),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
    )
    app_layout, title_surface = with_titlebar(workspace, settings.get("theme"))
    page.add(app_layout)

    refresh()
    localize_flet(page.controls, settings["language"])
    page.update()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
