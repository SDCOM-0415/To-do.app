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

- Flet 常规四平台构建仅允许手动触发（`workflow_dispatch`），不得对普通代码提交自动构建。
- 仅在用户明确要求测试 macOS Intel 且无可用 gh CLI 时，可在独立的 `flet-macos-intel-test.yml` 工作流中，通过 `flet-version` 的专用标记文件 `.test-trigger/macos-intel-0.3.2` 进行精确 Push 触发。此例外只占用一个 macOS Runner，不触发其他平台或 Release。
- 禁止将该例外扩大为任意 `push`、`pull_request`、`schedule` 等自动构建。
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

## GitHub Actions 六条流水线触发速查（2026-11-11 核对）

> **强制规则：专用标记文件 Push 是仅在执行环境没有可用且已认证的 GitHub CLI（\`gh\`）时才考虑的后备方案。存在可用的 \`gh\` 时必须优先使用 \`gh workflow run\`，不得为了省事修改标记文件。** 如果 \`gh\` 不可用但 GitHub Actions 网页手动操作可用，可直接选择 Run workflow；并非必须制造一次 Push。所有触发均须用户本次明确授权。不要改变工作流的 \`on:\` 条件来绕过限制。

### 列表：逐条对应工作流、触发分支和备用标记文件

| # | 工作流文件（\`.github/workflows/\` 下） | 触发所在分支 | 首选 \`gh\` CLI 命令（在仓库目录执行） | 仅在无可用 \`gh\` 时，可修改并 Push 的已有文件 | 执行内容 / 是否发布 |
| --- | --- | --- | --- | --- | --- |
| 1 | \`build-release.yml\` | \`main\` | \`gh workflow run build-release.yml --ref main -f version=v0.3.2 -F publish=true -F prerelease=true\` | **\`main\`**：\`.release-trigger/0.3.2-prerelease\` | Tk + Flet 八平台联合构建；Push 入口固定为 v0.3.2 预发布，八份产物校验通过后创建 Release |
| 2 | \`i18n-color-check.yml\` | \`main\` | \`gh workflow run i18n-color-check.yml --ref main\` | **\`main\`**：\`.test-trigger/i18n-color-check\` | 单个 Ubuntu Runner 检出两分支，运行语言、颜色等回归检查；不发布 |
| 3 | \`tk-macos-intel-test.yml\` | \`main\` | \`gh workflow run tk-macos-intel-test.yml --ref main\` | **\`main\`**：\`.test-trigger/tk-macos-intel-0.3.2\` | Tk macOS Intel x64 单平台测试包；不发布 |
| 4 | \`flet-build.yml\` | \`flet-version\` | \`gh workflow run flet-build.yml --ref flet-version\` | **无标记文件入口；仅 \`workflow_dispatch\`** | Flet Windows x64、Linux x64、macOS x64、macOS arm64 四平台构建；仅 Actions Artifacts，不发布 |
| 5 | \`flet-macos-intel-test.yml\` | \`flet-version\` | \`gh workflow run flet-macos-intel-test.yml --ref flet-version\` | **\`flet-version\`**：\`.test-trigger/macos-intel-0.3.2\` | Flet macOS Intel x64 单平台测试包；不发布 |
| 6 | \`flet-windows-macos-test.yml\` | \`flet-version\` | \`gh workflow run flet-windows-macos-test.yml --ref flet-version\` | **\`flet-version\`**：\`.test-trigger/flet-windows-macos-0.3.2\` | 同一次运行使用 Windows x64、macOS Intel x64 两个 Runner；不发布 |

\`gh workflow run\` 使用 GitHub CLI 的 Actions API，需要 CLI 已安装、身份认证成功且具有目标仓库 Actions 写入权限。部分仅存在于非默认分支的工作流，可能受 GitHub 对 \`workflow_dispatch\` 工作流注册、可见性和默认分支的限制；如果返回找不到工作流或无法分发，应检查实际 GitHub Actions 页面和权限，不得宣称已触发，也不得擅自修改 \`on:\`。

### 仅在无可用 gh CLI 时：标记文件后备流程

1. 先确认用户授权的**具体一条流水线**、目标分支、期望是“测试工件”还是“正式发布”，以及现有 Actions 中是否已有同并发组运行（多数流水线设置 \`cancel-in-progress: true\`）。已有运行时不得重复触发，避免取消前一次构建。
2. 对照上表选择**精确路径与分支**。文件已经存在时，必须编辑文件内容形成真实差异；通过 GitHub Contents API 更新时需提供刚获取的 blob SHA。切勿创建同名文件、改动不相关的标记、修改 workflow YAML 或对全部 Push 放开触发。
3. 先提交需要构建的实际代码及文档；**最后单独提交并 Push 该标记文件**到表中指定分支。GitHub 的 \`paths\` 过滤器才会匹配。提交 \`AGENTS.md\`、README 或普通源码本身不会启动这些受限 Push 工作流。
4. 通过 GitHub Actions 运行列表核对新 Run 的 \`event=push\`、工作流名称、分支与提交 SHA，确认状态已排队才称“触发成功”；\`in_progress\` 不是构建完成。
5. 查看全部 Job、测试及工件；只有完成并全部成功才能说“构建成功”。联合发布还须确认新 GitHub Release、预发布标志和八个平台附件及 SHA256SUMS。失败时先查日志，不经用户再次授权不得重跑或修改标记重复触发。
6. 对 \`flet-build.yml\` **绝对不能使用标记文件法**，因为它没有 \`push\` 触发器。无 \`gh\` CLI 时优先使用 GitHub Actions 网页 Run workflow；若网页和 Actions API 也不可用，则如实说明无法启动，不能伪称改文件就能触发。

### 有 gh CLI 时：常规触发和结果确认

从已认证且具有仓库权限的环境执行上表 \`gh workflow run\` 命令；可通过 \`gh run list --repo SDCOM-0415/To-do.app --limit 10\` 找到新运行，通过 \`gh run view <RUN_ID> --repo SDCOM-0415/To-do.app\` 查看作业，通过 \`gh run watch <RUN_ID> --repo SDCOM-0415/To-do.app\` 等待实际结果。不要把 \`gh workflow run\` 的命令发送成功视作构建成功。

联合预发布还要注意：\`build-release.yml\` 的 Push 标记入口硬编码 \`v0.3.2\`、\`publish=true\`、\`prerelease=true\`；手动 \`workflow_dispatch\` 才支持指定基础版本、选择仅构建或发布。发布标签按北京时间查询既有标签并分配 \`v0.3.2-YYYYMMDD-N\`，不能覆盖旧 Release；\`prepare\` 冻结 \`main\` 和 \`flet-version\` 两个 HEAD，八项矩阵全通过才创建一个合并 Release。不要在同一版本的在途发布期间重复触发。此说明属于操作规范，**修改本文件不代表授权或启动任何构建**。

