"""依赖管理演示 - requirements.txt / poetry / uv 对比"""

import os
import tempfile
from pathlib import Path


def create_requirements_txt():
    """生成示例 requirements.txt"""
    content = """# 生产依赖
requests==2.31.0
pydantic>=2.0,<3.0
fastapi>=0.104.0
uvicorn[standard]>=0.24.0

# 开发依赖（通常放在 requirements-dev.txt）
# pytest>=7.4
# pytest-cov>=4.1
# black>=23.0
# ruff>=0.1.0
"""
    print("[requirements.txt 示例]")
    print(content)
    return content


def create_pyproject_poetry():
    """生成 poetry 风格的 pyproject.toml"""
    content = """
# Poetry 风格
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.10"
requests = "^2.31"
pydantic = "^2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
black = "^23.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
    print("[Poetry pyproject.toml 示例]")
    print(content)


def compare_tools():
    """对比三种依赖管理工具"""
    print("""
┌──────────────┬────────────┬────────────┬────────────┐
│              │ requirements│  Poetry    │    uv      │
├──────────────┼────────────┼────────────┼────────────┤
│ 速度         │ ★☆☆        │ ★★☆        │ ★★★        │
│ 锁文件       │ 无         │ 有         │ 有         │
│ 虚拟环境管理 │ 手动       │ 自动       │ 自动       │
│ 发布 PyPI    │ 手动       │ 一条命令   │ 一条命令   │
│ 适合场景     │ 简单项目   │ 成熟项目   │ 所有项目   │
└──────────────┴────────────┴────────────┴────────────┘

推荐：小项目用 requirements.txt，正经项目用 uv。
""")


if __name__ == "__main__":
    create_requirements_txt()
    compare_tools()
    create_pyproject_poetry()
