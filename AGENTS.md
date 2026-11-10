# AGENTS.md — TodoApp Tk 主分支协作规范

本文件约束在 **`main`** 分支上工作的开发者与 AI 编程代理。

## 分支定位

- 当前桌面版使用 Python + CustomTkinter，入口为 `app.py`，主窗口在 `main_app.py`。
- 通过 `build.spec`、PyInstaller 和 `.github/workflows/build-release.yml` 构建及联合发布。
- Flet 版本由 `flet-version` 单独维护，历史项目在 `old-version`，不得把这些实现复制回主分支。
- 主分支负责联合 Release：分别检出 `main`、`flet-version` 的提交，构建两个版本并按文件名区分。
- 任务数据位于 `platformdirs.user_data_path("TodoApp", "SDCOM")/tasks.json`。Tk 设置独立保存为 `tk-config.json`；Flet 设置为 `flet-settings.json`。

## Git 提交与文字规范

1. **参考本仓库历史 Git 提交格式，允许使用英文 Conventional Commits 类型前缀；描述和正文必须使用简体中文。** 推荐写法：`fix: 修复主题切换问题`、`feat(flet): 增加窗口标题栏适配`、`docs: 更新中文使用说明`、`ci: 优化手动构建流程`。
2. 可使用 `feat:`、`fix:`、`docs:`、`refactor:`、`test:`、`ci:`、`build:`、`chore:`、`release:` 等英文前缀，也可以在括号中标识范围，例如 `fix(tk): 修复配置路径`。不要使用全英文描述（如 `fix: update readme`）。
3. 允许提交标题不使用前缀，但标题描述仍应为中文；不改写历史提交记录。英文技术标识、程序名、版本号、路径、参数、API 等无需翻译。
4. 所有新建或修改的 **README.md 必须以简体中文撰写**，可保留代码、命令、路径、专业名词、项目名称及参数键名。
5. 新增用户文档、注释和开发说明以中文为主；既有英文代码注释无需为了统一风格而机械改写。
6. 修改目录、运行方式、版本、依赖或构建流程时，同步更新 README，不能将未经验证的构建或运行情况写成已通过。

## GitHub Actions 执行策略

- Flet 独立构建只能通过 `workflow_dispatch` 手动启动，禁止添加自动 Push 触发器。
- Tk macOS Intel 独立测试工作流为 `.github/workflows/tk-macos-intel-test.yml`。仅用户明确要求时，允许通过 `main` 的 `.test-trigger/tk-macos-intel-0.3.2` 专用标记文件触发；只使用一个 Intel Mac Runner、只上传测试 Artifact，不创建 Release 或启动其他构建。
- `main` 联合发布默认仅手动触发；**用户明确授权发布时**，允许通过创建一次性 `.release-trigger/0.3.2-prerelease` 文件触发限定为 `main` 和该路径的 Push 工作流。
- 不得扩大成对普通代码、文档提交或 PR 的自动构建；禁止加入 `schedule` 等无关触发器。
- 每次新的联合发布均须有用户明确要求，且应检查已有标签、版本编号以及发布产物，不得覆盖旧 Release。
- CI 失败时先调查日志，修改配置后也不要自动重新运行；等待用户明确指示。

## 工作流程

- 修改前确认当前所在分支及工作树内容，不跨分支混入另一个 UI 框架的源码。
- 优先进行最小范围改动，保证跨平台兼容；不要擅自更改任务 JSON 数据结构。
- 涉及数据迁移必须保留原文件，避免覆盖用户已有任务；保留 Tk 与 Flet 对共享任务目录的约定。
- 提交前运行本分支相关的语法、单元测试；没有实际运行的检查不得宣称通过。
- 除非用户明确要求，否则不创建、覆盖 Git 标签或发布 Release；不修改已发布的历史版本。
- 遇到系统或 SDK 平台限制时，说明限制并优先做可复现验证。


## Tk 分支验证

```bash
python -m compileall -q app.py main_app.py config.py database.py models.py settings_dialog.py
python -m unittest discover -s . -p "test_*.py" -v
```

运行界面前安装 `requirements.txt`，打包要在相应操作系统原生 Runner 上执行。发布工作流变更须验证两个版本的实际路径与产物名称。
