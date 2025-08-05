# Todo App v0.3 - 现代化跨平台待办事项管理器

一个使用 **customtkinter** 构建的现代化跨平台待办事项应用程序，支持深色/浅色模式切换，完美兼容 Windows、Linux、macOS 系统。

## 🌟 项目特色

- ✅ **跨平台支持**: Windows、Linux、macOS 原生支持
- 🌙 **深色模式**: 支持深色/浅色/系统主题自动切换
- 🎨 **现代化界面**: 基于 customtkinter 的美观现代化 UI
- ⚡ **轻量级**: 基于 Tkinter，无重型依赖
- 💾 **自动保存**: 智能自动保存，数据永不丢失
- 🔍 **智能搜索**: 实时搜索任务内容
- 📊 **统计分析**: 任务完成率和统计信息
- 🏷️ **优先级管理**: 高中低优先级分类
- 📅 **截止日期**: 任务截止日期提醒

## 📁 项目结构

```
Todo App v0.3/
├── app.py              # 🚀 程序入口文件
├── main_app.py         # 🏠 主应用程序
├── ui_components.py    # 🎨 UI组件模块
├── models.py           # 📋 数据模型
├── database.py         # 💾 数据库管理
├── config.py           # ⚙️ 配置管理
├── requirements.txt    # 📦 依赖包列表
├── README.md           # 📖 项目说明
├── todo_app.py         # 📜 旧版本（PySide6）
└── old version/        # 📂 历史版本存档
```

## 🛠️ 技术架构

### 核心模块说明

#### 1. `app.py` - 程序入口
- 系统环境检测和初始化
- 依赖包检查
- DPI 感知设置（Windows）
- 异常处理和错误报告

#### 2. `main_app.py` - 主应用程序
- `TodoApp` 主窗口类
- 界面布局和交互逻辑
- 主题切换和设置管理
- 任务的增删改查操作

#### 3. `ui_components.py` - UI组件
- `TaskEditDialog` - 任务编辑对话框
- `TaskItem` - 任务列表项组件
- `StatisticsFrame` - 统计信息面板
- 自定义界面组件实现

#### 4. `models.py` - 数据模型
- `Task` 任务数据类
- 任务属性和方法定义
- 数据验证和转换
- 优先级和日期处理

#### 5. `database.py` - 数据库管理
- `TaskDatabase` 数据管理类
- JSON 文件存储
- 任务的 CRUD 操作
- 搜索、排序、统计功能

#### 6. `config.py` - 配置管理
- `Config` 配置管理类
- 用户设置持久化
- 主题和界面配置
- 跨平台路径处理

## 🚀 快速开始

### 环境要求
- Python 3.7+
- 支持的操作系统: Windows 10+, macOS 10.14+, Ubuntu 18.04+

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd Todo-App-v0.3
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **运行程序**
```bash
python app.py
```

## 📖 使用指南

### 基本操作

1. **添加任务**
   - 在输入框中输入任务标题，按回车快速添加
   - 点击"详细添加"按钮设置优先级、描述、截止日期

2. **管理任务**
   - 点击复选框标记任务完成/未完成
   - 点击"编辑"按钮修改任务信息
   - 点击"删除"按钮删除任务

3. **任务筛选**
   - 使用搜索框实时搜索任务
   - 选择排序方式：创建时间、优先级、截止日期等
   - 切换显示/隐藏已完成任务

4. **主题切换**
   - 点击工具栏的 🌙 按钮切换深色/浅色模式
   - 支持跟随系统主题设置

### 高级功能

- **统计信息**: 右侧面板显示任务完成率和统计数据
- **批量操作**: 快捷清除已完成任务或所有任务
- **数据导出**: 将任务数据导出为 JSON 格式
- **自动保存**: 每30秒自动保存，程序关闭时保存设置

## 🔧 配置说明

配置文件位置：
- 所有系统: 软件根目录下

配置文件：
- `config.json` - 应用设置
- `tasks.json` - 任务数据

配置文件与程序文件存放在同一目录，便于备份和迁移。

## 🎨 自定义主题

支持的主题模式：
- `dark` - 深色模式
- `light` - 浅色模式  
- `system` - 跟随系统

优先级颜色自定义：
```json
{
  "priority_colors": {
    "高": "#ff4444",
    "中": "#ffaa00",
    "低": "#44ff44"
  }
}
```

## 🔄 版本历史

### v0.3 (当前版本)
- 🆕 完全重构，使用 customtkinter 框架
- 🆕 现代化界面设计
- 🆕 改进的跨平台支持
- 🆕 模块化架构设计
- 🆕 增强的主题系统
- 🆕 实时搜索功能
- 🆕 统计信息面板

### v0.2 (PySide6 版本)
- 基于 PySide6 (Qt) 的实现
- 支持深色模式
- 任务优先级和截止日期
- 右键菜单操作

### v0.1 (原始版本)
- 基础的任务管理功能
- 简单的界面设计

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境设置
1. Fork 项目
2. 创建功能分支: `git checkout -b feature/new-feature`
3. 提交更改: `git commit -am 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 提交 Pull Request

### 代码规范
- 使用中文注释和文档字符串
- 遵循 PEP 8 代码风格
- 保持模块单一职责
- 添加类型提示

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- 项目作者: SDCOM
- 项目主页: [GitHub Repository]
- 问题反馈: [Issues Page]

## 🙏 致谢

感谢以下开源项目：
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) - 现代化 Tkinter 界面框架
- [Python](https://python.org) - 强大的编程语言

---

**Todo App v0.3** - 让任务管理变得简单而美观 ✨