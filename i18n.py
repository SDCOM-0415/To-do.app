"""UI translations shared by the Tk and Flet editions.

The JSON task schema and priority identifiers remain in Chinese for compatibility.
Only UI labels and messages are translated. Unknown/user-generated strings are not changed.
"""
from __future__ import annotations

LANGUAGES = ("zh-cn", "en", "zh-tw")

# Canonical Simplified Chinese -> (English, Traditional Chinese)
STRINGS = {
    "全部任务": ("All tasks", "全部任務"),
    "进行中": ("In progress", "進行中"),
    "已完成": ("Completed", "已完成"),
    "工作空间": ("Workspace", "工作空間"),
    "我的工作空间": ("My workspace", "我的工作空間"),
    "你的个人工作空间": ("Your personal workspace", "你的個人工作空間"),
    "任务清单": ("Task list", "任務清單"),
    "任务统计": ("Task statistics", "任務統計"),
    "总任务: 0": ("Total tasks: 0", "總任務: 0"),
    "已完成: 0": ("Completed: 0", "已完成: 0"),
    "待完成: 0": ("Remaining: 0", "待完成: 0"),
    "已过期: 0": ("Overdue: 0", "已逾期: 0"),
    "完成率: 0%": ("Completion: 0%", "完成率: 0%"),
    "整理任务，专注当下。": ("Organize tasks. Stay focused.", "整理任務，專注當下。"),
    "这里暂时没有任务": ("No tasks here yet", "這裡暫時沒有任務"),
    "添加一条待办，或调整筛选条件": ("Add a task or adjust your filters", "新增待辦事項或調整篩選條件"),
    "新建任务": ("New task", "新增任務"),
    "编辑任务": ("Edit task", "編輯任務"),
    "添加": ("Add", "新增"),
    "详细添加": ("Add details", "詳細新增"),
    "编辑": ("Edit", "編輯"),
    "删除": ("Delete", "刪除"),
    "删除任务": ("Delete task", "刪除任務"),
    "删除任务？": ("Delete task?", "刪除任務？"),
    "取消": ("Cancel", "取消"),
    "确定": ("OK", "確定"),
    "确认": ("Confirm", "確認"),
    "应用": ("Apply", "套用"),
    "保存": ("Save", "儲存"),
    "保存更改": ("Save changes", "儲存變更"),
    "排序:": ("Sort:", "排序："),
    "排序": ("Sort", "排序"),
    "创建时间": ("Created", "建立時間"),
    "截止日期": ("Due date", "截止日期"),
    "截止日期:": ("Due date:", "截止日期："),
    "标题": ("Title", "標題"),
    "任务标题:": ("Task title:", "任務標題："),
    "任务描述:": ("Description:", "任務描述："),
    "优先级": ("Priority", "優先級"),
    "优先级:": ("Priority:", "優先級："),
    "高": ("High", "高"),
    "中": ("Medium", "中"),
    "低": ("Low", "低"),
    "完成状态": ("Completion status", "完成狀態"),
    "搜索任务...": ("Search tasks...", "搜尋任務..."),
    "搜索任务…": ("Search tasks…", "搜尋任務…"),
    "搜索任务和备注...": ("Search tasks and notes...", "搜尋任務與備註..."),
    "输入新任务，按回车快速添加...": ("Type a task and press Enter...", "輸入新任務並按 Enter 新增..."),
    "输入任务并按回车添加…": ("Type a task and press Enter…", "輸入任務並按 Enter 新增…"),
    "搜索与过滤 · 统计信息 · 多主题 · JSON 导入导出": ("Search & filter · Statistics · Themes · JSON import/export", "搜尋與篩選 · 統計資訊 · 多主題 · JSON 匯入匯出"),
    "任务创建与编辑 · 优先级 · 截止日期 · 标签": ("Create & edit · Priority · Due date · Tags", "建立與編輯任務 · 優先級 · 截止日期 · 標籤"),
    "显示已完成": ("Show completed", "顯示已完成"),
    "显示已完成任务": ("Show completed tasks", "顯示已完成任務"),
    "清除已完成": ("Clear completed", "清除已完成"),
    "清除已完成任务": ("Clear completed tasks", "清除已完成任務"),
    "清除所有任务": ("Clear all tasks", "清除所有任務"),
    "导入任务": ("Import tasks", "匯入任務"),
    "导出任务": ("Export tasks", "匯出任務"),
    "应用设置": ("Settings", "應用程式設定"),
    "⚙️ 应用设置": ("⚙️ Settings", "⚙️ 應用程式設定"),
    "返回任务列表": ("Back to tasks", "返回任務清單"),
    "界面风格": ("Appearance preset", "介面風格"),
    "字体大小": ("Font size", "字體大小"),
    "界面字体": ("UI font", "介面字體"),
    "主题模式": ("Theme mode", "主題模式"),
    "主界面布局": ("Main layout", "主介面版面"),
    "窗口设置": ("Window settings", "視窗設定"),
    "宽度": ("Width", "寬度"),
    "高度": ("Height", "高度"),
    "默认窗口大小:": ("Default window size:", "預設視窗大小："),
    "启用自动保存（每30秒）": ("Auto-save every 30 seconds", "每 30 秒自動儲存"),
    "自动保存": ("Auto-save", "自動儲存"),
    "删除任务时确认": ("Confirm before deleting", "刪除任務前確認"),
    "显示统计面板": ("Show statistics", "顯示統計面板"),
    "显示统计信息": ("Show statistics", "顯示統計資訊"),
    "显示选项": ("Display options", "顯示選項"),
    "默认显示已完成任务": ("Show completed by default", "預設顯示已完成任務"),
    "行为": ("Behavior", "行為"),
    "外观": ("Appearance", "外觀"),
    "颜色": ("Colors", "顏色"),
    "高级": ("Advanced", "進階"),
    "关于": ("About", "關於"),
    "语言设置": ("Language", "語言設定"),
    "界面语言:": ("Interface language:", "介面語言："),
    "界面语言": ("Interface language", "介面語言"),
    "优先级颜色": ("Priority colors", "優先級顏色"),
    "重置为默认颜色": ("Reset colors", "重設預設顏色"),
    "恢复默认颜色": ("Restore default colors", "還原預設顏色"),
    "选择颜色": ("Choose color", "選擇顏色"),
    "选择截止日期": ("Choose a due date", "選擇截止日期"),
    "日历": ("Calendar", "日曆"),
    "打开日期选择器": ("Open calendar", "開啟日期選擇器"),
    "确认导入": ("Confirm import", "確認匯入"),
    "确认清除": ("Confirm clear", "確認清除"),
    "任务与显示": ("Tasks & display", "任務與顯示"),
    "偏好设置": ("Preferences", "偏好設定"),
    "默认窗口大小": ("Default window size", "預設視窗大小"),
    "导出设置": ("Export settings", "匯出設定"),
    "导入设置": ("Import settings", "匯入設定"),
    "导出所有设置": ("Export all settings", "匯出所有設定"),
    "重置所有设置": ("Reset settings", "重設所有設定"),
    "数据管理": ("Data management", "資料管理"),
    "调试信息": ("Debug information", "偵錯資訊"),
    "高级设置": ("Advanced settings", "進階設定"),
    "主要功能": ("Features", "主要功能"),
    "开发信息": ("Developer information", "開發資訊"),
    "系统信息": ("System information", "系統資訊"),
    "联系方式": ("Contact", "聯絡方式"),
    "快捷操作": ("Quick actions", "快速操作"),
    "现代化跨平台待办事项管理器": ("Modern cross-platform task manager", "現代跨平台待辦事項管理器"),
    "创建备份": ("Create backup", "建立備份"),
    "恢复所选备份": ("Restore selected backup", "還原所選備份"),
    "删除所选备份": ("Delete selected backup", "刪除所選備份"),
    "设置导入与导出": ("Import / export settings", "匯入／匯出設定"),
    "设置备份": ("Settings backups", "設定備份"),
    "任务保存在本地 · 与 Tk 版共享": ("Tasks stored locally · Shared with Tk", "任務儲存於本機 · 與 Tk 版共用"),
    "任务存储在本地 · 与 Flet 版共享数据": ("Tasks stored locally · Shared with Flet", "任務儲存於本機 · 與 Flet 版共用資料"),
    "应用后即可切换；任务与配置不会丢失。": ("Apply to switch; your tasks and settings are preserved.", "套用後即可切換；任務與設定不會遺失。"),
    "字体授权：HarmonyOS Sans © Huawei Device Co., Ltd.，详见 assets/fonts/LICENSE.txt": ("Font license: HarmonyOS Sans © Huawei Device Co., Ltd. See assets/fonts/LICENSE.txt", "字體授權：HarmonyOS Sans © Huawei Device Co., Ltd.，詳見 assets/fonts/LICENSE.txt"),
    "两个版本共享任务，但设置互相独立。不要同时编辑相同任务。": ("Both editions share tasks but have separate settings. Avoid editing at the same time.", "兩個版本共用任務，但設定獨立。請勿同時編輯相同任務。"),
    "内置字体版权归 Huawei Device Co., Ltd. 所有。": ("Bundled font © Huawei Device Co., Ltd.", "內建字體版權歸 Huawei Device Co., Ltd. 所有。"),
    "项目地址：github.com/SDCOM-0415/To-do.app": ("Project: github.com/SDCOM-0415/To-do.app", "專案網址：github.com/SDCOM-0415/To-do.app"),
    "目前语言选项沿用 Tk 版配置；Flet 界面完整本地化仍需单独实现。": ("Select a language and apply it to update the interface.", "選擇介面語言後按套用即可更新。"),
    "开发者：SDCOM": ("Developer: SDCOM", "開發者：SDCOM"),
    "开发者: SDCOM": ("Developer: SDCOM", "開發者：SDCOM"),
    "排序设置": ("Sort settings", "排序設定"),
    "保存设置": ("Save settings", "儲存設定"),
}
# Longer keys first to avoid translating a short label within a longer string.
_REVERSE = {}
for chinese, versions in STRINGS.items():
    _REVERSE.setdefault(chinese, chinese)
    for translated in versions:
        _REVERSE.setdefault(translated, chinese)


def normalize_language(value: str | None) -> str:
    return value if value in LANGUAGES else "zh-cn"


def tr(value: str, language: str | None = None) -> str:
    """Translate known UI text; leave task titles, notes and unknown strings intact."""
    if not isinstance(value, str):
        return value
    if language is None:
        language = "zh-cn"
    language = normalize_language(language)
    canonical = _REVERSE.get(value, value)
    variants = STRINGS.get(canonical)
    if variants is None or language == "zh-cn":
        return canonical
    return variants[0 if language == "en" else 1]
