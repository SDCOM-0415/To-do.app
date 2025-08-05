"""
配置文件
包含应用程序的所有配置信息
"""

import os

# 应用配置
APP_TITLE = "待办事项管理器"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MIN_WINDOW_WIDTH = 600
MIN_WINDOW_HEIGHT = 400

# 数据库配置
DATABASE_FILE = "tasks.json"

# 字体配置
FONT_PATH = os.path.join("res", "NotoSansSC.ttf")
DEFAULT_FONT_FAMILY = "Microsoft YaHei"
DEFAULT_FONT_SIZE = 10

# 颜色配置
COLORS = {
    'bg_primary': '#f0f0f0',
    'bg_secondary': '#ffffff',
    'text_primary': '#333333',
    'text_secondary': '#666666',
    'accent': '#007acc',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'border': '#cccccc'
}

# UI配置
PADDING = 10
BUTTON_HEIGHT = 35
ENTRY_HEIGHT = 30
LISTBOX_HEIGHT = 15

# 任务状态
TASK_STATUS = {
    'PENDING': '待完成',
    'COMPLETED': '已完成'
}

# 优先级
PRIORITY_LEVELS = {
    'LOW': '低',
    'MEDIUM': '中',
    'HIGH': '高'
}