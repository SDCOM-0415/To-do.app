# TodoApp — 独立版本分支与联合发布

本仓库同时维护三个分支：

| 分支 | 用途 | 入口 | 构建方式 |
|---|---|---|---|
| `main` | 现行 Tk / CustomTkinter 版 | `app.py` | PyInstaller |
| `flet-version` | 独立 Flet / Flutter 版 | `main.py` | Flet CLI |
| `old-version` | 历史 Qt 版和 v0.2 归档 | `todo_app.py`、`v0.2/` | 仅归档 |

三个分支各自维护源码。**Flet 源码直接位于 `flet-version` 根目录**，不再嵌套在 `flet_port/` 中。旧代码已从 `main` 的工作树移出，保存在 `old-version`；原提交历史仍然可查看。

## 构建与联合发布

在 `main` 分支运行 [Build and Release (Tk + Flet)](https://github.com/SDCOM-0415/To-do.app/actions/workflows/build-release.yml)，输入基础版本，例如 `v0.3.2`。

- **Publish** 默认关闭：只构建并上传 8 份临时 Actions 工件，不发布 Release。
- **Prerelease** 勾选时使用北京时间生成 `vX.X.X-YYYYMMDD-N`，序号按同一天该基础版本已有 Git Tags 递增；兼容旧的 `YYYY-MM-DD` 日期格式以免序号重复。
- 发布必须等八个目标全部成功：每版分别构建 Windows x64、Linux x64、macOS Intel 和 macOS ARM64。
- `prepare` 会记录两个分支各自的提交 SHA，所有构建在同一次运行中检出对应 SHA，不需要合并分支。

正式发布文件名示例：

- `TodoApp-v0.3.2-20261110-1-Windows-x64.zip`（Tk）
- `TodoApp-Flet-v0.3.2-20261110-1-Windows-x64.zip`（Flet）
- 其他目标分别有 Linux `.tar.gz` 及 macOS `.zip`，另外提供 `SHA256SUMS.txt`。

`flet-version` 单独运行 [Flet Edition Build](https://github.com/SDCOM-0415/To-do.app/blob/flet-version/.github/workflows/flet-build.yml)，只上传测试工件，不发布 Release。

## 数据兼容

两个现行版本使用同一个 `platformdirs.user_data_path("TodoApp", "SDCOM")/tasks.json`。
Tk 设置存储在 `tk-config.json`，Flet 设置存储在 `flet-settings.json`。
切换版本之前请备份任务文件；不要在两个程序中并发修改相同任务，以免覆盖。

macOS 下载的应用包尚未自动签名和公证，正式发布前建议在目标系统上验证。
