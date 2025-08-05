"""
设置模块测试 - Todo App v0.3
测试设置功能的完整性和正确性
"""
import unittest
import tempfile
import json
from pathlib import Path
from config import Config
from settings_manager import SettingsManager
from settings_utils import SettingsBackup, SettingsPresets, SettingsValidator

class TestSettingsModule(unittest.TestCase):
    """设置模块测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时配置目录
        self.temp_dir = tempfile.mkdtemp()
        self.test_config = Config()
        self.test_config.config_dir = Path(self.temp_dir)
        self.test_config.config_file = self.test_config.config_dir / "test_config.json"
        
        self.settings_manager = SettingsManager()
        self.settings_backup = SettingsBackup()
        self.settings_presets = SettingsPresets()
    
    def test_config_validation(self):
        """测试配置验证"""
        # 测试有效配置
        valid_settings = {
            "theme": "dark",
            "window_size": "900x700",
            "font_size": 14,
            "language": "zh-cn",
            "auto_save": True,
            "priority_colors": {
                "高": "#ff4444",
                "中": "#ffaa00",
                "低": "#44ff44"
            }
        }
        
        is_valid, errors = self.settings_manager.validate_all_settings(valid_settings)
        self.assertTrue(is_valid, f"有效配置验证失败: {errors}")
        
        # 测试无效配置
        invalid_settings = {
            "theme": "invalid_theme",
            "window_size": "invalid_size",
            "font_size": "not_a_number",
            "language": "invalid_lang"
        }
        
        is_valid, errors = self.settings_manager.validate_all_settings(invalid_settings)
        self.assertFalse(is_valid, "无效配置应该验证失败")
        self.assertGreater(len(errors), 0, "应该有错误信息")
    
    def test_settings_export_import(self):
        """测试设置导出导入"""
        # 创建测试设置
        test_settings = {
            "theme": "light",
            "window_size": "1024x768",
            "font_size": 16
        }
        
        # 导出设置
        export_file = Path(self.temp_dir) / "test_export.json"
        success, message = self.settings_manager.export_settings(str(export_file))
        self.assertTrue(success, f"导出失败: {message}")
        self.assertTrue(export_file.exists(), "导出文件不存在")
        
        # 验证导出内容
        with open(export_file, 'r', encoding='utf-8') as f:
            export_data = json.load(f)
        
        self.assertIn("settings", export_data, "导出数据缺少settings字段")
        self.assertIn("app_version", export_data, "导出数据缺少版本信息")
        
        # 导入设置
        success, message, imported_settings = self.settings_manager.import_settings(str(export_file))
        self.assertTrue(success, f"导入失败: {message}")
        self.assertIsNotNone(imported_settings, "导入的设置为空")
    
    def test_settings_backup(self):
        """测试设置备份"""
        # 创建备份
        success, message = self.settings_backup.create_backup("测试备份")
        self.assertTrue(success, f"创建备份失败: {message}")
        
        # 列出备份
        backups = self.settings_backup.list_backups()
        self.assertGreater(len(backups), 0, "应该有至少一个备份")
        
        # 验证备份内容
        backup = backups[0]
        self.assertIn("filename", backup, "备份信息缺少文件名")
        self.assertIn("timestamp", backup, "备份信息缺少时间戳")
        self.assertIn("description", backup, "备份信息缺少描述")
    
    def test_settings_presets(self):
        """测试设置预设"""
        # 获取预设列表
        preset_names = self.settings_presets.get_preset_names()
        self.assertGreater(len(preset_names), 0, "应该有预设可用")
        
        # 测试获取预设
        for name in preset_names:
            preset = self.settings_presets.get_preset(name)
            self.assertIsInstance(preset, dict, f"预设 {name} 应该是字典类型")
            self.assertGreater(len(preset), 0, f"预设 {name} 不应该为空")
    
    def test_individual_setting_validation(self):
        """测试单个设置项验证"""
        # 测试主题验证
        is_valid, error = self.settings_manager.validate_setting("theme", "dark")
        self.assertTrue(is_valid, f"有效主题验证失败: {error}")
        
        is_valid, error = self.settings_manager.validate_setting("theme", "invalid")
        self.assertFalse(is_valid, "无效主题应该验证失败")
        
        # 测试窗口大小验证
        is_valid, error = self.settings_manager.validate_setting("window_size", "900x700")
        self.assertTrue(is_valid, f"有效窗口大小验证失败: {error}")
        
        is_valid, error = self.settings_manager.validate_setting("window_size", "invalid")
        self.assertFalse(is_valid, "无效窗口大小应该验证失败")
        
        # 测试字体大小验证
        is_valid, error = self.settings_manager.validate_setting("font_size", 14)
        self.assertTrue(is_valid, f"有效字体大小验证失败: {error}")
        
        is_valid, error = self.settings_manager.validate_setting("font_size", 100)
        self.assertFalse(is_valid, "过大的字体大小应该验证失败")
    
    def test_priority_colors_validation(self):
        """测试优先级颜色验证"""
        # 有效的优先级颜色
        valid_colors = {
            "高": "#ff4444",
            "中": "#ffaa00",
            "低": "#44ff44"
        }
        
        is_valid, error = self.settings_manager.validate_setting("priority_colors", valid_colors)
        self.assertTrue(is_valid, f"有效优先级颜色验证失败: {error}")
        
        # 无效的优先级颜色 - 缺少键
        invalid_colors = {
            "高": "#ff4444",
            "中": "#ffaa00"
            # 缺少"低"
        }
        
        is_valid, error = self.settings_manager.validate_setting("priority_colors", invalid_colors)
        self.assertFalse(is_valid, "缺少优先级的颜色配置应该验证失败")
        
        # 无效的颜色格式
        invalid_format_colors = {
            "高": "red",  # 不是十六进制格式
            "中": "#ffaa00",
            "低": "#44ff44"
        }
        
        is_valid, error = self.settings_manager.validate_setting("priority_colors", invalid_format_colors)
        self.assertFalse(is_valid, "无效颜色格式应该验证失败")

def run_settings_tests():
    """运行设置模块测试"""
    print("=" * 50)
    print("Todo App v0.3 - 设置模块测试")
    print("=" * 50)
    
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSettingsModule)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出结果
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ 所有测试通过！设置模块功能正常。")
    else:
        print("❌ 部分测试失败，请检查设置模块。")
        print(f"失败: {len(result.failures)}, 错误: {len(result.errors)}")
    print("=" * 50)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_settings_tests()