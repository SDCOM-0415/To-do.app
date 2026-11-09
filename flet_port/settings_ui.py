"""Modern Flet settings panel mirroring the legacy Tk settings features."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import flet as ft
import storage


def show_settings(
    page: ft.Page,
    settings: dict[str, Any],
    on_changed: Callable[[], None],
    picker: ft.FilePicker,
    notify: Callable[[str], None],
) -> None:
    draft = json.loads(json.dumps(settings))
    colors = draft.get("priority_colors", {"高": "#ff4444", "中": "#ffaa00", "低": "#44ff44"})
    theme = ft.Dropdown(
        label="主题模式", value=draft.get("theme", "system"),
        options=[ft.DropdownOption(key="system", text="跟随系统"),
                 ft.DropdownOption(key="dark", text="深色模式"),
                 ft.DropdownOption(key="light", text="浅色模式")],
        on_select=lambda e: draft.update(theme=e.control.value),
    )
    font_label = ft.Text(f"{draft.get('font_size', 14)} px")
    font_size = ft.Slider(
        min=10, max=20, divisions=10, value=float(draft.get("font_size", 14)),
        label="{value} px",
        on_change=lambda e: (draft.update(font_size=int(e.control.value)), setattr(font_label, "value", f"{int(e.control.value)} px"), font_label.update()),
    )
    width_text, height_text = str(draft.get("window_size", "900x700")).split("x", 1)
    width = ft.TextField(label="宽度", value=width_text, width=130, keyboard_type=ft.KeyboardType.NUMBER)
    height = ft.TextField(label="高度", value=height_text, width=130, keyboard_type=ft.KeyboardType.NUMBER)
    auto_save = ft.Switch(label="自动保存任务变更", value=bool(draft.get("auto_save", True)),
                          on_change=lambda e: draft.update(auto_save=bool(e.control.value)))
    show_completed = ft.Switch(label="默认显示已完成任务", value=bool(draft.get("show_completed", True)),
                                on_change=lambda e: draft.update(show_completed=bool(e.control.value)))
    show_statistics = ft.Switch(label="显示统计面板", value=bool(draft.get("show_statistics", True)),
                                 on_change=lambda e: draft.update(show_statistics=bool(e.control.value)))
    confirm_delete = ft.Switch(label="删除任务时确认", value=bool(draft.get("confirm_delete", True)),
                                on_change=lambda e: draft.update(confirm_delete=bool(e.control.value)))
    language = ft.Dropdown(
        label="界面语言", value=draft.get("language", "zh-cn"),
        options=[ft.DropdownOption(key="zh-cn", text="简体中文"),
                 ft.DropdownOption(key="en", text="English"),
                 ft.DropdownOption(key="zh-tw", text="繁體中文")],
        on_select=lambda e: draft.update(language=e.control.value),
    )
    sort = ft.Dropdown(
        label="默认排序", value=draft.get("sort", "created_at"),
        options=[ft.DropdownOption(key="created_at", text="创建时间"),
                 ft.DropdownOption(key="priority", text="优先级"),
                 ft.DropdownOption(key="due_date", text="截止日期"),
                 ft.DropdownOption(key="title", text="标题"),
                 ft.DropdownOption(key="completed", text="完成状态")],
        on_select=lambda e: draft.update(sort=e.control.value),
    )
    color_fields = {
        key: ft.TextField(label=f"{key}优先级颜色", value=colors.get(key, default), width=190)
        for key, default in (("高", "#ff4444"), ("中", "#ffaa00"), ("低", "#44ff44"))
    }
    status = ft.Text("", size=12, color=ft.Colors.ON_SURFACE_VARIANT)

    def section(title: str, *controls: ft.Control) -> ft.Control:
        return ft.Container(
            padding=16, border_radius=14, bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                spacing=10,
                controls=[ft.Text(title, size=16, weight=ft.FontWeight.BOLD), *controls],
            ),
        )

    def validate_and_collect() -> bool:
        try:
            w, h = int((width.value or "").strip()), int((height.value or "").strip())
            if not (800 <= w <= 3840 and 600 <= h <= 2160):
                raise ValueError("窗口尺寸应在 800×600 至 3840×2160 之间")
            normalized = {}
            for key, field in color_fields.items():
                value = (field.value or "").strip()
                if len(value) != 7 or not value.startswith("#"):
                    raise ValueError(f"{key}优先级颜色必须是 #RRGGBB 格式")
                int(value[1:], 16)
                normalized[key] = value
            draft["window_size"] = f"{w}x{h}"
            draft["font_size"] = int(font_size.value or 14)
            draft["priority_colors"] = normalized
            return True
        except (ValueError, TypeError) as exc:
            status.value = str(exc)
            status.color = ft.Colors.RED_400
            status.update()
            return False

    def apply(e=None, close: bool = False) -> None:
        if not validate_and_collect():
            return
        settings.clear()
        settings.update(draft)
        try:
            storage.save_settings(settings)
        except Exception as exc:
            notify(f"保存设置失败：{exc}")
            return
        on_changed()
        status.value = "设置已保存"
        status.color = ft.Colors.GREEN_500
        status.update()
        if close:
            page.pop_dialog()
            notify("设置已应用")

    async def export_settings(e) -> None:
        try:
            payload = {
                "app_name": "Todo App",
                "app_version": "0.3.1",
                "settings": settings,
            }
            path = await picker.save_file(
                dialog_title="导出所有设置", file_name="todo-settings.json",
                file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["json"],
                src_bytes=json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"),
            )
            if path:
                notify(f"设置已导出：{path}")
        except Exception as exc:
            notify(f"导出设置失败：{exc}")

    async def import_settings(e) -> None:
        try:
            files = await picker.pick_files(
                dialog_title="导入设置", allow_multiple=False,
                file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["json"],
                with_data=True,
            )
            if not files:
                return
            item = files[0]
            raw = item.bytes if item.bytes is not None else Path(item.path).read_bytes()
            payload = json.loads(raw.decode("utf-8-sig"))
            imported = payload.get("settings") if isinstance(payload, dict) else None
            if not isinstance(imported, dict):
                raise ValueError("设置文件格式无效，缺少 settings 对象")
            candidate = json.loads(json.dumps(storage.DEFAULT_SETTINGS))
            candidate.update(imported)
            # Validate through the same constraints exposed in the UI.
            if candidate.get("theme") not in ("system", "dark", "light"):
                raise ValueError("无效的主题设置")
            if not isinstance(candidate.get("font_size"), int) or not 10 <= candidate["font_size"] <= 20:
                raise ValueError("字体大小必须在 10-20 之间")
            for key in ("高", "中", "低"):
                color = candidate.get("priority_colors", {}).get(key, "")
                if len(color) != 7 or not color.startswith("#"):
                    raise ValueError(f"{key}优先级颜色格式无效")
                int(color[1:], 16)
            settings.clear()
            settings.update(candidate)
            storage.save_settings(settings)
            on_changed()
            page.pop_dialog()
            notify("设置已导入并应用")
        except Exception as exc:
            notify(f"导入设置失败：{exc}")

    def reset_settings(e) -> None:
        def confirm(event) -> None:
            page.pop_dialog()
            settings.clear()
            settings.update(json.loads(json.dumps(storage.DEFAULT_SETTINGS)))
            storage.save_settings(settings)
            on_changed()
            page.pop_dialog()
            notify("所有 Flet 设置已恢复默认值")

        page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("重置所有设置？"),
            content=ft.Text("这会恢复 Flet 版本的全部设置，但不会删除任务数据。"),
            actions=[
                ft.TextButton("取消", on_click=lambda event: page.pop_dialog()),
                ft.Button("确认重置", on_click=confirm),
            ],
        ))

    page.show_dialog(ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Icon(ft.Icons.SETTINGS_OUTLINED),
            ft.Text("应用设置", size=22, weight=ft.FontWeight.BOLD),
        ]),
        content=ft.Container(
            width=640,
            height=590,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=12,
                controls=[
                    section("外观设置", theme, ft.Text("字体大小"), font_size, font_label,
                            ft.Row([width, height], spacing=10)),
                    section("行为设置", auto_save, show_completed, show_statistics,
                            confirm_delete, language, sort),
                    section("颜色设置", *color_fields.values(),
                            ft.Text("颜色使用十六进制格式，例如 #ff4444。")),
                    section("数据管理",
                            ft.Text("任务文件在 Tk 与 Flet 版本之间共享；界面设置分别保存。"),
                            ft.Text(f"共享数据目录：{storage.APP_DIR}", size=11),
                            ft.Row([
                                ft.OutlinedButton("导出所有设置", icon=ft.Icons.UPLOAD_FILE, on_click=export_settings),
                                ft.OutlinedButton("导入设置", icon=ft.Icons.DOWNLOAD, on_click=import_settings),
                                ft.OutlinedButton("重置所有设置", icon=ft.Icons.RESTART_ALT, on_click=reset_settings),
                            ], wrap=True)),
                    section("关于",
                            ft.Text("Todo App 0.3.1 · Flet Edition"),
                            ft.Text("开发者：SDCOM"),
                            ft.Text("技术栈：Python 3.12 · Flet 1.1 · Flutter"),
                            ft.Text("GitHub：github.com/SDCOM-0415/To-do.app")),
                    status,
                ],
            ),
        ),
        actions=[
            ft.TextButton("取消", on_click=lambda e: page.pop_dialog()),
            ft.OutlinedButton("应用", on_click=apply),
            ft.Button("确定", on_click=lambda e: apply(close=True)),
        ],
    ))
