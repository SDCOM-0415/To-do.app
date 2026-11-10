# AGENTS.md — TodoApp Flet 分支协作规范

本文件约束在 **`flet-version`** 分支上工作的开发者与 AI 编程代理。

## 分支定位

- 本分支只维护 Python + Flet/Flutter 桌面版，入口为根目录的 `main.py`。
- `appearance.py` 管理三套界面主题，`settings_ui.py` 管理设置页，`window_chrome.py` 管理平台窗口外观。
- `storage.py` 与 `models.py` 负责任务存储及兼容；`pyproject.toml` 定义 Flet 应用标识。
- **不要引入 Tk、PyInstaller、`old version/` 或旧的 `flet_port/` 嵌套目录。**
- 单独 CI 在 `.github/workflows/flet-build.yml`，联合发布由 `main` 负责。
- 任务文件与 Tk 版共享 `platformdirs.user_data_path("TodoApp", "SDCOM")/tasks.json`，但 Flet 设置只使用 `flet-settings.json`。

## Git 提交与文字规范

1. **参考本仓库历史 Git 提交格式，允许使用英文 Conventional Commits 类型前缀；描述和正文必须使用简体中文。** 推荐写法：`fix: 修复主题切换问题`、`feat(flet): 增加窗口标题栏适配`、`docs: 更新中文使用说明`、`ci: 优化手动构建流程`。
2. 可使用 `feat:`、`fix:`、`docs:`、`refactor:`、`test:`、`ci:`、`build:`、`chore:`、`release:` 等英文前缀，也可以在括号中标识范围，例如 `fix(tk): 修复配置路径`。不要使用全英文描述（如 `fix: update readme`）。
3. 允许提交标题不使用前缀，但标题描述仍应为中文；不改写历史提交记录。英文技术标识、程序名、版本号、路径、参数、API 等无需翻译。
4. 所有新建或修改的 **README.md 必须以简体中文撰写**，可保留代码、命令、路径、专业名词、项目名称及参数键名。
5. 新增用户文档、注释和开发说明以中文为主；既有英文代码注释无需为了统一风格而机械改写。
6. 修改目录、运行方式、版本、依赖或构建流程时，同步更新 README，不能将未经验证的构建或运行情况写成已通过。

## GitHub Actions 执行策略

- **所有构建与联合发布工作流仅允许手动触发（`workflow_dispatch`）。**
- 不要重新加入 `push`、`pull_request`、`schedule` 等自动构建触发器；避免文档及普通代码提交耗费跨平台 Runner 资源。
- 除非用户明确要求，禁止手动触发工作流、创建或覆盖标签、上传新 Release。
- CI 失败时先调查日志，修改配置后也不要自动重新运行；等待用户明确指示。

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
