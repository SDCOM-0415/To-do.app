# TodoApp — 跨平台待办事项管理器（Tk 版本）

TodoApp 是使用 Python 与 **CustomTkinter** 开发的桌面待办事项工具，支持 Windows、Linux 和 macOS。当前 Tk 应用版本为 **0.3.2**。本分支继续维护轻量桌面版；Flet 版本和历史版本分别由独立分支维护。

## 主要功能

- 创建、编辑、完成和删除任务，支持标题与备注。
- 设置任务优先级、截止日期，搜索和排序任务。
- 支持深色、浅色及跟随系统的主题模式。
- 可切换界面字体：默认内置 HarmonyOS Sans SC，或选择当前平台系统中文字体。字体原件和授权文件存放在 `res/fonts/`，随安装包分发。
- **双 UI 模式**：经典界面完整保留，新增侧栏式现代工作空间；通过「应用设置 → 外观 → 主界面布局」切换，立即生效并记住选择。
- 现代界面提供全部任务、进行中、已完成导航，同时沿用原有搜索、排序、任务操作及本地数据。
- 显示任务统计，支持用户偏好设置和 JSON 数据保存。
- 跨平台构建 Windows、Linux、macOS Intel 与 Apple Silicon 安装包。

## 下载与安装

在 [GitHub Releases](https://github.com/SDCOM-0415/To-do.app/releases) 中选择文件名前缀为 **`TodoApp-`** 的安装包，不要与 **`TodoApp-Flet-`** 混淆。

| 平台 | Tk 版本安装包命名示例 |
|---|---|
| Windows x64 | `TodoApp-v0.3.2-20261110-1-Windows-x64.zip` |
| Linux x64 | `TodoApp-v0.3.2-20261110-1-Linux-x64.tar.gz` |
| macOS Intel | `TodoApp-v0.3.2-20261110-1-macOS-x64.zip` |
| macOS Apple Silicon | `TodoApp-v0.3.2-20261110-1-macOS-arm64.zip` |

示例文件名对应一次预发布；请以 Release 页面实际提供的最新版本为准。macOS 安装包为包含 `.app` 的 ZIP 压缩文件，而不是 DMG。若 macOS 阻止打开未经签名或公证的应用，请按系统安全提示处理。

## 字体选择及随包分发

在「应用设置 → 外观 → 界面字体」选择 **HarmonyOS Sans SC（默认）** 或 **系统字体**。
Windows 的系统字体采用 `Microsoft YaHei UI`，macOS 为 `PingFang SC`，
Linux 为 `Noto Sans CJK SC`（该字体若未安装则由系统回退）。字体模式保存在
`tk-config.json` 中，重启后保持不变。

出于安装包体积考虑，**仅使用简体中文 Regular 原始字重（8,261,128 字节）**，
不对字体进行子集化、转换或修改。原始字体及 `LICENSE.txt` 存放于
`res/fonts/`，版权归 Huawei Device Co., Ltd. 所有。
字体授权允许随应用分发未经修改的原始文件，完整条款请参见随包提供的
`LICENSE.txt`。

构建工作流会调用 `prepare_fonts.py`，从
[华为官方字体包](https://developer.huawei.com/images/download/general/HarmonyOS-Sans.zip)
提取文件并校验 SHA-256，再一起打包；无需在 Git 仓库中存放大型二进制字体。
在本地构建或运行源码前也可以执行：

```bash
python prepare_fonts.py --edition tk --zip /path/to/HarmonyOS-Sans.zip
```

省略 `--zip` 参数则尝试下载官方 ZIP。字体文件不存在时，Tk 会回退到系统字体；
Flet 原生构建应先完成资源准备，以确保默认字体真正打包。

## 从源码运行

建议使用 **Python 3.12**。先安装 Python、pip，并确保 tkinter/Tcl/Tk 可用。

```bash
git clone --branch main https://github.com/SDCOM-0415/To-do.app.git
cd To-do.app
python -m pip install -r requirements.txt
python app.py
```

Linux 若缺少 tkinter，可使用仓库提供的 `install_linux_tkinter.sh`，或使用发行版包管理器安装 `python3-tk`。Windows 需确保 Python 安装时包含 Tcl/Tk 支持。

## 源码目录

| 文件 | 用途 |
|---|---|
| `app.py` | Tk 程序入口 |
| `main_app.py` | 主窗口、任务交互和双布局切换 |
| `modern_ui.py` | 新版侧栏工作空间 UI |
| `ui_components.py` | 可复用界面组件 |
| `settings_dialog.py` | 设置窗口 |
| `settings_manager.py`、`settings_utils.py` | 设置管理与辅助功能 |
| `models.py`、`database.py` | 任务模型、数据管理 |
| `config.py` | 程序配置与用户数据路径 |
| `build.spec`、`build.py` | PyInstaller 打包配置与辅助脚本 |
| `DUAL_RELEASE.md` | 双版本分支及联合发布说明 |

## 数据保存与版本兼容

Tk 与 Flet 使用同一份任务数据：

```text
platformdirs.user_data_path("TodoApp", "SDCOM")/
├── tasks.json          # 两个版本共享
├── tk-config.json      # Tk 的独立设置
└── flet-settings.json  # Flet 的独立设置
```

在 macOS 上，通常位于 `~/Library/Application Support/SDCOM/TodoApp/`。原 Tk 版本若曾将 `tasks.json`、`config.json` 放在应用包内部，新版本会在共享目标文件尚不存在时尝试复制迁移，保留旧文件不动。切换版本前建议自行备份任务；不要让两个程序同时修改同一任务，以免互相覆盖。

## 分支与构建

- **[main](https://github.com/SDCOM-0415/To-do.app/tree/main)**：CustomTkinter 当前版本。
- **[flet-version](https://github.com/SDCOM-0415/To-do.app/tree/flet-version)**：基于 Flet 的独立版本，源码直接位于该分支根目录。
- **[old-version](https://github.com/SDCOM-0415/To-do.app/tree/old-version)**：历史 Qt 版和 v0.2 归档。

仅需验证 Tk 版 Intel Mac 时，可通过 [Tk macOS Intel 独立测试工作流](https://github.com/SDCOM-0415/To-do.app/actions/workflows/tk-macos-intel-test.yml) 单独构建：仅使用一个 `macos-26-intel` Runner，执行语法与单元测试、PyInstaller 打包和 x86_64 架构检查，生成 Actions Artifact `TodoApp-Tk-macOS-x64-test`，不创建 Release。该工作流只能手动执行，或在明确要求测试时通过提交 `.test-trigger/tk-macos-intel-0.3.2` 标记文件触发；普通代码提交不会自动构建。

两个现行版本由 [联合发布工作流](https://github.com/SDCOM-0415/To-do.app/actions/workflows/build-release.yml) 分别构建，再上传到同一个 GitHub Release。发布方式、命名和预发布编号见 [DUAL_RELEASE.md](DUAL_RELEASE.md)。

## 参与开发

请先阅读 [AGENTS.md](AGENTS.md)。新增 Git 提交信息及 README 统一使用简体中文，代码标识、命令及标准技术术语保留原文。欢迎通过 [Issues](https://github.com/SDCOM-0415/To-do.app/issues) 反馈问题，或提交 Pull Request。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。项目维护者：SDCOM。
