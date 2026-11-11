"""Todo App 0.3.1 Flet desktop edition.

The Tkinter UI remains untouched. This prototype reuses the existing Task
dataclass and JSON schema while writing to per-user application storage.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import flet as ft

from models import Task
from task_operations import pop_task_by_id
import storage
from settings_ui import show_settings
from appearance import appearance, normalize_theme
from font_preferences import font_family, register_flet_fonts
from window_chrome import configure_window, with_titlebar, update_titlebar_theme, SIDEBAR_WIDTH


def main(page: ft.Page) -> None:
    page.title = "TodoApp Flet 0.3.2"
    page.padding = 0
    page.spacing = 0
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

    theme_surfaces: list[tuple[ft.Container, str]] = []
    title_surface: ft.Container | None = None
    colors = appearance(settings.get("theme"))

    def apply_theme() -> None:
        nonlocal colors
        settings["theme"] = normalize_theme(settings.get("theme"))
        colors = appearance(settings["theme"])
        page.theme_mode = colors["mode"]
        page.theme = ft.Theme(
            color_scheme_seed=colors["accent"],
            font_family=font_family(settings.get("font_mode")),
        )
        page.bgcolor = colors["canvas"]
        page.window.bgcolor = colors["sidebar"]
        for surface, token in theme_surfaces:
            surface.bgcolor = colors[token]
        if title_surface is not None:
            update_titlebar_theme(title_surface, settings["theme"])
        try:
            width_value, height_value = settings.get("window_size", "900x700").split("x", 1)
            page.window.width = int(width_value)
            page.window.height = int(height_value)
        except (ValueError, TypeError):
            pass

    apply_theme()

    search = ft.TextField(
        hint_text="搜索任务和备注...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        on_change=lambda e: refresh(),
    )
    quick = ft.TextField(
        hint_text="输入任务，按回车创建",
        expand=True,
        on_submit=lambda e: quick_add(),
    )
    show_completed = ft.Checkbox(
        label="显示已完成", value=bool(settings["show_completed"]),
        on_change=lambda e: change_setting("show_completed", bool(e.control.value)),
    )
    sort = ft.Dropdown(
        width=180,
        label="排序",
        value=str(settings.get("sort", "created_at")),
        options=[
            ft.DropdownOption(key="created_at", text="创建时间"),
            ft.DropdownOption(key="priority", text="优先级"),
            ft.DropdownOption(key="due_date", text="截止日期"),
            ft.DropdownOption(key="title", text="标题"),
            ft.DropdownOption(key="completed", text="完成状态"),
        ],
        on_select=lambda e: change_setting("sort", e.control.value),
    )
    stats = ft.Text(size=12, color=ft.Colors.ON_SURFACE_VARIANT)
    task_list = ft.ListView(expand=True, spacing=0)
    view_mode = "all"
    view_title = ft.Text("全部任务", size=27, weight=ft.FontWeight.BOLD)
    nav_widgets: dict[str, ft.Container] = {}


    def message(text: str) -> None:
        # 避免 Paper & Ink 等浅色主题出现默认的深灰色整宽提示条。
        foreground = "#25282B" if colors["mode"] == ft.ThemeMode.LIGHT else "#F2F1F7"
        page.show_dialog(ft.SnackBar(
            content=ft.Text(text, color=foreground),
            bgcolor=appearance(settings.get("theme"))["surface"],
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
            page.pop_dialog()
            if not save():
                tasks.insert(index, removed)
            refresh()

        if not settings.get("confirm_delete", True):
            do_delete(None)
            return
        page.show_dialog(ft.AlertDialog(
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

        page.show_dialog(ft.AlertDialog(
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
            label="截止日期（YYYY-MM-DD，可留空）",
            value=(task.due_date or "") if task else "",
        )
        tags = ft.TextField(
            label="标签（逗号分隔）",
            value=", ".join(task.tags or []) if task else "",
        )
        error = ft.Text("", color=ft.Colors.RED_400, size=12)

        def submit(e) -> None:
            name = (title.value or "").strip()
            if not name:
                error.value = "请填写任务名称"
                return
            due_value = (due.value or "").strip()
            if due_value:
                try:
                    date.fromisoformat(due_value)
                except ValueError:
                    error.value = "日期格式应为 YYYY-MM-DD"
                    return
            changes = {
                "title": name,
                "description": description.value or "",
                "priority": priority.value or "中",
                "due_date": due_value or None,
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

        page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("编辑任务" if editing else "添加任务"),
            content=ft.Container(
                width=410,
                content=ft.Column(
                    controls=[title, description, priority, due, tags, error],
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

    def card(task: Task) -> ft.Control:
        tint = {
            "高": ft.Colors.RED_400,
            "中": ft.Colors.AMBER_600,
            "低": ft.Colors.GREEN_500,
        }.get(task.priority, ft.Colors.BLUE_400)
        tint = settings.get("priority_colors", {}).get(task.priority, tint)
        meta = [f"{task.priority}优先级"]
        if task.due_date:
            meta.append(f"截止 {task.due_date}")
        if task.tags:
            meta.extend(task.tags)
        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=12, vertical=12),
            border=ft.Border(bottom=ft.BorderSide(1, colors["divider"])),
            content=ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Checkbox(
                        value=task.completed,
                        on_change=lambda e, item=task: toggle_task(item, bool(e.control.value)),
                    ),
                    ft.Column(
                        expand=True,
                        spacing=6,
                        controls=[
                            ft.Text(
                                task.title,
                                size=settings.get("font_size", 14),
                                weight=ft.FontWeight.W_600,
                                color=(ft.Colors.ON_SURFACE_VARIANT if task.completed
                                       else ft.Colors.ON_SURFACE),
                            ),
                            ft.Row(
                                spacing=10,
                                wrap=True,
                                controls=[
                                    ft.Text(f"● {meta[0]}", color=tint, size=11),
                                    *[ft.Text(text, size=11, color=ft.Colors.ON_SURFACE_VARIANT)
                                      for text in meta[1:]],
                                ],
                            ),
                            *([ft.Text(task.description, size=12,
                                       color=ft.Colors.ON_SURFACE_VARIANT)]
                              if task.description else []),
                        ],
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT_OUTLINED,
                        tooltip="编辑任务",
                        icon_size=19,
                        on_click=lambda e, item=task: edit_task(item),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        tooltip="删除任务",
                        icon_size=19,
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

    def nav_button(title: str, icon: str, target: str) -> ft.Container:
        button = ft.Container(
            border_radius=9,
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            on_click=lambda e: change_view(target),
            ink=True,
            content=ft.Row([
                ft.Icon(icon, size=19),
                ft.Text(title, size=13, weight=ft.FontWeight.W_500),
            ], spacing=11),
        )
        nav_widgets[target] = button
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
            button.bgcolor = (colors["selected"]
                              if key == view_mode else ft.Colors.TRANSPARENT)
        rows = visible_tasks()
        task_list.controls = [card(t) for t in rows] if rows else [
            ft.Container(
                padding=28,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=42, color=ft.Colors.INDIGO_300),
                        ft.Text("这里暂时没有任务", size=17),
                        ft.Text("添加一条待办，或调整筛选条件", color=ft.Colors.ON_SURFACE_VARIANT),
                    ],
                ),
            ),
        ]

    async def export_tasks(e) -> None:
        payload = json.dumps([t.to_dict() for t in tasks], ensure_ascii=False, indent=2).encode("utf-8")
        try:
            path = await picker.save_file(
                dialog_title="导出待办任务", file_name="todo-tasks.json",
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
                dialog_title="导入待办任务",
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

        page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("确认导入"),
            content=ft.Text(f"导入 {len(imported)} 条任务将替换当前全部 {len(tasks)} 条任务。确定吗？"),
            actions=[
                ft.TextButton("取消", on_click=lambda e: page.pop_dialog()),
                ft.Button("确认导入", on_click=confirm),
            ],
        ))

    def on_settings_changed() -> None:
        # Keep task toolbar controls in sync with the settings workspace.
        apply_theme()
        sort.value = settings.get("sort", "created_at")
        show_completed.value = bool(settings.get("show_completed", True))
        refresh()
        page.update()

    quick_panel = ft.Container(
        bgcolor=colors["surface"],
        border_radius=12,
        padding=8,
        content=ft.Row([
            quick,
            ft.Button("添加", icon=ft.Icons.ADD,
                      on_click=lambda e: quick_add()),
        ]),
    )

    sidebar = ft.Container(
        width=SIDEBAR_WIDTH,
        padding=ft.Padding.symmetric(horizontal=14, vertical=24),
        bgcolor=colors["sidebar"],
        border=ft.Border(right=ft.BorderSide(1, colors["divider"])),
        content=ft.Column(
            expand=True,
            spacing=7,
            controls=[
                ft.Row([
                    ft.Container(
                        bgcolor=ft.Colors.PRIMARY,
                        border_radius=9,
                        padding=8,
                        content=ft.Icon(ft.Icons.DONE, size=19,
                                        color=ft.Colors.ON_PRIMARY),
                    ),
                    ft.Text("TodoApp Flet", weight=ft.FontWeight.BOLD, size=17),
                ], spacing=10),
                ft.Container(height=22),
                ft.Text("工作空间", size=11, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE_VARIANT),
                nav_button("全部任务", ft.Icons.LIST_ALT, "all"),
                nav_button("进行中", ft.Icons.ACCESS_TIME, "active"),
                nav_button("已完成", ft.Icons.CHECK_CIRCLE_OUTLINE, "done"),
                ft.Container(expand=True),
                ft.Divider(height=1, color=ft.Colors.OUTLINE_VARIANT),
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
                ft.Text("TODOAPP FLET · 0.3.2", size=10,
                        color=ft.Colors.ON_SURFACE_VARIANT),
            ],
        ),
    )

    theme_surfaces.extend([
        (sidebar, "sidebar"),
        (quick_panel, "surface"),
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
                                        left=32, top=28, right=32, bottom=22),
                                    content=ft.Column(
                                        spacing=18,
                                        controls=[
                                            ft.Row([
                                                ft.Column([
                                                    ft.Text("我的工作空间", size=11,
                                                            color=ft.Colors.PRIMARY,
                                                            weight=ft.FontWeight.BOLD),
                                                    view_title,
                                                    ft.Text("整理任务，专注当下。",
                                                            color=ft.Colors.ON_SURFACE_VARIANT,
                                                            size=12),
                                                ], spacing=5, expand=True),
                                                ft.Button(
                                                    "新建任务",
                                                    icon=ft.Icons.ADD,
                                                    on_click=lambda e: edit_task(),
                                                ),
                                            ]),
                                            ft.Row([search, sort, show_completed],
                                                   spacing=11,
                                                   vertical_alignment=ft.CrossAxisAlignment.CENTER),
                                        ],
                                    ),
                                ),
                                ft.Divider(height=1, color=ft.Colors.OUTLINE_VARIANT),
                                ft.Container(
                                    expand=True,
                                    padding=ft.Padding.only(
                                        left=32, right=32, top=18, bottom=6),
                                    content=ft.Column(
                                        expand=True, spacing=10,
                                        controls=[
                                            stats,
                                            quick_panel,
                                            task_list,
                                        ],
                                    ),
                                ),
                                ft.Divider(height=1, color=ft.Colors.OUTLINE_VARIANT),
                                ft.Container(
                                    padding=ft.Padding.symmetric(
                                        horizontal=32, vertical=11),
                                    content=ft.Row([
                                        ft.Text("任务保存在本地 · 与 Tk 版共享",
                                                size=11, expand=True,
                                                color=ft.Colors.ON_SURFACE_VARIANT),
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


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
