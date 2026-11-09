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
import storage
from settings_ui import show_settings


def main(page: ft.Page) -> None:
    page.title = "Todo App 0.3.1"
    page.padding = 24
    page.spacing = 14
    picker = ft.FilePicker()
    page.services.append(picker)
    page.window.width = 1100
    page.window.height = 760
    page.window.min_width = 750
    page.window.min_height = 540

    dirty = False
    try:
        tasks = storage.load_tasks()
        settings = storage.load_settings()
    except Exception as exc:
        page.add(ft.Text(f"无法读取任务数据：{exc}", color=ft.Colors.RED_400))
        page.add(ft.Text(f"数据目录：{storage.APP_DIR}"))
        return

    def apply_theme() -> None:
        page.theme_mode = {
            "light": ft.ThemeMode.LIGHT,
            "dark": ft.ThemeMode.DARK,
        }.get(settings["theme"], ft.ThemeMode.SYSTEM)
        page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
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
    theme = ft.Dropdown(
        width=145,
        label="外观",
        value=settings["theme"],
        options=[
            ft.DropdownOption(key="system", text="跟随系统"),
            ft.DropdownOption(key="light", text="浅色"),
            ft.DropdownOption(key="dark", text="深色"),
        ],
        on_select=lambda e: change_setting("theme", e.control.value),
    )
    stats = ft.Text(size=13, color=ft.Colors.ON_SURFACE_VARIANT)
    task_list = ft.ListView(expand=True, spacing=9)

    def message(text: str) -> None:
        page.show_dialog(ft.SnackBar(content=ft.Text(text)))

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
        settings[name] = value
        try:
            storage.save_settings(settings)
        except Exception as exc:
            message(f"无法保存设置：{exc}")
        if name == "theme":
            apply_theme()
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
        def do_delete(e) -> None:
            page.pop_dialog()
            tasks.remove(task)
            if not save():
                tasks.append(task)
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
            meta.append(" · ".join(task.tags))
        return ft.Container(
            border_radius=16,
            padding=14,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Checkbox(
                        value=task.completed,
                        on_change=lambda e, item=task: toggle_task(item, bool(e.control.value)),
                    ),
                    ft.Column(
                        expand=True,
                        spacing=4,
                        controls=[
                            ft.Text(
                                task.title,
                                size=settings.get("font_size", 14),
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.ON_SURFACE if not task.completed
                                else ft.Colors.ON_SURFACE_VARIANT,
                            ),
                            ft.Text("  •  ".join(meta), color=tint, size=12),
                            *([ft.Text(task.description, size=12, color=ft.Colors.ON_SURFACE_VARIANT)]
                              if task.description else []),
                        ],
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT_OUTLINED,
                        tooltip="编辑任务",
                        on_click=lambda e, item=task: edit_task(item),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        tooltip="删除任务",
                        on_click=lambda e, item=task: remove_task(item),
                    ),
                ],
            ),
        )

    def visible_tasks() -> list[Task]:
        query = (search.value or "").lower().strip()
        rows = [
            t for t in tasks
            if (settings.get("show_completed", True) or not t.completed)
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
        stats.value = f"总计 {len(tasks)} 项  ·  已完成 {complete}  ·  未完成 {len(tasks) - complete}  ·  已逾期 {overdue}"
        stats.visible = bool(settings.get("show_statistics", True))
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
        theme.value = settings.get("theme", "system")
        sort.value = settings.get("sort", "created_at")
        show_completed.value = bool(settings.get("show_completed", True))
        refresh()
        page.update()

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                spacing=16,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column([
                                ft.Text("Today, in focus.", size=29, weight=ft.FontWeight.BOLD),
                                ft.Text("一个更轻快的跨平台待办事项管理器", color=ft.Colors.ON_SURFACE_VARIANT),
                            ], expand=True, spacing=2),
                            ft.IconButton(icon=ft.Icons.SETTINGS_OUTLINED, tooltip="应用设置", on_click=lambda e: show_settings(page, settings, on_settings_changed, picker, message)),
                            theme,
                        ],
                    ),
                    ft.Container(
                        padding=16,
                        border_radius=18,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                        content=ft.Column(
                            spacing=10,
                            controls=[
                                ft.Row([quick, ft.Button("添加任务", icon=ft.Icons.ADD, on_click=lambda e: quick_add())]),
                                ft.Row(
                                    controls=[search, sort, show_completed],
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ],
                        ),
                    ),
                    stats,
                    task_list,
                    ft.Row(
                        controls=[
                            ft.Text(f"数据目录：{storage.APP_DIR}", size=11, color=ft.Colors.ON_SURFACE_VARIANT, expand=True),
                            ft.TextButton("保存更改", on_click=manual_save),
                            ft.TextButton("导入 JSON", on_click=import_tasks),
                            ft.TextButton("导出 JSON", on_click=export_tasks),
                            ft.TextButton("清除已完成", on_click=clear_completed),
                        ],
                    ),
                ],
            ),
        )
    )
    refresh()


if __name__ == "__main__":
    ft.run(main)
