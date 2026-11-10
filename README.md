# TodoApp Flet — 跨平台待办事项管理器

这是 TodoApp 的 **Flet / Flutter 独立桌面版本**，当前应用版本为 **0.3.2**。本分支仅包含 Flet 实现，代码直接放在根目录；Tk 版本请查看 [main](https://github.com/SDCOM-0415/To-do.app/tree/main)。

## 主要功能

- 新建、编辑、完成及删除任务，支持优先级、截止日期、备注、搜索与排序。
- 左侧工作空间导航，快速查看全部任务、进行中与已完成任务。
- 完整设置页面，支持数据管理、优先级颜色、窗口偏好、设置备份等功能。
- 十种可切换界面风格，通过「应用设置 → 外观 → 界面风格」选择并保存：
  - **Graphite Focus**：石墨深色与柔和紫色。
  - **Paper & Ink**：暖白色与低饱和绿色。
  - **Blue Hour**：深蓝色与冷青色。
  - **Nord Frost**：冰川浅灰蓝与沉稳北欧蓝。
  - **Forest Studio**：墨绿色与苔绿色。
  - **Rose Quartz**：淡粉米白与柔和玫瑰色。
  - **Solar Sand**：浅沙色与温暖赭橙。
  - **Midnight OLED**：近黑色与薄荷青色。
  - **Lavender Mist**：雾紫浅色与薰衣草紫。
  - **Copper Dusk**：暖灰深色与赤铜色。
- macOS 使用 Flet 的自定义标题栏方案，使原生红绿灯按钮与应用界面尽可能协调；效果需在目标 macOS 环境实际验证。

## 下载与运行

从 [GitHub Releases](https://github.com/SDCOM-0415/To-do.app/releases) 下载以 **`TodoApp-Flet-`** 开头的安装包，勿与 Tk 版的 `TodoApp-` 混淆。

| 平台 | Flet 版本安装包命名示例 |
|---|---|
| Windows x64 | `TodoApp-Flet-v0.3.2-20261110-1-Windows-x64.zip` |
| Linux x64 | `TodoApp-Flet-v0.3.2-20261110-1-Linux-x64.tar.gz` |
| macOS Intel | `TodoApp-Flet-v0.3.2-20261110-1-macOS-x64.zip` |
| macOS Apple Silicon | `TodoApp-Flet-v0.3.2-20261110-1-macOS-arm64.zip` |

这些是历史预发布的示例文件名，实际版本以 Release 页面为准。macOS 下载内容为 `.app` 应用包的 ZIP 压缩文件。

## 源码运行

需要 **Python 3.12**。在此分支根目录执行：

```bash
git clone --branch flet-version https://github.com/SDCOM-0415/To-do.app.git
cd To-do.app
python -m pip install -r requirements.txt
python main.py
```

## 项目结构

| 文件 | 用途 |
|---|---|
| `main.py` | Flet 应用入口和任务工作空间 |
| `appearance.py` | 十种预设界面风格的统一配色配置 |
| `settings_ui.py` | 应用设置页面 |
| `window_chrome.py` | macOS 窗口标题栏适配 |
| `models.py` | 任务数据模型 |
| `storage.py` | JSON 任务持久化及旧数据迁移 |
| `pyproject.toml` | Flet 应用元数据与打包配置 |
| `requirements.txt` | Python 依赖 |
| `test_*.py` | 单元测试 |
| `.github/workflows/flet-build.yml` | Flet 四平台构建工作流 |

本分支不包含 Tk 的 `app.py`、PyInstaller 构建脚本或历史 `old version/` 目录。

## 数据与设置

Flet 与 Tk 版本共用 `platformdirs.user_data_path("TodoApp", "SDCOM")/tasks.json`，但保留各自配置文件：Flet 使用 `flet-settings.json`，Tk 使用 `tk-config.json`。

支持在共享目标文件不存在时尝试迁移旧的本地 JSON 数据，原文件保持不变。两个程序可以独立安装，但**不要同时编辑相同任务**，以免后写入的数据覆盖先前修改。建议更新前备份任务文件。

## 构建与发布

需要构建时可手动运行 [Flet 独立构建](https://github.com/SDCOM-0415/To-do.app/actions/workflows/flet-build.yml)，为 Windows x64、Linux x64、macOS Intel 和 Apple Silicon 构建测试产物。该工作流不会自动创建 Release。

正式及预发布由 [main 分支的联合发布工作流](https://github.com/SDCOM-0415/To-do.app/actions/workflows/build-release.yml) 统一处理，分别检出两个版本的源码，全部八项构建成功后才发布。

## 开发约定与许可证

参与修改前请阅读 [AGENTS.md](AGENTS.md)。新提交信息与 README 使用简体中文；专业术语、API 和代码命令保留原文。本项目采用 [MIT 许可证](LICENSE)。
