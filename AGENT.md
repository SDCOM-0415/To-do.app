# AGENT.md — TodoApp Flet 分支协作规范

本文件约束在 **`flet-version`** 分支上工作的开发者与 AI 编程代理。

## 分支定位

- 本分支只维护 Python + Flet/Flutter 桌面版，入口为根目录的 `main.py`。
- `appearance.py` 管理三套界面主题，`settings_ui.py` 管理设置页，`window_chrome.py` 管理平台窗口外观。
- `storage.py` 与 `models.py` 负责任务存储及兼容；`pyproject.toml` 定义 Flet 应用标识。
- **不要引入 Tk、PyInstaller、`old version/` 或旧的 `flet_port/` 嵌套目录。**
- 单独 CI 在 `.github/workflows/flet-build.yml`，联合发布由 `main` 负责。
- 任务文件与 Tk 版共享 `platformdirs.user_data_path("TodoApp", "SDCOM")/tasks.json`，但 Flet 设置只使用 `flet-settings.json`。

## Git 提交与文字规范

1. **从现在起，所有新的 Git 提交标题和正文都必须使用中文。** 包括功能开发、修复、重构、测试、文档和 CI 修改。允许保留 Python、Flet、Tk、CI、API、文件名、参数及其他不可替代的技术标识。
2. 提交标题使用简洁的中文动宾表达，推荐格式为 `功能：……`、`修复：……`、`重构：……`、`测试：……`、`文档：……` 或 `构建：……`。
3. 不使用英文描述作为提交标题，例如 `fix: update readme`；改用 `文档：更新项目说明`。不要求改写历史提交记录。
4. 所有新建或修改的 **README.md 必须以简体中文撰写**。可保留代码、命令、路径、专业名词、项目名称、链接地址，以及必要的参数键名。
5. 新增的用户可见文档、注释及开发说明以简体中文为主；修改既有代码时无需为此批量重写原有英文注释。
6. 文档与代码行为要一致：修改目录、运行方式、版本、依赖或构建流程时同步更新对应 README，严禁编造已经验证成功的构建结果。

## 工作流程

- 修改前确认当前所在分支及工作树内容，不跨分支混入另一个 UI 框架的源码。
- 优先进行最小范围改动，保证跨平台兼容；不要擅自更改任务 JSON 数据结构。
- 涉及数据迁移必须保留原文件，避免覆盖用户已有任务；保留 Tk 与 Flet 对共享任务目录的约定。
- 提交前运行本分支相关的语法、单元测试；没有实际运行的检查不得宣称通过。
- 除非用户明确要求，否则不创建、覆盖 Git 标签或发布 Release；不修改已发布的历史版本。
- 遇到系统或 SDK 平台限制时，说明限制并优先做可复现验证。


## Flet 分支验证

```bash
python -m compileall -q main.py models.py storage.py settings_ui.py appearance.py window_chrome.py
python -m unittest discover -s . -p "test_*.py" -v
```

应使用 Python 3.12 与本分支的 `requirements.txt`；需在对应平台通过 `flet build` 验证安装包。macOS 自定义标题栏必须保留系统原生窗口按钮，且主题切换不能破坏已有设置。
