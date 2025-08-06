"""
配置文件 - Todo App v0.3
支持 Windows、Linux、macOS 多系统
"""
import os
import json
from pathlib import Path
from typing import Dict, Any

class Config:
    def __init__(self):
        self.app_name = "Todo App v0.3"
        self.version = "0.3.0"
        
        # 配置文件路径 - 存放在软件根目录
        self.config_dir = Path(__file__).parent
        self.config_file = self.config_dir / "config.json"
        self.tasks_file = self.config_dir / "tasks.json"
        
        # 确保配置目录存在
        self.config_dir.mkdir(exist_ok=True)
        
        # 默认配置
        self.default_config = {
            "theme": "system",  # dark, light, system
            "window_size": "900x700",
            "window_position": "center",
            "auto_save": True,
            "show_completed": True,
            "font_size": 14,
            "language": "zh-cn",
            "priority_colors": {
                "高": "#ff4444",
                "中": "#ffaa00", 
                "低": "#44ff44"
            }
        }
        
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置，确保所有键都存在
                for key, value in self.default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except Exception as e:
                print(f"加载配置失败: {e}")
                return self.default_config.copy()
        else:
            return self.default_config.copy()
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def get(self, key: str, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        self.config[key] = value
        self.save_config()
    
    def get_priority_color(self, priority: str) -> str:
        """获取优先级颜色"""
        colors = self.config.get("priority_colors", self.default_config["priority_colors"])
        return colors.get(priority, "#ffaa00")

# 全局配置实例
app_config = Config()