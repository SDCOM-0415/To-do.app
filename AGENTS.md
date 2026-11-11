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

## Actions 触发机制与 0.3.2 联合预发布（2026-11-11 核对）

### 各工作流的入口与边界

| 工作流 | 所在分支 | 触发入口 | 产物/作用 |
| --- | --- | --- | --- |
| `.github/workflows/build-release.yml` | `main` | `workflow_dispatch`；或仅 `main` 下 `.release-trigger/0.3.2-prerelease` 的 Push | 统一构建 Tk 和 Flet 并可创建合并 Release |
| `.github/workflows/i18n-color-check.yml` | `main` | 手动；或仅 `.test-trigger/i18n-color-check` 的 Push | 一个 Ubuntu Runner 检出双分支，进行语言与颜色回归检查，不发布 |
| `.github/workflows/tk-macos-intel-test.yml` | `main` | 手动；或专用 `.test-trigger/tk-macos-intel-0.3.2` 的 Push | 只测 Tk macOS Intel，不发布 |
| `.github/workflows/flet-build.yml` | `flet-version` | 仅 `workflow_dispatch` | 独立 Flet 四平台 Actions 工件，不创建 Release |
| `.github/workflows/flet-windows-macos-test.yml` | `flet-version` | 手动；或专用 `.test-trigger/flet-windows-macos-0.3.2` 的 Push | 一次运行两个 Runner，Windows x64 + macOS Intel Flet 测试，不发布 |
| `.github/workflows/flet-macos-intel-test.yml` | `flet-version` | 手动；或专用 `.test-trigger/macos-intel-0.3.2` 的 Push | 单平台 macOS Intel Flet 测试，不发布 |

以上路径基于工作流定义；修改非触发路径的正常代码、`AGENTS.md` 或 `README.md` 不会启动这些 Push 工作流。不要为了触发发布新增宽泛的 `push`、`pull_request` 或定时触发条件。

### 联合发布的两种授权触发方法

1. **手动入口**：在 GitHub Actions 选择 `Build and Release (Tk + Flet)`，点击 Run workflow，选择 `main`，输入 `version=v0.3.2`，设定 `publish=true`、`prerelease=true`。若 `publish=false`，只保留短期 Actions 工件，不发布。
2. **仓库文件入口**：仅在用户明确授权一次预发布后，修改 `main` 上已经存在的 `.release-trigger/0.3.2-prerelease`，提交并 Push 到 `main`。由于标记文件已存在，应**更新内容**而不是尝试同路径创建文件；使用 GitHub Contents API 时必须提供当前 blob SHA。该路径的 Push 会按硬编码 `v0.3.2`、`prerelease=true`、发布开启的配置启动联合流程，不能借它发布其他基础版本。

推荐在受限 GitHub 连接环境使用第二种方法：先提交两分支源码和文档，最后单独更新触发标记，保持一次用户授权对应一次发布触发；提交后通过 Actions 运行记录确认确实入队。触发标记属于发布操作，不得因普通代码修改而顺手更新。

### 构建、标签和校验细节

- `prepare` 使用 GitHub API 分别读取 `main`、`flet-version` 分支头 SHA，冻结此次构建源代码；构建矩阵通过各自 SHA 检出，避免版本混用。
- 八项矩阵任务：Tk/Flet 各有 Windows x64（`windows-latest`）、Linux x64（`ubuntu-24.04`）、macOS x64、macOS arm64。Tk Intel 使用 `macos-26-intel`；Flet Intel 在 `macos-26` 上以 `--arch x86_64` 交叉构建，并用 `lipo` 检查目标架构。
- 发布文件名使用 `TodoApp` 和 `TodoApp-Flet` 两类前缀，Windows/macOS 为 ZIP、Linux 为 tar.gz。只有八个任务全部成功后，`release` 作业才检查八个文件、生成 `SHA256SUMS.txt`、创建一个组合 GitHub Release。
- 预发布标签由 `prepare` 按中国标准时间自动分配 `v0.3.2-YYYYMMDD-N`，同时检查已有带横线的旧日期格式；不会覆盖已经存在的标签。2026-11-11 核对时已有 `v0.3.2-20261111-1`、`v0.3.2-20261111-2`，后续编号以**实际运行时**再次查询为准，不能预先认定一定是 `-3`。
- 联合发布并发组为 `todo-dual-release-v0.3.2`（Push 情况），且 `cancel-in-progress: true`。不要在已有相同版本构建运行中重复触发，否则可能取消前一次执行。
- 如果 `prepare`、八项构建或 `release` 中任何步骤失败，先核对运行日志、源 SHA、构建工件和 Release 状态。**不得在未获新的明确授权时修改标记再次重跑**；更不能将入队、运行中误报为发布成功。
- 0.3.2 已有预发布资产，创建新标签保留原有 Release。正常的 `AGENTS.md` 更新不会触发联合构建；请把分析文档提交与发布标记提交分开，便于审计。

