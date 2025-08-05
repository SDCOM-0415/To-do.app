#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
待办事项应用程序 - 文字配置文件
包含所有界面文字、提示信息和状态消息的中文配置
"""

class TextConfig:
    """文字配置类，包含所有界面文字和消息"""
    
    # 应用程序基本信息
    APP_TITLE = "SDCOM 待办事项管理器"
    APP_VERSION = "v2.0"
    APP_DESCRIPTION = "一个简单而美观的跨平台待办事项应用"
    
    # 主界面文字
    MAIN_TITLE = "📋 我的待办事项"
    INPUT_PLACEHOLDER = "✏️ 输入新任务内容..."
    ADD_BUTTON = "➕ 添加任务"
    
    # 任务编辑对话框
    EDIT_DIALOG_TITLE = "编辑任务"
    TASK_CONTENT_LABEL = "任务内容:"
    PRIORITY_LABEL = "优先级:"
    DUE_DATE_LABEL = "截止日期:"
    CONFIRM_BUTTON = "确认"
    CANCEL_BUTTON = "取消"
    
    # 优先级选项
    PRIORITY_LOW = "低"
    PRIORITY_MEDIUM = "中"
    PRIORITY_HIGH = "高"
    
    # 任务状态
    TASK_COMPLETED = "已完成"
    TASK_PENDING = "未完成"
    DUE_DATE_PREFIX = "截止: "
    DUE_TODAY = "今天到期"
    DUE_OVERDUE = "已过期: "
    DUE_SOON = "即将到期: "
    
    # 按钮提示
    EDIT_TOOLTIP = "编辑"
    DELETE_TOOLTIP = "删除"
    
    # 菜单栏
    MENU_FILE = "📁 文件"
    MENU_VIEW = "👁️ 视图"
    MENU_DEBUG = "🔧 调试"
    MENU_HELP = "❓ 帮助"
    
    # 文件菜单项
    ACTION_NEW_TASK = "📝 新建任务"
    ACTION_SAVE = "💾 保存任务"
    ACTION_CLEAR_ALL = "🗑️ 清空所有任务"
    ACTION_EXIT = "🚪 退出程序"
    
    # 视图菜单项
    ACTION_SHOW_COMPLETED = "✅ 显示已完成任务"
    ACTION_SORT_PRIORITY = "🔥 按优先级排序"
    ACTION_SORT_DATE = "📅 按截止日期排序"
    ACTION_TOGGLE_THEME = "🌙 切换深色/浅色模式"
    
    # 调试菜单项
    ACTION_DEBUG_BORDERS = "🔍 检测界面边框状态"
    
    # 帮助菜单项
    ACTION_ABOUT = "ℹ️ 关于本程序"
    
    # 状态栏消息
    STATUS_READY = "🚀 系统已就绪，开始管理您的待办事项"
    STATUS_TASK_ADDED = "✅ 任务添加成功: {}"
    STATUS_QUICK_ADD_SUCCESS = "✅ 快速添加成功: {}"
    STATUS_TASK_DELETED = "🗑️ 任务已删除"
    STATUS_TASK_COMPLETED = "✅ 任务标记为已完成"
    STATUS_TASK_PENDING = "⏳ 任务标记为未完成"
    STATUS_TASK_UPDATED = "📝 任务已更新: {}"
    STATUS_TASKS_LOADED = "📂 任务已加载"
    STATUS_TASKS_CLEARED = "🧹 所有任务已清空"
    STATUS_SORTED_BY_PRIORITY = "🔥 已按优先级排序"
    STATUS_SORTED_BY_DATE = "📅 已按截止日期排序"
    STATUS_THEME_SWITCHED = "✨ 已切换到{}模式"
    
    # 主题名称
    THEME_DARK = "🌙 深色"
    THEME_LIGHT = "☀️ 浅色"
    
    # 确认对话框
    CONFIRM_DELETE_TITLE = "确认删除"
    CONFIRM_DELETE_MESSAGE = "确定要删除任务 '{}' 吗？"
    CONFIRM_CLEAR_TITLE = "确认清空"
    CONFIRM_CLEAR_MESSAGE = "确定要清空所有任务吗？"
    
    # 警告和错误消息
    WARNING_EMPTY_TASK = "请输入任务内容"
    WARNING_TITLE = "提示"
    ERROR_LOAD_TASKS = "无法加载任务: {}"
    ERROR_SAVE_TASKS = "无法保存任务: {}"
    ERROR_LOAD_TITLE = "加载错误"
    ERROR_SAVE_TITLE = "保存错误"
    
    # 关于对话框
    ABOUT_TITLE = "关于待办事项应用"
    ABOUT_MESSAGE = """SDCOM的待办项目 v2.0

一个简单而美观的跨平台待办事项应用
使用 PySide6 (Qt for Python) 构建

支持 Windows, macOS 和 Linux
支持深色/浅色模式自动切换
彻底去除所有界面元素边框"""
    
    # 右键菜单
    CONTEXT_EDIT = "编辑"
    CONTEXT_DELETE = "删除"
    
    # 调试信息
    DEBUG_BORDER_INFO = "=== QListWidget边框调试信息 ==="
    DEBUG_STYLE_SET = "已设置调试样式，请检查界面中的红色和蓝色边框"
    DEBUG_FONT_LOADED = "已加载字体: {}"
    DEBUG_FONT_LOAD_FAILED = "字体加载失败，使用默认字体"
    DEBUG_FONT_FILE_FAILED = "字体文件加载失败，使用默认字体"
    DEBUG_FONT_NOT_FOUND = "字体文件不存在: {}，使用默认字体"
    DEBUG_CURRENT_STYLE = "当前样式引擎: {}"
    DEBUG_LISTWIDGET_SETUP = "QListWidget无边框设置完成"
    
    # 优先级颜色配置
    PRIORITY_COLORS = {
        PRIORITY_LOW: "#28a745",    # 绿色
        PRIORITY_MEDIUM: "#ffc107", # 黄色
        PRIORITY_HIGH: "#dc3545"    # 红色
    }
    
    # 优先级提示文字
    PRIORITY_TOOLTIP = "{}优先级"
    
    @classmethod
    def get_priority_tooltip(cls, priority):
        """获取优先级提示文字"""
        return cls.PRIORITY_TOOLTIP.format(priority)
    
    @classmethod
    def get_task_status_message(cls, is_completed):
        """获取任务状态消息"""
        return cls.STATUS_TASK_COMPLETED if is_completed else cls.STATUS_TASK_PENDING
    
    @classmethod
    def get_theme_name(cls, is_dark_mode):
        """获取主题名称"""
        return cls.THEME_DARK if is_dark_mode else cls.THEME_LIGHT
    
    @classmethod
    def get_sort_status_message(cls, sort_by):
        """获取排序状态消息"""
        if sort_by == "priority":
            return cls.STATUS_SORTED_BY_PRIORITY
        elif sort_by == "due_date":
            return cls.STATUS_SORTED_BY_DATE
        return ""