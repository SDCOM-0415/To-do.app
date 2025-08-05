#!/bin/bash
# Linux 系统 Tkinter 安装脚本 - Todo App v0.3

echo "🐧 Linux 系统 Tkinter 安装脚本"
echo "=================================================="

# 检测 Linux 发行版
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_NAME=$NAME
    OS_ID=$ID
    echo "检测到系统: $OS_NAME"
else
    echo "无法检测系统版本，尝试通用安装方法"
    OS_ID="unknown"
fi

echo ""
echo "📦 安装 Python Tkinter 支持..."

# 根据不同发行版安装 tkinter
case $OS_ID in
    "ubuntu"|"debian"|"linuxmint")
        echo "🔧 Ubuntu/Debian 系统，使用 apt 安装..."
        sudo apt update
        sudo apt install -y python3-tk python3-dev
        ;;
    "fedora"|"rhel"|"centos")
        echo "🔧 Fedora/RHEL/CentOS 系统，使用 dnf/yum 安装..."
        if command -v dnf &> /dev/null; then
            sudo dnf install -y python3-tkinter python3-devel
        else
            sudo yum install -y tkinter python3-devel
        fi
        ;;
    "arch"|"manjaro")
        echo "🔧 Arch Linux 系统，使用 pacman 安装..."
        sudo pacman -S tk python
        ;;
    "opensuse"|"sles")
        echo "🔧 openSUSE 系统，使用 zypper 安装..."
        sudo zypper install -y python3-tk python3-devel
        ;;
    *)
        echo "⚠️  未识别的系统，请手动安装 python3-tk 包"
        echo "常见安装命令："
        echo "  Ubuntu/Debian: sudo apt install python3-tk"
        echo "  Fedora: sudo dnf install python3-tkinter"
        echo "  Arch: sudo pacman -S tk"
        echo "  openSUSE: sudo zypper install python3-tk"
        ;;
esac

echo ""
echo "🧪 测试 Tkinter 安装..."

python3 -c "
try:
    import tkinter as tk
    print('✅ Tkinter 安装成功！')
    
    # 创建测试窗口
    root = tk.Tk()
    root.title('Tkinter 测试')
    root.geometry('300x200')
    
    label = tk.Label(root, text='✅ Tkinter 工作正常！\n窗口将在3秒后关闭', 
                    font=('Arial', 12), justify='center')
    label.pack(expand=True)
    
    # 3秒后自动关闭
    root.after(3000, root.quit)
    root.mainloop()
    root.destroy()
    
    print('✅ Tkinter 测试通过')
    
except ImportError as e:
    print(f'❌ Tkinter 仍然不可用: {e}')
    print('请检查安装是否成功，或尝试重新安装')
    exit(1)
except Exception as e:
    print(f'⚠️  Tkinter 可用但测试失败: {e}')
    print('可能是显示相关问题，但基本功能应该正常')
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 安装完成！现在可以运行 Todo App v0.3 了"
    echo ""
else
    echo ""
    echo "❌ 安装可能失败，请检查错误信息"
fi