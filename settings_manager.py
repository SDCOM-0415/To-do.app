"""
设置管理器 - Todo App v0.3
统一管理应用程序设置的验证、应用和持久化
"""
import json
import re
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
from config import app_config

class SettingsManager:
    """设置管理器"""
    
    def __init__(self):
        self.validators = {
            "theme": self._validate_theme,
            "window_size": self._validate_window_size,
            "font_size": self._validate_font_size,
            "language": self._validate_language,
            "priority_colors": self._validate_priority_colors,
            "auto_save": self._validate_boolean,
            "show_completed": self._validate_boolean,
            "show_statistics": self._validate_boolean,
            "confirm_delete": self._validate_boolean,
        }
    
    def validate_setting(self, key: str, value: Any) -> Tuple[bool, str]:
        """验证单个设置项
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if key not in self.validators:
            return True, ""  # 未知设置项，允许通过
        
        return self.validators[key](value)
    
    def validate_all_settings(self, settings: Dict[str, Any]) -> Tuple[bool, list]:
        """验证所有设置项
        
        Returns:
            tuple: (all_valid, error_messages)
        """
        errors = []
        
        for key, value in settings.items():
            is_valid, error_msg = self.validate_setting(key, value)
            if not is_valid:
                errors.append(f"{key}: {error_msg}")
        
        return len(errors) == 0, errors
    
    def apply_settings(self, settings: Dict[str, Any]) -> Tuple[bool, list]:
        """应用设置
        
        Returns:
            tuple: (success, error_messages)
        """
        # 首先验证所有设置
        is_valid, errors = self.validate_all_settings(settings)
        if not is_valid:
            return False, errors
        
        # 应用设置
        try:
            for key, value in settings.items():
                app_config.set(key, value)
            return True, []
        except Exception as e:
            return False, [f"应用设置时发生错误: {str(e)}"]
    
    def export_settings(self, filepath: str) -> Tuple[bool, str]:
        """导出设置到文件
        
        Returns:
            tuple: (success, message)
        """
        try:
            export_data = {
                "app_name": app_config.app_name,
                "app_version": app_config.version,
                "export_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "settings": app_config.config.copy()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            return True, f"设置已成功导出到: {filepath}"
        except Exception as e:
            return False, f"导出设置失败: {str(e)}"
    
    def import_settings(self, filepath: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """从文件导入设置
        
        Returns:
            tuple: (success, message, settings_data)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if "settings" not in data:
                return False, "无效的设置文件格式：缺少 'settings' 字段", None
            
            settings = data["settings"]
            
            # 验证导入的设置
            is_valid, errors = self.validate_all_settings(settings)
            if not is_valid:
                error_msg = "导入的设置包含无效值:\n" + "\n".join(errors)
                return False, error_msg, None
            
            return True, "设置文件验证通过", settings
            
        except json.JSONDecodeError:
            return False, "无效的JSON文件格式", None
        except FileNotFoundError:
            return False, "找不到指定的设置文件", None
        except Exception as e:
            return False, f"导入设置失败: {str(e)}", None
    
    def reset_to_defaults(self) -> Tuple[bool, str]:
        """重置所有设置为默认值
        
        Returns:
            tuple: (success, message)
        """
        try:
            app_config.config = app_config.default_config.copy()
            app_config.save_config()
            return True, "所有设置已重置为默认值"
        except Exception as e:
            return False, f"重置设置失败: {str(e)}"
    
    def get_setting_info(self, key: str) -> Dict[str, Any]:
        """获取设置项的详细信息"""
        info_map = {
            "theme": {
                "name": "主题模式",
                "description": "应用程序的外观主题",
                "type": "choice",
                "choices": ["dark", "light", "system"],
                "default": "dark"
            },
            "window_size": {
                "name": "窗口大小",
                "description": "应用程序启动时的默认窗口大小",
                "type": "string",
                "pattern": r"^\d+x\d+$",
                "default": "900x700"
            },
            "font_size": {
                "name": "字体大小",
                "description": "界面文字的字体大小",
                "type": "integer",
                "min": 10,
                "max": 20,
                "default": 14
            },
            "language": {
                "name": "界面语言",
                "description": "应用程序界面显示语言",
                "type": "choice",
                "choices": ["zh-cn", "en", "zh-tw"],
                "default": "zh-cn"
            },
            "priority_colors": {
                "name": "优先级颜色",
                "description": "不同优先级任务的颜色配置",
                "type": "dict",
                "default": {"高": "#ff4444", "中": "#ffaa00", "低": "#44ff44"}
            },
            "auto_save": {
                "name": "自动保存",
                "description": "是否启用自动保存功能",
                "type": "boolean",
                "default": True
            },
            "show_completed": {
                "name": "显示已完成任务",
                "description": "是否默认显示已完成的任务",
                "type": "boolean",
                "default": True
            },
            "show_statistics": {
                "name": "显示统计面板",
                "description": "是否显示任务统计信息面板",
                "type": "boolean",
                "default": True
            },
            "confirm_delete": {
                "name": "删除确认",
                "description": "删除任务时是否需要确认",
                "type": "boolean",
                "default": True
            }
        }
        
        return info_map.get(key, {
            "name": key,
            "description": "未知设置项",
            "type": "unknown",
            "default": None
        })
    
    # 验证器方法
    def _validate_theme(self, value: Any) -> Tuple[bool, str]:
        """验证主题设置"""
        valid_themes = ["dark", "light", "system"]
        if value not in valid_themes:
            return False, f"主题必须是以下值之一: {', '.join(valid_themes)}"
        return True, ""
    
    def _validate_window_size(self, value: Any) -> Tuple[bool, str]:
        """验证窗口大小设置"""
        if not isinstance(value, str):
            return False, "窗口大小必须是字符串格式"
        
        pattern = r"^\d+x\d+$"
        if not re.match(pattern, value):
            return False, "窗口大小格式必须是 '宽度x高度'，如 '900x700'"
        
        width, height = map(int, value.split('x'))
        if width < 800 or height < 600:
            return False, "窗口大小不能小于 800x600"
        if width > 3840 or height > 2160:
            return False, "窗口大小不能大于 3840x2160"
        
        return True, ""
    
    def _validate_font_size(self, value: Any) -> Tuple[bool, str]:
        """验证字体大小设置"""
        if not isinstance(value, int):
            return False, "字体大小必须是整数"
        
        if value < 10 or value > 20:
            return False, "字体大小必须在 10-20 之间"
        
        return True, ""
    
    def _validate_language(self, value: Any) -> Tuple[bool, str]:
        """验证语言设置"""
        valid_languages = ["zh-cn", "en", "zh-tw"]
        if value not in valid_languages:
            return False, f"语言必须是以下值之一: {', '.join(valid_languages)}"
        return True, ""
    
    def _validate_priority_colors(self, value: Any) -> Tuple[bool, str]:
        """验证优先级颜色设置"""
        if not isinstance(value, dict):
            return False, "优先级颜色必须是字典格式"
        
        required_keys = ["高", "中", "低"]
        for key in required_keys:
            if key not in value:
                return False, f"缺少优先级 '{key}' 的颜色设置"
            
            color = value[key]
            if not isinstance(color, str):
                return False, f"优先级 '{key}' 的颜色必须是字符串"
            
            # 验证颜色格式（十六进制）
            if not re.match(r"^#[0-9a-fA-F]{6}$", color):
                return False, f"优先级 '{key}' 的颜色格式无效，必须是十六进制格式如 '#ff4444'"
        
        return True, ""
    
    def _validate_boolean(self, value: Any) -> Tuple[bool, str]:
        """验证布尔值设置"""
        if not isinstance(value, bool):
            return False, "该设置必须是布尔值（True 或 False）"
        return True, ""

# 全局设置管理器实例
settings_manager = SettingsManager()