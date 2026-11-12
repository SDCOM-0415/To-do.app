"""UI translations shared by the Tk and Flet editions.

The JSON task schema and priority identifiers remain in Chinese for compatibility.
Only UI labels and messages are translated. Unknown/user-generated strings are not changed.
"""
from __future__ import annotations

import re

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
MORE_STRINGS = {
    "选取": ("Pick", "選取"),
    "选择语言后点击应用或确定，界面会立即更新。": ("Choose a language, then click Apply or OK to update the interface.", "選擇語言後按「套用」或「確定」，介面會立即更新。"),
    "点击选取以可视化调整 RGB，或直接输入 #RRGGBB 色号。": ("Use Pick to adjust RGB visually, or enter a #RRGGBB hex value.", "按「選取」以視覺化調整 RGB，或直接輸入 #RRGGBB 色碼。"),
    "拖动红、绿、蓝滑块调整颜色": ("Use the red, green and blue sliders to adjust the color", "拖曳紅、綠、藍滑桿調整顏色"),
    "颜色已恢复默认值；点击应用或确定保存。": ("Default colors restored; click Apply or OK to save.", "已還原預設顏色；按「套用」或「確定」儲存。"),
    "调试与数据目录": ("Debug & data paths", "偵錯與資料目錄"),
    "功能": ("Features", "功能"),
    "任务与显示": ("Tasks and display", "任務與顯示"),
    "删除前确认": ("Confirm before deleting", "刪除前確認"),
    "选择语言后点击应用或确定": ("Apply language selection", "套用語言選項"),
    "独立于 Tk 版本保存，可随时切换。": ("Saved separately from Tk; switch any time.", "與 Tk 版分開儲存，可隨時切換。"),
    "鸿蒙字体默认内置；系统字体会按 Windows / macOS / Linux 自动选择。": ("HarmonyOS Sans is bundled by default; system fonts depend on your OS.", "預設內建鴻蒙字體；系統字體依 Windows / macOS / Linux 自動選擇。"),
    "任务标题和部分界面文字的字号。": ("Controls task titles and selected UI text sizes.", "調整任務標題及部分介面文字的大小。"),
    "下次启动时按照保存的尺寸打开。": ("Used the next time the app launches.", "下次啟動時使用儲存的視窗大小。"),
    "启用后立即保存任务；关闭后使用主界面的保存按钮。": ("Save tasks immediately; otherwise use the Save button.", "啟用後立即儲存任務；停用時請使用儲存按鈕。"),
    "在任务列表中显示或隐藏已完成项目。": ("Show or hide completed tasks in the list.", "在清單中顯示或隱藏已完成任務。"),
    "显示任务总数、已完成及逾期数量。": ("Show task totals, completed and overdue counts.", "顯示任務總數、完成數及逾期數。"),
    "删除单条任务前弹出确认提示。": ("Ask before deleting a task.", "刪除單一任務前先確認。"),
    "支持当前 Flet 版以及原 Tk 版导出的设置 JSON。": ("Supports settings JSON from Flet and Tk editions.", "支援 Flet 及 Tk 版本匯出的 JSON 設定。"),
    "最多保留最近 10 份 Flet 设置备份，不影响任务数据。": ("Retain up to 10 Flet settings backups; tasks are unaffected.", "最多保留最近 10 份 Flet 設定備份，不影響任務資料。"),
    "技术栈：Python · Flet · Flutter": ("Built with Python · Flet · Flutter", "技術：Python · Flet · Flutter"),
    "技术栈: Python 3.12 + CustomTkinter": ("Stack: Python 3.12 + CustomTkinter", "技術：Python 3.12 + CustomTkinter"),
    "任务名称": ("Task name", "任務名稱"),
    "备注": ("Notes", "備註"),
    "优先级颜色必须使用 #RRGGBB 格式": ("Priority color must be #RRGGBB", "優先級顏色必須使用 #RRGGBB 格式"),
    "确定删除任务吗？": ("Delete this task?", "確定刪除任務嗎？"),
    "添加任务": ("Add task", "新增任務"),
    "导出": ("Export", "匯出"),
    "导入": ("Import", "匯入"),
    "恢复默认": ("Restore defaults", "還原預設"),
    "高优先级": ("High priority", "高優先級"),
    "中优先级": ("Medium priority", "中優先級"),
    "低优先级": ("Low priority", "低優先級"),
    "高优先级:": ("High priority:", "高優先級："),
    "中优先级:": ("Medium priority:", "中優先級："),
    "低优先级:": ("Low priority:", "低優先級："),
    "选择高优先级颜色": ("Pick high priority color", "選取高優先級顏色"),
    "选择中优先级颜色": ("Pick medium priority color", "選取中優先級顏色"),
    "点击色块直接选择颜色": ("Click a swatch to choose a color", "點選色塊直接選擇顏色"),
    "选择低优先级颜色": ("Pick low priority color", "選取低優先級顏色"),
    "HarmonyOS Sans SC（内置，默认）": ("HarmonyOS Sans SC (bundled, default)", "HarmonyOS Sans SC（內建，預設）"),
    "系统字体（跟随当前平台）": ("System font (OS default)", "系統字體（依目前平台）"),
    "系统字体（按操作系统选择）": ("System font (per operating system)", "系統字體（依作業系統選擇）"),
    "确认清除": ("Confirm clear", "確認清除"),
    "总计": ("Total", "總計"),
    "未设置": ("Not set", "未設定"),
    "任务已保存": ("Task saved", "任務已儲存"),
    "更改已应用": ("Changes applied", "變更已套用"),
    "设置已保存": ("Settings saved", "設定已儲存"),
    "请选择有效日期": ("Enter a valid date", "請輸入有效日期"),
    "确认导入": ("Confirm import", "確認匯入"),
    "打开日期选择器": ("Open date picker", "開啟日期選擇器"),
    "YYYY/MM/DD（可选）": ("YYYY/MM/DD (optional)", "YYYY/MM/DD（選填）"),
    "保存后同步更新任务列表。": ("The task list updates after saving.", "儲存後同步更新任務清單。"),
    "输入任务，按回车创建": ("Type a task and press Enter", "輸入任務後按 Enter 建立"),
    "添加任务或调整筛选条件": ("Add a task or adjust the filters", "新增任務或調整篩選條件"),
}
MORE_STRINGS.update({
    "跟随系统": ("Follow system", "跟隨系統"),
    "深色模式": ("Dark mode", "深色模式"),
    "浅色模式": ("Light mode", "淺色模式"),
    "经典界面（原版）": ("Classic interface (original)", "經典介面（原版）"),
    "现代工作空间（新版）": ("Modern workspace (new)", "現代工作空間（新版）"),
    "操作系统": ("Operating system", "作業系統"),
    "系统架构": ("Architecture", "系統架構"),
    "架构": ("Architecture", "架構"),
    "Python 版本": ("Python version", "Python 版本"),
    "版本": ("Version", "版本"),
    "设置已成功保存": ("Settings saved successfully", "設定已成功儲存"),
    "任务默认排序": ("Default task sort", "預設任務排序"),
    "恢复默认颜色": ("Restore default colors", "還原預設顏色"),
    "设置已应用": ("Settings applied", "設定已套用"),
})
MORE_STRINGS.update({
    "现代化跨平台待办事项管理器\n支持 Windows、Linux、macOS 和深色模式": ("Modern cross-platform task manager\nSupports Windows, Linux, macOS and dark mode", "現代跨平台待辦事項管理器\n支援 Windows、Linux、macOS 與深色模式"),
    "✅ 任务创建、编辑和删除": ("✅ Create, edit and delete tasks", "✅ 建立、編輯與刪除任務"),
    "✅ 优先级设置（高、中、低）": ("✅ Priority levels (high, medium, low)", "✅ 優先級設定（高、中、低）"),
    "✅ 截止日期管理": ("✅ Due date management", "✅ 截止日期管理"),
    "✅ 任务分类和标签": ("✅ Task categories and tags", "✅ 任務分類與標籤"),
    "✅ 搜索和过滤功能": ("✅ Search and filtering", "✅ 搜尋與篩選"),
    "✅ 统计信息面板": ("✅ Task statistics", "✅ 統計資訊面板"),
    "✅ 深色/浅色主题切换": ("✅ Dark/light themes", "✅ 深色／淺色主題切換"),
    "✅ 自动保存功能": ("✅ Automatic saving", "✅ 自動儲存"),
    "✅ 数据导入导出": ("✅ Data import/export", "✅ 資料匯入匯出"),
    "✅ 跨平台支持": ("✅ Cross-platform support", "✅ 跨平台支援"),
    "配置文件": ("Config file", "設定檔"),
    "任务文件": ("Task file", "任務檔案"),
    "邮箱": ("Email", "電子郵件"),
    "个人网站": ("Website", "個人網站"),
    "错误": ("Error", "錯誤"),
    "导出成功": ("Export successful", "匯出成功"),
    "导入成功": ("Import successful", "匯入成功"),
    "保存失败": ("Save failed", "儲存失敗"),
    "颜色格式无效": ("Invalid color format", "顏色格式無效"),
    "设置已导出": ("Settings exported", "設定已匯出"),
    "设置已载入；点击应用或确定保存": ("Settings loaded; click Apply or OK to save", "已載入設定；按「套用」或「確定」儲存"),
    "备份已载入；点击应用或确定保存": ("Backup loaded; click Apply or OK to save", "已載入備份；按「套用」或「確定」儲存"),
    "请先选择备份": ("Select a backup first", "請先選擇備份"),
    "备份已删除": ("Backup deleted", "備份已刪除"),
    "已恢复默认值；点击应用或确定保存": ("Defaults restored; click Apply or OK to save", "已還原預設值；按「套用」或「確定」儲存"),
    "选择备份": ("Select backup", "選擇備份"),
    "截止日期（YYYY/MM/DD，可留空）": ("Due date (YYYY/MM/DD, optional)", "截止日期（YYYY/MM/DD，可留空）"),
    "例如 2026/11/11，输入数字自动补 /": ("e.g. 2026/11/11; slashes are inserted automatically", "例如 2026/11/11，輸入數字會自動補 /"),
    "标签（逗号分隔）": ("Tags (comma-separated)", "標籤（以逗號分隔）"),
    "请填写任务名称": ("Enter a task name", "請輸入任務名稱"),
    "请输入有效日期（YYYY/MM/DD）": ("Enter a valid date (YYYY/MM/DD)", "請輸入有效日期（YYYY/MM/DD）"),
    "导出待办任务": ("Export tasks", "匯出待辦任務"),
    "导入待办任务": ("Import tasks", "匯入待辦任務"),
    "暂无已完成任务": ("No completed tasks", "暫無已完成任務"),
    "数据目录": ("Data directory", "資料目錄"),
    "文件": ("File", "檔案"),
    "设置已应用": ("Settings applied", "設定已套用"),
    "导出失败": ("Export failed", "匯出失敗"),
    "导入失败": ("Import failed", "匯入失敗"),
    "应用失败": ("Apply failed", "套用失敗"),
    "重置完成": ("Reset complete", "重設完成"),
    "重置失败": ("Reset failed", "重設失敗"),
    "确认重置": ("Confirm reset", "確認重設"),
    "操作失败": ("Operation failed", "操作失敗"),
    "日期无效": ("Invalid date", "日期無效"),
    "请输入任务标题": ("Enter a task title", "請輸入任務標題"),
    "请使用 YYYY/MM/DD 格式输入有效日期": ("Enter a valid date in YYYY/MM/DD format", "請以 YYYY/MM/DD 格式輸入有效日期"),
})
MORE_STRINGS.update({
    "深色石墨与淡紫色强调": ("Dark graphite with soft lavender accents", "深色石墨搭配淡紫色點綴"),
    "暖白纸张与低饱和绿色": ("Warm white paper with muted green", "暖白紙張搭配低飽和綠色"),
    "深海蓝与冷青色强调": ("Deep ocean blue with cool cyan accents", "深海藍搭配冷青色點綴"),
    "冰川浅灰蓝与沉稳的北欧蓝": ("Icy blue-gray with classic Nordic blue", "冰川淺灰藍搭配沉穩北歐藍"),
    "墨绿工作台与柔和苔绿色": ("Forest green with soft moss accents", "墨綠工作台搭配柔和苔綠色"),
    "淡粉米白与柔和玫瑰色": ("Soft blush ivory and rose", "淡粉米白搭配柔和玫瑰色"),
    "浅沙色纸面与温暖赭橙": ("Pale sand with warm ochre orange", "淺沙色紙面搭配溫暖赭橙"),
    "雾紫浅色与雅致的薰衣草紫": ("Misty violet and lavender", "霧紫淺色搭配雅緻薰衣草紫"),
    "暖灰深色与内敛的赤铜色": ("Warm charcoal with copper accents", "暖灰深色搭配內斂赤銅色"),
    "近黑色界面与清透薄荷青": ("Near-black surfaces with mint accents", "近黑色介面搭配清透薄荷青"),
    "Flet 配置文件": ("Flet settings file", "Flet 設定檔"),
    "Tk 配置文件": ("Tk settings file", "Tk 設定檔"),
    "共享任务文件": ("Shared tasks file", "共用任務檔案"),
    "备份失败": ("Backup failed", "備份失敗"),
    "恢复失败": ("Restore failed", "還原失敗"),
    "删除备份失败": ("Delete backup failed", "刪除備份失敗"),
    "导出失败": ("Export failed", "匯出失敗"),
    "导入失败": ("Import failed", "匯入失敗"),
    "已创建备份": ("Backup created", "已建立備份"),
    "已导出": ("Exported", "已匯出"),
    "已删除任务": ("Task deleted", "已刪除任務"),
    "已添加任务": ("Task added", "已新增任務"),
    "已更新任务": ("Task updated", "已更新任務"),
    "保存失败": ("Save failed", "儲存失敗"),
    "无法保存设置": ("Unable to save settings", "無法儲存設定"),
})
MORE_STRINGS.update({
    "设置已成功保存": ("Settings saved successfully", "設定已成功儲存"),
    "导入设置将覆盖当前设置，是否继续？": ("Import settings and overwrite current preferences?", "匯入設定將覆蓋目前設定，是否繼續？"),
    "设置已导入，请重启应用程序以应用所有更改": ("Settings imported. Restart the app to apply all changes.", "設定已匯入，請重新啟動應用程式以套用所有變更。"),
    "确定要重置所有设置为默认值吗？此操作不可恢复！": ("Reset all settings to defaults? This cannot be undone.", "確定將所有設定還原成預設值嗎？此操作無法復原！"),
    "确定要清除所有已完成的任务吗？": ("Clear all completed tasks?", "確定要清除所有已完成的任務嗎？"),
    "确定要清除所有任务吗？此操作不可恢复！": ("Clear all tasks? This cannot be undone.", "確定清除所有任務嗎？此操作無法復原！"),
    "已清除所有已完成任务": ("All completed tasks cleared", "已清除所有已完成任務"),
    "已清除所有任务": ("All tasks cleared", "已清除所有任務"),
    "添加任务失败": ("Failed to add task", "新增任務失敗"),
    "更新任务失败": ("Failed to update task", "更新任務失敗"),
    "删除任务失败": ("Failed to delete task", "刪除任務失敗"),
    "清除任务失败": ("Failed to clear tasks", "清除任務失敗"),
    "设置应用时发生错误": ("Error while applying settings", "套用設定時發生錯誤"),
    "确认删除": ("Confirm deletion", "確認刪除"),
    "确认清除": ("Confirm clearing", "確認清除"),
    "导出失败": ("Export failed", "匯出失敗"),
    "颜色格式无效": ("Invalid color format", "顏色格式無效"),
    "请先选择备份": ("Select a backup first", "請先選擇備份"),
    "邮箱地址已复制": ("Email address copied", "電子郵件地址已複製"),
    "无法打开邮箱客户端或复制地址": ("Unable to open email app or copy address", "無法開啟電子郵件程式或複製地址"),
    "无法打开链接": ("Unable to open link", "無法開啟連結"),
    "保存设置时发生错误": ("Error saving settings", "儲存設定時發生錯誤"),
    "版本": ("Version", "版本"),
    "操作系统": ("Operating system", "作業系統"),
    "系统架构": ("Architecture", "系統架構"),
    "天后到期": ("days until due", "天後到期"),
    "今天到期": ("Due today", "今天到期"),
})
MORE_STRINGS.update({
    "📧 邮箱: ": ("📧 Email: ", "📧 電子郵件："),
    "🌐 个人网站: ": ("🌐 Website: ", "🌐 個人網站："),
    "打开链接失败": ("Failed to open link", "開啟連結失敗"),
    "启动错误": ("Startup error", "啟動錯誤"),
    "日期格式不正确": ("Invalid date format", "日期格式不正確"),
    "日期超出允许范围": ("Date out of range", "日期超出允許範圍"),
    "应用导入的设置时发生错误:\n": ("Error applying imported settings:\n", "套用匯入設定時發生錯誤：\n"),
    "邮箱地址已复制": ("Email address copied", "電子郵件地址已複製"),
    "保存设置时发生错误": ("Error saving settings", "儲存設定時發生錯誤"),
    "程序启动失败": ("Application failed to start", "應用程式啟動失敗"),
    "无法读取任务数据": ("Cannot read task data", "無法讀取任務資料"),
    "任务已导出到": ("Tasks exported to", "任務已匯出至"),
    "导出任务时发生错误": ("Error exporting tasks", "匯出任務時發生錯誤"),
    "无法打开链接": ("Unable to open link", "無法開啟連結"),
    "错误": ("Error", "錯誤"),
    "截止": ("Due", "截止"),
    "已导出": ("Exported", "已匯出"),
})
MORE_STRINGS.update({
    "设置必须是 JSON 对象": ("Settings must be a JSON object", "設定必須是 JSON 物件"),
    "语言设置无效": ("Invalid language setting", "語言設定無效"),
    "排序设置无效": ("Invalid sort setting", "排序設定無效"),
    "字体大小应为 10–20": ("Font size must be 10–20", "字體大小必須為 10–20"),
    "窗口大小必须使用 宽度x高度 格式": ("Window size must use width x height", "視窗大小必須使用 寬度x高度 格式"),
    "窗口大小应介于 800×600 与 3840×2160 之间": ("Window size must be between 800×600 and 3840×2160", "視窗尺寸必須介於 800×600 與 3840×2160 之間"),
    "优先级颜色数据无效": ("Invalid priority color data", "優先級顏色資料無效"),
    "设置文件必须是 JSON 对象": ("Settings file must be a JSON object", "設定檔必須是 JSON 物件"),
    "任务数据必须是 JSON 数组": ("Task data must be a JSON array", "任務資料必須是 JSON 陣列"),
    "手动备份": ("Manual backup", "手動備份"),
    "保存失败": ("Save failed", "儲存失敗"),
})
STRINGS.update(MORE_STRINGS)

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
    # Counts are generated after each refresh; translate their label fragments.
    if language != "zh-cn":
        stats = re.fullmatch(
            r"总计 (\d+) 项  ·  已完成 (\d+)  ·  进行中 (\d+)  ·  逾期 (\d+)",
            canonical,
        )
        if stats:
            total, done, active, overdue = stats.groups()
            return (
                f"Total {total} · Completed {done} · Active {active} · Overdue {overdue}"
                if language == "en" else
                f"總計 {total} 項 · 已完成 {done} · 進行中 {active} · 逾期 {overdue}"
            )
        count_labels = {
            "总任务": ("Total tasks", "總任務"),
            "已完成": ("Completed", "已完成"),
            "待完成": ("Remaining", "待完成"),
            "已过期": ("Overdue", "已逾期"),
            "完成率": ("Completion", "完成率"),
        }
        for prefix, variants in count_labels.items():
            if re.fullmatch(re.escape(prefix) + r":\s*[0-9]+(?:\.[0-9]+)?%?", canonical):
                return variants[0 if language == "en" else 1] + canonical[len(prefix):]
    # System metadata and path labels contain a localized prefix plus runtime data.
    # Only match known label prefixes, never rewrite arbitrary user content.
    for prefix in ("操作系统", "Python 版本", "系统架构", "架构", "版本"):
        labels = STRINGS.get(prefix)
        if not labels:
            continue
        for source_label in (prefix, *labels):
            match = re.fullmatch(re.escape(source_label) + r"([：:]\s*)(.+)", canonical)
            if match:
                translated_prefix = prefix if language == "zh-cn" else labels[0 if language == "en" else 1]
                return translated_prefix + match.group(1) + match.group(2)
    # About/status text with a runtime year or version.
    match = re.fullmatch(r"版权所有 © (\d{4}) SDCOM", canonical)
    if match:
        return (f"Copyright © {match.group(1)} SDCOM" if language == "en"
                else f"版權所有 © {match.group(1)} SDCOM" if language == "zh-tw"
                else canonical)
    match = re.fullmatch(r"版本\s+([0-9]+(?:\.[0-9]+)*)", canonical)
    if match:
        return (f"Version {match.group(1)}" if language == "en"
                else f"版本 {match.group(1)}")
    # User-facing dialog and validation templates, never touch task data.
    match = re.fullmatch(r"确定要删除任务 '(.+)' 吗？", canonical)
    if match:
        return (f"Delete task '{match.group(1)}'?" if language == "en"
                else f"確定刪除任務「{match.group(1)}」嗎？" if language == "zh-tw"
                else canonical)
    match = re.fullmatch(r"(高|中|低)优先级颜色必须使用 #RRGGBB 格式", canonical)
    if match:
        return (f"{tr(match.group(1), language)} priority color must be #RRGGBB" if language == "en"
                else f"{match.group(1)}優先級顏色必須使用 #RRGGBB 格式" if language == "zh-tw"
                else canonical)
    match = re.fullmatch(r"(高|中|低)优先级颜色应为 #RRGGBB，例如 #FF4444", canonical)
    if match:
        return (f"{tr(match.group(1), language)} priority color must be #RRGGBB, e.g. #FF4444" if language == "en"
                else f"{match.group(1)}優先級顏色應為 #RRGGBB，例如 #FF4444" if language == "zh-tw"
                else canonical)
    match = re.fullmatch(r"(.+) 必须为布尔值", canonical)
    if match:
        return (f"{match.group(1)} must be a boolean" if language == "en"
                else f"{match.group(1)} 必須為布林值" if language == "zh-tw"
                else canonical)
    # User-visible Tk dialogs that interpolate paths, email or error details.
    match = re.fullmatch(r"邮箱地址 (.+) 已复制到剪贴板", canonical)
    if match:
        return (f"Email address {match.group(1)} copied to clipboard" if language == "en"
                else f"電子郵件地址 {match.group(1)} 已複製到剪貼簿" if language == "zh-tw"
                else canonical)
    match = re.fullmatch(r"无法打开链接[:：] (.+)\n错误[:：] (.+)", canonical)
    if match:
        return (f"Unable to open link: {match.group(1)}\nError: {match.group(2)}" if language == "en"
                else f"無法開啟連結：{match.group(1)}\n錯誤：{match.group(2)}" if language == "zh-tw"
                else canonical)
    match = re.fullmatch(r"无法打开邮箱客户端或复制地址\n错误[:：] (.+)", canonical)
    if match:
        return (f"Unable to open email client or copy address\nError: {match.group(1)}" if language == "en"
                else f"無法開啟郵件程式或複製地址\n錯誤：{match.group(1)}" if language == "zh-tw"
                else canonical)
    # Interpolate UI templates without translating user task names or data.
    patterns = (
        (r"确定删除「(.+)」吗？", "Delete “{0}”?", "確定刪除「{0}」嗎？"),
        (r"确定删除 (\d+) 项已完成任务吗？",
         "Delete {0} completed tasks?", "確定刪除 {0} 項已完成任務嗎？"),
        (r"导入 (\d+) 条任务将替换当前全部 (\d+) 条任务。确定吗？",
         "Import {0} tasks and replace all {1} existing tasks?",
         "匯入 {0} 條任務並取代現有的 {1} 條任務，確定嗎？"),
        (r"已导入 (\d+) 条任务", "Imported {0} tasks", "已匯入 {0} 條任務"),
        (r"已过期 (\d+) 天", "Overdue by {0} days", "已逾期 {0} 天"),
        (r"(\d+) 天后到期", "Due in {0} days", "{0} 天後到期"),
        (r"截止: (.+)", "Due: {0}", "截止：{0}"),
        (r"任务已标记为(完成|未完成)", "Task marked {0}", "任務已標記為{0}"),
    )
    for pattern, english, traditional in patterns:
        match = re.fullmatch(pattern, canonical)
        if match:
            values = match.groups()
            if pattern.startswith("任务已标记"):
                values = (("completed" if values[0] == "完成" else "incomplete")
                          if language == "en" else values[0],)
            if language == "en":
                return english.format(*values)
            if language == "zh-tw":
                return traditional.format(*values)
    # Translate fixed UI prefixes while preserving filenames, platform data,
    # task titles, user-controlled content and numeric values unchanged.
    for prefix in ("配置文件", "任务文件", "邮箱", "个人网站", "数据目录",
                   "Flet 配置文件", "Tk 配置文件", "共享任务文件"):
        labels = STRINGS.get(prefix)
        if labels:
            for source_label in (prefix, *labels):
                match = re.fullmatch(re.escape(source_label) + r"([：:]\s*)(.+)", canonical)
                if match:
                    target = prefix if language == "zh-cn" else labels[0 if language == "en" else 1]
                    return target + match.group(1) + match.group(2)
    for priority in ("高", "中", "低"):
        pattern = re.fullmatch(re.escape(priority) + r"(优先级[:：]?)", canonical)
        if pattern:
            item = "优先级:" if pattern.group(1).endswith((":", "：")) else "优先级"
            name = tr(priority, language)
            if language == "en":
                return name + (" priority:" if item.endswith(":") else " priority")
            if language == "zh-tw":
                return name + ("優先級：" if item.endswith(":") else "優先級")
    for source, translations in (
        ("已过期", ("Overdue", "已逾期")),
        ("天后到期", ("days until due", "天後到期")),
    ):
        match = re.fullmatch(re.escape(source) + r"\s+(\d+)\s+天", canonical)
        if match:
            return (translations[0] if language == "en" else translations[1]) + " " + match.group(1)
    # Runtime status messages: preserve filenames and error details verbatim.
    for prefix in ("保存设置时发生错误", "程序启动失败", "无法读取任务数据",
                   "任务已导出到", "导出任务时发生错误",
                   "备份失败", "恢复失败", "删除备份失败",
                   "导出失败", "导入失败", "已创建备份",
                   "已导出", "已删除任务", "已添加任务",
                   "已更新任务", "保存失败", "无法保存设置"):
        variants = STRINGS.get(prefix)
        if variants:
            match = re.fullmatch(re.escape(prefix) + r"([：:]\s*)(.+)", canonical)
            if match:
                translated = prefix if language == "zh-cn" else variants[0 if language == "en" else 1]
                return translated + match.group(1) + match.group(2)
    # Dynamic prefix + numeric suffix, generated after every task refresh.
    for prefix in ("总任务", "已完成", "待完成", "已过期", "完成率"):
        choices = STRINGS.get(prefix)
        if choices:
            match = re.fullmatch(re.escape(prefix) + r"([:：]\s*)([0-9]+(?:\.[0-9]+)?%?)", canonical)
            if match:
                value = match.group(2)
                if language == "en":
                    return choices[0] + ": " + value
                if language == "zh-tw":
                    return choices[1] + "：" + value
                return prefix + ": " + value
    # Preserve runtime numbers while translating the settings subtitle.
    style_count = re.fullmatch(r"TodoApp Flet · (\d+) 种外观风格", canonical)
    if style_count:
        count = style_count.group(1)
        if language == "en":
            return f"TodoApp Flet · {count} appearance presets"
        if language == "zh-tw":
            return f"TodoApp Flet · {count} 種外觀風格"
    variants = STRINGS.get(canonical)
    if variants is None or language == "zh-cn":
        return canonical
    return variants[0 if language == "en" else 1]
