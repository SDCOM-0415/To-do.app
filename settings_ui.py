"""Full settings workspace for the Flet desktop edition.

Unlike a tall AlertDialog, this screen owns the normal page layout and restores
the task workspace on close. All five original Tk categories are represented.
"""
from __future__ import annotations

import json
import platform
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import flet as ft

import storage
from appearance import PALETTES, appearance, normalize_theme
from font_preferences import normalize_font_mode, scaled_font_size
from window_chrome import with_titlebar, update_titlebar_theme
from localize_flet import localize_flet
from i18n import tr
from i18n import tr

DEFAULT_COLORS = storage.DEFAULT_SETTINGS["priority_colors"]
BACKUP_DIR = storage.APP_DIR / "backups"
COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


def validate_settings(values: dict[str, Any]) -> dict[str, Any]:
    """Normalize settings from either Flet or legacy Tk JSON exports."""
    if not isinstance(values, dict):
        raise ValueError("设置必须是 JSON 对象")
    candidate = json.loads(json.dumps(storage.DEFAULT_SETTINGS))
    candidate.update({k: v for k, v in values.items() if k in candidate})
    # Preserve explicit user choice, translating legacy theme values.
    candidate["theme"] = normalize_theme(candidate.get("theme"))
    candidate["font_mode"] = normalize_font_mode(candidate.get("font_mode"))
    if candidate["language"] not in ("zh-cn", "en", "zh-tw"):
        raise ValueError("语言设置无效")
    if candidate["sort"] not in ("created_at", "priority", "due_date", "title", "completed"):
        raise ValueError("排序设置无效")
    if type(candidate["font_size"]) is not int or not 10 <= candidate["font_size"] <= 20:
        raise ValueError("字体大小应为 10–20")
    match = re.fullmatch(r"(\d+)x(\d+)", str(candidate["window_size"]))
    if not match:
        raise ValueError("窗口大小必须使用 宽度x高度 格式")
    w, h = int(match.group(1)), int(match.group(2))
    if not (800 <= w <= 3840 and 600 <= h <= 2160):
        raise ValueError("窗口大小应介于 800×600 与 3840×2160 之间")
    for key in ("auto_save", "show_completed", "show_statistics", "confirm_delete"):
        if type(candidate[key]) is not bool:
            raise ValueError(f"{key} 必须为布尔值")
    colors = candidate["priority_colors"]
    if not isinstance(colors, dict):
        raise ValueError("优先级颜色数据无效")
    for key in ("高", "中", "低"):
        if not isinstance(colors.get(key), str) or not COLOR_RE.fullmatch(colors[key]):
            raise ValueError(f"{key}优先级颜色必须使用 #RRGGBB 格式")
    candidate["priority_colors"] = {key: colors[key] for key in ("高", "中", "低")}
    return candidate


def _make_backup(values: dict[str, Any], description: str = "手动备份") -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output = BACKUP_DIR / f"flet_settings_{stamp}.json"
    storage._atomic_json_write(output, {
        "timestamp": stamp, "description": description,
        "app_version": "0.3.2", "settings": validate_settings(values),
    })
    for old in sorted(BACKUP_DIR.glob("flet_settings_*.json"), reverse=True)[10:]:
        old.unlink()
    return output


def show_settings(
    page: ft.Page,
    settings: dict[str, Any],
    on_changed: Callable[[], None],
    picker: ft.FilePicker,
    notify: Callable[[str], None],
) -> None:
    """Show a five-tab settings view in place of the task workspace."""
    original_controls = list(page.controls)
    ui_language = settings.get("language", "zh-cn")
    def label(text: str) -> str:
        return tr(text, ui_language)
    title_surface: ft.Container | None = None
    draft = validate_settings(settings)
    error_text = ft.Text(label(""), color=ft.Colors.RED_400, size=scaled_font_size(12, settings.get("font_size", 14)))

    def option(key: str, caption: str, choices: list[tuple[str, str]], width: int | None = None):
        return ft.Dropdown(
            label=label(caption), width=width, value=draft[key],
            options=[ft.DropdownOption(key=value, text=label(name)) for name, value in choices],
            on_select=lambda e: draft.update({key: e.control.value}),
        )

    def heading(name: str, detail: str = "") -> ft.Control:
        return ft.Column(
            controls=[
                ft.Text(label(name), size=scaled_font_size(18, settings.get("font_size", 14)), weight=ft.FontWeight.BOLD),
                *([ft.Text(label(detail), size=scaled_font_size(12, settings.get("font_size", 14)), color=ft.Colors.ON_SURFACE_VARIANT)] if detail else []),
                ft.Divider(height=12, color=ft.Colors.OUTLINE_VARIANT),
            ], spacing=4,
        )

    def scroll_tab(controls: list[ft.Control]) -> ft.Control:
        return ft.Container(
            expand=True,
            padding=ft.Padding.symmetric(horizontal=22, vertical=18),
            content=ft.Column(
                controls=controls, spacing=18, scroll=ft.ScrollMode.AUTO, expand=True,
            ),
        )

    font_mode_control = option("font_mode", "界面字体", [
        ("HarmonyOS Sans SC（内置，默认）", "harmony"),
        ("系统字体（跟随当前平台）", "system"),
    ], 310)

    theme_control = option(
        "theme", "界面风格",
        [(preset["label"], key) for key, preset in PALETTES.items()],
        310,
    )

    size_value = ft.Text(f'{draft["font_size"]} px', weight=ft.FontWeight.W_500)
    def update_size(e) -> None:
        draft["font_size"] = int(e.control.value)
        size_value.value = f'{draft["font_size"]} px'
        size_value.update()

    font = ft.Slider(min=10, max=20, divisions=10, value=draft["font_size"], expand=True, on_change=update_size)
    window_parts = str(draft["window_size"]).split("x")
    width = ft.TextField(label=label("宽度"), width=140, value=window_parts[0], keyboard_type=ft.KeyboardType.NUMBER)
    height = ft.TextField(label=label("高度"), width=140, value=window_parts[1], keyboard_type=ft.KeyboardType.NUMBER)
    language = option("language", "界面语言", [
        ("简体中文", "zh-cn"), ("English", "en"), ("繁體中文", "zh-tw"),
    ], 280)
    sort = option("sort", "任务默认排序", [
        ("创建时间", "created_at"), ("优先级", "priority"), ("截止日期", "due_date"),
        ("标题", "title"), ("完成状态", "completed"),
    ], 280)
    color_fields: dict[str, ft.TextField] = {}
    color_previews: dict[str, ft.Container] = {}
    color_rows = []

    def sync_color_preview(key: str) -> None:
        raw = (color_fields[key].value or "").strip()
        if COLOR_RE.fullmatch(raw):
            color_previews[key].bgcolor = raw
            color_previews[key].update()

    def open_color_picker(key: str) -> None:
        """Visual RGB picker with unrestricted 24-bit colors and hex input."""
        initial = (color_fields[key].value or "").strip()
        if not COLOR_RE.fullmatch(initial):
            initial = DEFAULT_COLORS[key]
        rgb = [int(initial[i:i+2], 16) for i in (1, 3, 5)]
        chosen = ft.Text(initial.upper(), selectable=True)
        preview = ft.Container(width=200, height=38, bgcolor=initial, border_radius=8)
        sliders = []

        def update_rgb(e=None) -> None:
            result = "#" + "".join(f"{int(slider.value):02X}" for slider in sliders)
            chosen.value = result
            preview.bgcolor = result
            chosen.update()
            preview.update()

        for channel, value in zip(("R", "G", "B"), rgb):
            slider = ft.Slider(min=0, max=255, divisions=255, value=value,
                               expand=True, on_change=update_rgb)
            sliders.append(slider)

        def choose_swatch(value: str) -> None:
            chosen.value = value
            preview.bgcolor = value
            chosen.update()
            preview.update()

        swatches = ft.Row(
            controls=[
                ft.Container(
                    width=30, height=30, bgcolor=value, border_radius=6,
                    tooltip=value,
                    on_click=lambda e, color=value: choose_swatch(color),
                )
                for value in ("#FF4444", "#FFAA00", "#44FF44", "#2196F3",
                              "#9C27B0", "#FF4081", "#00BCD4", "#FFFFFF",
                              "#000000")
            ],
            wrap=True, spacing=8,
        )

        def commit_color(e) -> None:
            color_fields[key].value = chosen.value
            sync_color_preview(key)
            color_fields[key].update()
            page.pop_dialog()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(label(f"选择{key}优先级颜色")),
            content=ft.Container(width=365, content=ft.Column(
                tight=True, spacing=12, controls=[
                    ft.Text(label("拖动红、绿、蓝滑块调整颜色")),
                    preview, chosen,
                    ft.Text(label("点击色块直接选择颜色")),
                    swatches,
                    *[ft.Row([ft.Text(channel, width=20), slider], spacing=8)
                      for channel, slider in zip(("R", "G", "B"), sliders)],
                ],
            )),
            actions=[
                ft.TextButton(label("取消"), on_click=lambda e: page.pop_dialog()),
                ft.Button(label("确定"), on_click=commit_color),
            ],
        )
        localize_flet(dialog, ui_language)
        page.show_dialog(dialog)

    for key in ("高", "中", "低"):
        field = ft.TextField(label=label(f"{key}优先级"), value=draft["priority_colors"][key],
                             width=180, on_change=lambda e, k=key: sync_color_preview(k))
        color_fields[key] = field
        preview = ft.Container(width=30, height=30, border_radius=6,
                               bgcolor=draft["priority_colors"][key])
        color_previews[key] = preview
        color_rows.append(ft.Row([
            preview,
            field,
            ft.OutlinedButton(label("选取"), icon=ft.Icons.COLOR_LENS_OUTLINED,
                              on_click=lambda e, k=key: open_color_picker(k)),
        ], spacing=12, wrap=True))

    def reset_colors(e):
        for key, field in color_fields.items():
            field.value = DEFAULT_COLORS[key]
            field.update()
            sync_color_preview(key)
        error_text.value = label("颜色已恢复默认值；点击应用或确定保存。")
        error_text.update()

    def collect() -> dict[str, Any]:
        # Read the current control value directly; on_select may not have fired
        # before the user immediately clicks Apply.
        draft["language"] = language.value or draft["language"]
        draft["window_size"] = f"{width.value}x{height.value}"
        draft["font_size"] = int(font.value)
        draft["priority_colors"] = {key: field.value.strip() for key, field in color_fields.items()}
        return validate_settings(draft)

    def status(text: str, is_error: bool = False):
        error_text.value = label(text)
        error_text.color = ft.Colors.RED_400 if is_error else ft.Colors.GREEN_500
        error_text.update()

    def save_changes(close: bool = False) -> bool:
        try:
            candidate = collect()
            storage.save_settings(candidate)
        except (OSError, ValueError, TypeError) as exc:
            status(str(exc), True)
            return False
        settings.clear()
        settings.update(candidate)
        on_changed()
        # Already mounted settings controls must switch language immediately.
        localize_flet(page.controls, settings.get("language", "zh-cn"))
        if title_surface is not None:
            update_titlebar_theme(title_surface, settings["theme"], settings_view=True)
            page.update()
        if close:
            close_view()
            notify(label("设置已保存"))
        else:
            if candidate["language"] != ui_language:
                # Rebuild settings controls in the new language. This also
                # localizes buttons and dropdowns the widget walker cannot see.
                page.controls.clear()
                page.controls.extend(original_controls)
                show_settings(page, settings, on_changed, picker, notify)
            else:
                status("更改已应用")
        return True

    def close_view(e=None) -> None:
        page.controls.clear()
        page.controls.extend(original_controls)
        page.update()

    def import_candidate(raw: bytes) -> dict[str, Any]:
        data = json.loads(raw.decode("utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError("设置文件必须是 JSON 对象")
        return validate_settings(data.get("settings", data))

    def update_controls(candidate: dict[str, Any]) -> None:
        """Load imported preferences into live controls before applying."""
        draft.clear()
        draft.update(candidate)
        theme_control.value = candidate["theme"]
        font_mode_control.value = candidate["font_mode"]
        language.value = candidate["language"]
        sort.value = candidate["sort"]
        font.value = candidate["font_size"]
        size_value.value = f'{candidate["font_size"]} px'
        w, h = candidate["window_size"].split("x")
        width.value, height.value = w, h
        for key, field in color_fields.items():
            field.value = candidate["priority_colors"][key]
            sync_color_preview(key)
        # Switches are not shared with the original task screen.
        for key, control in switches.items():
            control.value = candidate[key]
        page.update()

    switches: dict[str, ft.Switch] = {}
    def switch_row(key: str, caption: str, subtitle: str) -> ft.Control:
        switch = ft.Switch(
            value=draft[key], on_change=lambda e: draft.update({key: bool(e.control.value)}),
        )
        switches[key] = switch
        return ft.Row([
            ft.Column([
                ft.Text(label(caption), weight=ft.FontWeight.W_500, size=scaled_font_size(14, settings.get("font_size", 14))),
                ft.Text(label(subtitle), size=scaled_font_size(11, settings.get("font_size", 14)), color=ft.Colors.ON_SURFACE_VARIANT),
            ], expand=True, spacing=3),
            switch,
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)

    async def export_settings(e) -> None:
        try:
            candidate = collect()
            payload = json.dumps({
                "app_name": "TodoApp Flet", "app_version": "0.3.2",
                "export_time": datetime.now().isoformat(timespec="seconds"),
                "settings": candidate,
            }, ensure_ascii=False, indent=2).encode("utf-8")
            path = await picker.save_file(
                dialog_title=label("导出设置"), file_name="todo-settings.json",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["json"], src_bytes=payload,
            )
            if path:
                status("设置已导出")
        except Exception as exc:
            status(f"导出失败：{exc}", True)

    async def import_settings(e) -> None:
        try:
            selected = await picker.pick_files(
                dialog_title=label("导入设置"), allow_multiple=False,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["json"], with_data=True,
            )
            if not selected:
                return
            item = selected[0]
            data = item.bytes if item.bytes is not None else Path(item.path).read_bytes()
            update_controls(import_candidate(data))
            status("设置已载入；点击应用或确定保存")
        except Exception as exc:
            status(f"导入失败：{exc}", True)

    def backup_settings(e) -> None:
        try:
            path = _make_backup(collect())
            status(f"已创建备份：{path.name}")
            refresh_backups()
        except Exception as exc:
            status(f"备份失败：{exc}", True)

    backup_selector = ft.Dropdown(label=label("选择备份"), width=300, options=[])
    def refresh_backups() -> None:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        backup_selector.options = [
            ft.DropdownOption(key=p.name, text=p.name.replace("flet_settings_", ""))
            for p in sorted(BACKUP_DIR.glob("flet_settings_*.json"), reverse=True)
        ]
        backup_selector.update()

    def restore_backup(e) -> None:
        if not backup_selector.value:
            status("请先选择备份", True)
            return
        try:
            path = BACKUP_DIR / Path(backup_selector.value).name
            update_controls(import_candidate(path.read_bytes()))
            status("备份已载入；点击应用或确定保存")
        except Exception as exc:
            status(f"恢复失败：{exc}", True)

    def delete_backup(e) -> None:
        if not backup_selector.value:
            status("请先选择备份", True)
            return
        try:
            (BACKUP_DIR / Path(backup_selector.value).name).unlink()
            backup_selector.value = None
            refresh_backups()
            status("备份已删除")
        except Exception as exc:
            status(f"删除备份失败：{exc}", True)

    def reset_all(e) -> None:
        update_controls(validate_settings(storage.DEFAULT_SETTINGS))
        status("已恢复默认值；点击应用或确定保存")

    appearances = scroll_tab([
        heading("界面风格", "独立于 Tk 版本保存，可随时切换。"),
        theme_control,
        *[
            ft.Text(
                f'{preset["label"]} · {preset["description"]}',
                size=scaled_font_size(12, settings.get("font_size", 14)),
                color=ft.Colors.ON_SURFACE_VARIANT,
            )
            for preset in PALETTES.values()
        ],
        heading("界面字体", "鸿蒙字体默认内置；系统字体会按 Windows / macOS / Linux 自动选择。"),
        font_mode_control,
        ft.Text(label("字体授权：HarmonyOS Sans © Huawei Device Co., Ltd.，详见 assets/fonts/LICENSE.txt"), size=scaled_font_size(11, settings.get("font_size", 14)),
                color=ft.Colors.ON_SURFACE_VARIANT),
        heading("字体大小", "任务标题和部分界面文字的字号。"),
        ft.Row([font, size_value]),
        heading("默认窗口大小", "下次启动时按照保存的尺寸打开。"),
        ft.Row([width, ft.Text(label("×")), height], spacing=12),
    ])
    behaviors = scroll_tab([
        heading("任务与显示"),
        switch_row("auto_save", "自动保存", "启用后立即保存任务；关闭后使用主界面的保存按钮。"),
        switch_row("show_completed", "显示已完成任务", "在任务列表中显示或隐藏已完成项目。"),
        switch_row("show_statistics", "显示统计信息", "显示任务总数、已完成及逾期数量。"),
        switch_row("confirm_delete", "删除前确认", "删除单条任务前弹出确认提示。"),
        heading("偏好设置"),
        sort,
        language,
        ft.Text(label("选择语言后点击应用或确定，界面会立即更新。"),
                color=ft.Colors.ON_SURFACE_VARIANT, size=scaled_font_size(11, settings.get("font_size", 14))),
    ])
    colors = scroll_tab([
        heading("优先级颜色", "点击选取以可视化调整 RGB，或直接输入 #RRGGBB 色号。"),
        *color_rows,
        ft.OutlinedButton(label("恢复默认颜色"), icon=ft.Icons.RESTART_ALT, on_click=reset_colors),
    ])
    advanced = scroll_tab([
        heading("设置导入与导出", "支持当前 Flet 版以及原 Tk 版导出的设置 JSON。"),
        ft.Row([
            ft.OutlinedButton(label("导出设置"), icon=ft.Icons.UPLOAD_FILE, on_click=export_settings),
            ft.OutlinedButton(label("导入设置"), icon=ft.Icons.DOWNLOAD, on_click=import_settings),
        ], wrap=True),
        ft.OutlinedButton(label("重置所有设置"), icon=ft.Icons.RESTART_ALT, on_click=reset_all),
        heading("设置备份", "最多保留最近 10 份 Flet 设置备份，不影响任务数据。"),
        ft.OutlinedButton(label("创建备份"), icon=ft.Icons.SAVE_OUTLINED, on_click=backup_settings),
        backup_selector,
        ft.Row([
            ft.TextButton(label("恢复所选备份"), on_click=restore_backup),
            ft.TextButton(label("删除所选备份"), on_click=delete_backup),
        ], wrap=True),
        heading("调试与数据目录"),
        ft.Text(label(f"Flet 配置文件：{storage.SETTINGS_FILE}"), selectable=True, size=scaled_font_size(12, settings.get("font_size", 14))),
        ft.Text(label(f"Tk 配置文件：{storage.TK_SETTINGS_FILE}"), selectable=True, size=scaled_font_size(12, settings.get("font_size", 14))),
        ft.Text(label(f"共享任务文件：{storage.TASKS_FILE}"), selectable=True, size=scaled_font_size(12, settings.get("font_size", 14))),
        ft.Text(label("两个版本共享任务，但设置互相独立。不要同时编辑相同任务。"),
                color=ft.Colors.ON_SURFACE_VARIANT, size=scaled_font_size(11, settings.get("font_size", 14))),
    ])
    about = scroll_tab([
        heading("TodoApp Flet 0.3.2"),
        ft.Text(label("现代化跨平台待办事项管理器")),
        ft.Text(label("开发者：SDCOM")),
        ft.Text(label(f"版权所有 © {datetime.now().year} SDCOM")),
        ft.Text(label("技术栈：Python · Flet · Flutter")),
        heading("功能"),
        ft.Text(label("任务创建与编辑 · 优先级 · 截止日期 · 标签")),
        ft.Text(label("搜索与过滤 · 统计信息 · 多主题 · JSON 导入导出")),
        heading("系统信息"),
        ft.Text(label(f"操作系统：{platform.platform()}"), selectable=True),
        ft.Text(label(f"Python 版本：{sys.version.split()[0]}"), selectable=True),
        ft.Text(label(f"架构：{platform.machine()}"), selectable=True),
        ft.Text(label("项目地址：github.com/SDCOM-0415/To-do.app"), selectable=True),
    ])

    tabs = ft.Tabs(
        length=5,
        selected_index=0,
        expand=True,
        content=ft.Column(
            expand=True, spacing=0,
            controls=[
                ft.TabBar(tabs=[
                    ft.Tab(label=label("外观"), icon=ft.Icons.PALETTE_OUTLINED),
                    ft.Tab(label=label("行为"), icon=ft.Icons.TUNE),
                    ft.Tab(label=label("颜色"), icon=ft.Icons.COLOR_LENS_OUTLINED),
                    ft.Tab(label=label("高级"), icon=ft.Icons.SETTINGS_OUTLINED),
                    ft.Tab(label=label("关于"), icon=ft.Icons.INFO_OUTLINE),
                ]),
                ft.TabBarView(
                    expand=True,
                    controls=[appearances, behaviors, colors, advanced, about],
                ),
            ],
        ),
    )

    screen = ft.SafeArea(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=26, vertical=17),
                    content=ft.Row([
                        ft.IconButton(ft.Icons.ARROW_BACK, tooltip=label("返回任务列表"), on_click=close_view),
                        ft.Column([
                            ft.Text(label("应用设置"), size=scaled_font_size(23, settings.get("font_size", 14)), weight=ft.FontWeight.BOLD),
                            ft.Text(label(f"TodoApp Flet · {len(PALETTES)} 种外观风格"), size=scaled_font_size(12, settings.get("font_size", 14)), color=ft.Colors.ON_SURFACE_VARIANT),
                        ], expand=True, spacing=3),
                    ]),
                ),
                ft.Divider(height=1, color=ft.Colors.OUTLINE_VARIANT),
                tabs,
                ft.Divider(height=1, color=ft.Colors.OUTLINE_VARIANT),
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=25, vertical=12),
                    content=ft.Row([
                        ft.Container(content=error_text, expand=True),
                        ft.TextButton(label("取消"), on_click=close_view),
                        ft.OutlinedButton(label("应用"), on_click=lambda e: save_changes()),
                        ft.Button(label("确定"), on_click=lambda e: save_changes(close=True)),
                    ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ),
            ],
        ),
    )

    layout, title_surface = with_titlebar(screen, settings.get("theme"), settings_view=True)
    page.controls.clear()
    page.add(layout)
    localize_flet(page.controls, settings.get("language", "zh-cn"))
    page.update()
    # Controls need to be mounted before update() can be used.
    refresh_backups()
