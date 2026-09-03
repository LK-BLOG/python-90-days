"""Python 项目结构演示 - 展示 src layout vs flat layout 的区别"""

import os
import sys


def show_import_path_issue():
    """展示 flat layout 的常见陷阱"""
    # 在 flat layout 中，如果你的项目目录在 sys.path 里
    # 你可能 import 了本地的 "requests" 而不是 pip 安装的 requests
    print("[陷阱] Flat Layout 可能导致意外的 import 冲突")
    print("  例如：你的项目里有个 requests.py → import requests 会导入你的文件而不是库")

    print("\n[解决方案] Src Layout")
    print("  my_project/")
    print("  ├── src/")
    print("  │   └── my_package/    ← 包在 src 下")
    print("  │       ├── __init__.py")
    print("  │       └── utils.py")
    print("  ├── tests/")
    print("  ├── pyproject.toml")
    print("  └── README.md")


def show_pyproject_toml():
    """展示 pyproject.toml 的核心结构"""
    content = """
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "my-package"
version = "0.1.0"
description = "示例包"
requires-python = ">=3.10"
dependencies = ["requests>=2.28"]

[project.optional-dependencies]
dev = ["pytest", "black", "ruff"]

[project.scripts]
my-tool = "my_package.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
"""
    print("[pyproject.toml 示例]")
    print(content)


if __name__ == "__main__":
    show_import_path_issue()
    print("\n" + "=" * 50)
    show_pyproject_toml()
