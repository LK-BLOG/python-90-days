"""示例2：虚拟环境管理"""
import os
import sys
import subprocess

def create_venv(path=".venv"):
    """创建虚拟环境"""
    subprocess.run([sys.executable, "-m", "venv", path], check=True)
    print(f"虚拟环境已创建: {path}")

def get_venv_python(path=".venv"):
    """获取虚拟环境中的 Python 路径"""
    if os.name == "nt":  # Windows
        return os.path.join(path, "Scripts", "python.exe")
    return os.path.join(path, "bin", "python")

def install_in_venv(packages, venv_path=".venv"):
    """在虚拟环境中安装包"""
    python = get_venv_python(venv_path)
    subprocess.run([python, "-m", "pip", "install"] + packages, check=True)

def is_in_venv():
    """检查当前是否在虚拟环境中"""
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )

if __name__ == "__main__":
    print(f"当前是否在虚拟环境: {is_in_venv()}")
    print(f"Python 路径: {sys.executable}")
    print(f"Python 版本: {sys.version}")
    
    # 注意：实际创建虚拟环境需要取消下面的注释
    # create_venv("test_venv")
    # install_in_venv(["requests"], "test_venv")
