"""
设置工具 - Todo App v0.3
提供设置相关的实用工具函数
"""
import json
import os
from typing import Dict, Any, List, Tuple
from pathlib import Path
from datetime import datetime
from config import app_config

class SettingsBackup:
    """设置备份管理器"""
    
    def __init__(self):
        self.backup_dir = Path(app_config.config_dir) / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        self.max_backups = 10  # 最多保留10个备份
    
    def create_backup(self, description: str = "") -> Tuple[bool, str]:
        """创建设置备份
        
        Args:
            description: 备份描述
            
        Returns:
            tuple: (success, message)
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"settings_backup_{timestamp}.json"
            backup_path = self.backup_dir / backup_filename
            
            backup_data = {
                "timestamp": timestamp,
                "description": description or "手动备份",
                "app_version": app_config.version,
                "settings": app_config.config.copy()
            }
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            # 清理旧备份
            self._cleanup_old_backups()
            
            return True, f"备份已创建: {backup_filename}"
            
        except Exception as e:
            return False, f"创建备份失败: {str(e)}"
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """列出所有备份"""
        backups = []
        
        try:
            for backup_file in self.backup_dir.glob("settings_backup_*.json"):
                try:
                    with open(backup_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    backups.append({
                        "filename": backup_file.name,
                        "path": str(backup_file),
                        "timestamp": data.get("timestamp", "未知"),
                        "description": data.get("description", "无描述"),
                        "app_version": data.get("app_version", "未知"),
                        "size": backup_file.stat().st_size
                    })
                except Exception:
                    continue
            
            # 按时间戳排序
            backups.sort(key=lambda x: x["timestamp"], reverse=True)
            
        except Exception:
            pass
        
        return backups
    
    def restore_backup(self, backup_path: str) -> Tuple[bool, str]:
        """恢复备份
        
        Args:
            backup_path: 备份文件路径
            
        Returns:
            tuple: (success, message)
        """
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            if "settings" not in backup_data:
                return False, "无效的备份文件格式"
            
            # 创建当前设置的备份
            self.create_backup("恢复前自动备份")
            
            # 恢复设置
            app_config.config = backup_data["settings"]
            app_config.save_config()
            
            return True, "设置已从备份恢复"
            
        except Exception as e:
            return False, f"恢复备份失败: {str(e)}"
    
    def delete_backup(self, backup_path: str) -> Tuple[bool, str]:
        """删除备份
        
        Args:
            backup_path: 备份文件路径
            
        Returns:
            tuple: (success, message)
        """
        try:
            Path(backup_path).unlink()
            return True, "备份已删除"
        except Exception as e:
            return False, f"删除备份失败: {str(e)}"
    
    def _cleanup_old_backups(self):
        """清理旧备份"""
        try:
            backups = list(self.backup_dir.glob("settings_backup_*.json"))
            if len(backups) > self.max_backups:
                # 按修改时间排序，删除最旧的
                backups.sort(key=lambda x: x.stat().st_mtime)
                for old_backup in backups[:-self.max_backups]:
                    old_backup.unlink()
        except Exception:
            pass

class SettingsPresets:
    """设置预设管理器"""
    
    def __init__(self):
        self.presets = {
            "默认": {
                "theme": "dark",
                "window_size": "900x700",
                "font_size": 14,
                "auto_save": True,
                "show_completed": True,
                "show_statistics": True,
                "confirm_delete": True,
                "language": "zh-cn",
                "priority_colors": {
                    "高": "#ff4444",
                    "中": "#ffaa00", 
                    "低": "#44ff44"
                }
            },
            "简洁模式": {
                "theme": "light",
                "window_size": "800x600",
                "font_size": 12,
                "auto_save": True,
                "show_completed": False,
                "show_statistics": False,
                "confirm_delete": True,
                "language": "zh-cn",
                "priority_colors": {
                    "高": "#e74c3c",
                    "中": "#f39c12", 
                    "低": "#27ae60"
                }
            },
            "专业模式": {
                "theme": "dark",
                "window_size": "1200x800",
                "font_size": 16,
                "auto_save": True,
                "show_completed": True,
                "show_statistics": True,
                "confirm_delete": True,
                "language": "zh-cn",
                "priority_colors": {
                    "高": "#dc3545",
                    "中": "#ffc107", 
                    "低": "#28a745"
                }
            }
        }
    
    def get_preset_names(self) -> List[str]:
        """获取所有预设名称"""
        return list(self.presets.keys())
    
    def get_preset(self, name: str) -> Dict[str, Any]:
        """获取指定预设"""
        return self.presets.get(name, {})
    
    def apply_preset(self, name: str) -> Tuple[bool, str]:
        """应用预设
        
        Args:
            name: 预设名称
            
        Returns:
            tuple: (success, message)
        """
        if name not in self.presets:
            return False, f"预设 '{name}' 不存在"
        
        try:
            preset_settings = self.presets[name]
            
            # 应用预设设置
            for key, value in preset_settings.items():
                app_config.set(key, value)
            
            return True, f"已应用预设: {name}"
            
        except Exception as e:
            return False, f"应用预设失败: {str(e)}"

class SettingsValidator:
    """设置验证器"""
    
    @staticmethod
    def validate_config_integrity() -> Tuple[bool, List[str]]:
        """验证配置完整性
        
        Returns:
            tuple: (is_valid, error_messages)
        """
        errors = []
        
        # 检查必需的配置项
        required_keys = [
            "theme", "window_size", "font_size", "auto_save",
            "show_completed", "language", "priority_colors"
        ]
        
        for key in required_keys:
            if key not in app_config.config:
                errors.append(f"缺少必需的配置项: {key}")
        
        # 检查配置文件是否可写
        try:
            app_config.save_config()
        except Exception as e:
            errors.append(f"配置文件不可写: {str(e)}")
        
        # 检查配置目录权限
        if not os.access(app_config.config_dir, os.W_OK):
            errors.append("配置目录没有写入权限")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def repair_config() -> Tuple[bool, str]:
        """修复配置
        
        Returns:
            tuple: (success, message)
        """
        try:
            # 合并默认配置
            for key, value in app_config.default_config.items():
                if key not in app_config.config:
                    app_config.config[key] = value
            
            # 保存修复后的配置
            app_config.save_config()
            
            return True, "配置已修复"
            
        except Exception as e:
            return False, f"修复配置失败: {str(e)}"

# 全局实例
settings_backup = SettingsBackup()
settings_presets = SettingsPresets()
settings_validator = SettingsValidator()