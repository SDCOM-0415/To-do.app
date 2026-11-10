#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Todo App v0.3.2 - 发布脚本
自动化版本发布流程
"""

import os
import sys
import subprocess
import re
from pathlib import Path

def run_command(cmd, check=True):
    """运行命令并返回结果"""
    print(f"执行命令: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        return None

def get_current_version():
    """从 config.py 获取当前版本"""
    config_file = Path("config.py")
    if not config_file.exists():
        print("❌ 找不到 config.py 文件")
        return None
    
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找版本号
    version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    if version_match:
        return version_match.group(1)
    
    print("❌ 无法从 config.py 中找到版本号")
    return None

def check_git_status():
    """检查 Git 状态"""
    result = run_command("git status --porcelain")
    if result and result.stdout.strip():
        print("⚠️  工作目录有未提交的更改:")
        print(result.stdout)
        return False
    return True

def check_git_branch():
    """检查当前分支"""
    result = run_command("git branch --show-current")
    if result:
        branch = result.stdout.strip()
        print(f"当前分支: {branch}")
        if branch != "main" and branch != "master":
            print("⚠️  建议在 main 或 master 分支上发布")
            return input("是否继续? (y/N): ").lower() == 'y'
    return True

def create_tag(version):
    """创建 Git 标签"""
    tag_name = f"v{version}"
    
    # 检查标签是否已存在
    result = run_command(f"git tag -l {tag_name}", check=False)
    if result and result.stdout.strip():
        print(f"⚠️  标签 {tag_name} 已存在")
        if input("是否删除现有标签并重新创建? (y/N): ").lower() != 'y':
            return False
        
        # 删除本地标签
        run_command(f"git tag -d {tag_name}")
        # 删除远程标签
        run_command(f"git push origin --delete {tag_name}", check=False)
    
    # 创建新标签
    message = f"Release Todo App v{version}"
    result = run_command(f'git tag -a {tag_name} -m "{message}"')
    if not result:
        return False
    
    print(f"✅ 创建标签: {tag_name}")
    return tag_name

def push_tag(tag_name):
    """推送标签到远程仓库"""
    result = run_command(f"git push origin {tag_name}")
    if not result:
        return False
    
    print(f"✅ 推送标签: {tag_name}")
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("Todo App v0.3.2 - 自动发布脚本")
    print("=" * 60)
    
    # 检查是否在 Git 仓库中
    if not Path(".git").exists():
        print("❌ 当前目录不是 Git 仓库")
        return False
    
    # 获取当前版本
    version = get_current_version()
    if not version:
        return False
    
    print(f"当前版本: {version}")
    
    # 检查 Git 状态
    if not check_git_status():
        print("❌ 请先提交所有更改")
        return False
    
    # 检查当前分支
    if not check_git_branch():
        return False
    
    # 确认发布
    print(f"\n准备发布版本: v{version}")
    print("注意: 构建流程已改为手动触发模式")
    print("这将会:")
    print("1. 创建 Git 标签")
    print("2. 推送标签到远程仓库")
    print("3. 需要手动在 GitHub Actions 页面触发构建")
    
    if input("\n确认创建标签? (y/N): ").lower() != 'y':
        print("取消操作")
        return False
    
    # 创建标签
    tag_name = create_tag(version)
    if not tag_name:
        print("❌ 创建标签失败")
        return False
    
    # 推送标签
    if not push_tag(tag_name):
        print("❌ 推送标签失败")
        return False
    
    print("\n🎉 标签创建成功!")
    print(f"✅ 标签 {tag_name} 已推送到远程仓库")
    print("⚠️  请手动触发 GitHub Actions 构建")
    print("\n📋 后续步骤:")
    print("1. 在 GitHub Actions 页面查看构建进度")
    print("2. 构建完成后检查 Release 页面")
    print("3. 下载并测试二进制文件")
    print("4. 根据需要更新 Release 说明")
    
    # 打开相关页面
    repo_url = get_repo_url()
    if repo_url:
        print(f"\n🔗 相关链接:")
        print(f"Actions: {repo_url}/actions")
        print(f"Releases: {repo_url}/releases")
    
    return True

def get_repo_url():
    """获取仓库 URL"""
    result = run_command("git remote get-url origin", check=False)
    if result and result.stdout.strip():
        url = result.stdout.strip()
        # 转换 SSH URL 为 HTTPS URL
        if url.startswith("git@github.com:"):
            url = url.replace("git@github.com:", "https://github.com/")
        if url.endswith(".git"):
            url = url[:-4]
        return url
    return None

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发布过程出错: {e}")
        sys.exit(1)