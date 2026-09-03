"""示例1：pip 常用命令演示"""
import subprocess
import sys

def list_installed_packages():
    """列出已安装的包"""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=json"],
        capture_output=True, text=True
    )
    import json
    packages = json.loads(result.stdout)
    for pkg in packages:
        print(f"{pkg['name']:30s} {pkg['version']}")
    return packages

def freeze_requirements():
    """导出当前环境依赖"""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True, text=True
    )
    return result.stdout

def check_outdated():
    """检查过期的包"""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"],
        capture_output=True, text=True
    )
    import json
    return json.loads(result.stdout) if result.stdout else []

if __name__ == "__main__":
    print("=== 已安装的包 ===")
    list_installed_packages()
    
    print("\n=== 过期的包 ===")
    outdated = check_outdated()
    for pkg in outdated:
        print(f"{pkg['name']}: {pkg['version']} -> {pkg['latest_version']}")
    
    print("\n=== requirements.txt 内容 ===")
    print(freeze_requirements()[:500])  # 只显示前500字符
