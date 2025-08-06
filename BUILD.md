# Todo App v0.3.1 - 构建说明

本文档说明如何构建 Todo App 的二进制可执行文件。

## 🚀 自动构建（推荐）

### GitHub Actions 手动构建

构建流程已设置为仅允许手动触发，在 GitHub Actions 页面点击 "Run workflow" 按钮即可开始构建。

这将构建以下平台的二进制文件：
- Windows x64 (.zip)
- macOS x64 (.dmg) - 使用 macos-latest-large 镜像
- Linux x64 (.tar.gz)

构建完成后，二进制文件会自动上传到 GitHub Release。

### 手动触发步骤

1. 访问项目的 GitHub Actions 页面
2. 选择 "Build and Release" 工作流
3. 点击 "Run workflow" 按钮
4. 等待构建完成
5. 检查生成的 Release

## 🔧 本地构建

### 环境要求

- Python 3.12+
- 已安装项目依赖：`pip install -r requirements.txt`
- PyInstaller：`pip install pyinstaller`

### 快速构建

使用提供的构建脚本：

```bash
python build.py
```

这个脚本会：
1. 检查依赖环境
2. 自动构建适合当前平台的可执行文件
3. 创建压缩包
4. 显示构建结果

### 手动构建

如果你想手动控制构建过程：

```bash
# 使用 PyInstaller 直接构建
pyinstaller --onefile --windowed --name "TodoApp" app.py

# 或使用配置文件构建
pyinstaller build.spec
```

### 高级构建选项

使用 `build.spec` 配置文件可以进行更精细的控制：

```bash
pyinstaller build.spec
```

这个配置文件包含：
- 优化的依赖包含/排除设置
- 自定义图标支持
- macOS 应用程序包配置
- 数据文件包含设置

## 📦 构建输出

构建完成后，你会在 `dist/` 目录找到：

### Windows
- `Todo-App-v0.3.1-Windows-x64.exe` - 可执行文件
- `Todo-App-v0.3.1-Windows-x64.zip` - 压缩包

### macOS
- `TodoApp` 或 `TodoApp.app` - 可执行文件/应用程序包
- `Todo-App-v0.3.1-macOS-x64.tar.gz` - 压缩包

### Linux
- `TodoApp` - 可执行文件
- `Todo-App-v0.3.1-Linux-x64.tar.gz` - 压缩包

## 🐛 构建问题排查

### 常见问题

1. **缺少依赖模块**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Linux 系统缺少 tkinter**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk python3-dev
   
   # CentOS/RHEL
   sudo yum install tkinter python3-devel
   
   # 或使用提供的脚本
   bash install_linux_tkinter.sh
   ```

3. **macOS 权限问题**
   ```bash
   # 给构建脚本执行权限
   chmod +x build.py
   ```

4. **Windows 杀毒软件误报**
   - 将 `dist/` 目录添加到杀毒软件白名单
   - 或临时关闭实时保护

### 构建优化

1. **减小文件大小**
   - 编辑 `build.spec` 中的 `excludes` 列表
   - 移除不需要的依赖包

2. **添加自定义图标**
   - 将 `.ico` 文件放在项目根目录
   - 命名为 `icon.ico`

3. **包含额外文件**
   - 编辑 `build.spec` 中的 `datas` 列表
   - 添加需要包含的文件路径

## 📋 GitHub Actions 工作流说明

`.github/workflows/build-release.yml` 文件定义了自动构建流程：

### 触发条件
- 推送版本标签（如 `v0.3.1`）
- 手动触发

### 构建矩阵
- Windows (windows-latest)
- macOS (macos-latest)  
- Linux (ubuntu-latest)

### 构建步骤
1. 检出代码
2. 设置 Python 环境
3. 安装系统依赖（Linux）
4. 安装 Python 依赖
5. 构建可执行文件
6. 创建压缩包
7. 上传构建产物
8. 创建 GitHub Release
9. 上传文件到 Release

### 自定义构建

你可以修改工作流文件来：
- 更改 Python 版本
- 添加更多平台支持
- 修改构建参数
- 自定义 Release 说明

## 🎯 发布流程

完整的发布流程：

1. **更新版本号**
   ```bash
   # 已在代码中更新为 v0.3.1
   ```

2. **提交更改**
   ```bash
   git add .
   git commit -m "Release v0.3.1"
   git push origin main
   ```

3. **创建标签**
   ```bash
   git tag v0.3.1
   git push origin v0.3.1
   ```

4. **等待构建完成**
   - 在 GitHub Actions 页面查看构建进度
   - 构建完成后自动创建 Release

5. **验证发布**
   - 检查 Release 页面
   - 下载并测试二进制文件
   - 更新 Release 说明（如需要）

---

## 📞 技术支持

如果在构建过程中遇到问题：

1. 查看 GitHub Actions 构建日志
2. 检查本地构建输出
3. 在项目 Issues 页面提交问题
4. 联系开发者：sdcom@sdcom.asia

---

**注意**: 首次构建可能需要较长时间，因为需要下载和安装依赖。后续构建会更快。