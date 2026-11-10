# TodoApp — 历史版本归档

此分支专门保存 TodoApp 早期开发版本的源代码，不参与当前 Tk 与 Flet 的联合构建或 Release 发布。

## 归档内容

| 路径 | 内容 |
|---|---|
| `todo_app.py` | 早期 Qt / PySide6 实现 |
| `v0.2/` | v0.2 阶段的程序入口、主窗口、数据模型和界面组件 |

这些文件来自原 `main` 分支的 `old version/` 文件夹，迁移后保存在当前分支的根目录与 `v0.2/` 子目录内。历史代码保留用于参考和回溯；**尚未按当前开发环境逐一验证构建与运行**。

## 当前维护版本

- [main：CustomTkinter 版本](https://github.com/SDCOM-0415/To-do.app/tree/main)
- [flet-version：Flet / Flutter 版本](https://github.com/SDCOM-0415/To-do.app/tree/flet-version)

两个版本的安装包请从 [GitHub Releases](https://github.com/SDCOM-0415/To-do.app/releases) 获取。此归档分支不用于发布新安装包。

## 维护规则

历史版本原则上只进行归档说明、索引和明确要求的维护。改动前请阅读 [AGENTS.md](AGENTS.md)；未来新增的 Git 提交信息与 README 均使用简体中文。不得在未验证的情况下声称早期版本兼容当前系统。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
