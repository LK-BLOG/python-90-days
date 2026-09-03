"""
Challenge 02: 项目脚手架生成器 - PyScaffold
"""
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional


# 模板内容
PYPROJECT_TEMPLATE = """[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "{project_name}"
version = "0.1.0"
description = "{description}"
readme = "README.md"
license = {text = "{license}"}
requires-python = ">={python_version}"
authors = [
    {name = "{author}", email = "{email}"}
]
dependencies = []

[project.optional-dependencies]
dev = [
    "black>=23.0",
    "isort>=5.12",
    "flake8>=6.0",
    "mypy>=1.0",
]
test = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
]

[tool.black]
line-length = 88
target-version = ["py{python_version_no_dot}"]

[tool.isort]
profile = "black"

[tool.pytest.ini_options]
testpaths = ["tests"]
"""

README_TEMPLATE = """# {project_name}

{description}

## 安装

```bash
# 创建虚拟环境
python -m venv .venv
.venv/Scripts/activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 安装开发依赖
pip install -e ".[dev]"
```

## 使用

```python
import {project_name_underscore}
```

## 开发

```bash
make test      # 运行测试
make lint      # 代码检查
make format    # 格式化代码
```

## 许可证

{license}
"""

GITIGNORE_TEMPLATE = """__pycache__/
*.py[cod]
*$py.class
*.so
*.egg-info/
dist/
build/
*.egg
.venv/
venv/
ENV/
.vscode/
.idea/
*.swp
*.swo
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.DS_Store
Thumbs.db
"""

MAKEFILE_TEMPLATE = """.PHONY: help install dev test lint format clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {{FS = ":.*?## "}}; {{printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}}'

install:
	pip install -r requirements.txt

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	black --check .
	isort --check-only .
	flake8 .

format:
	black .
	isort .

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {{}} +
"""


def create_project(
    project_name: str,
    layout: str = "src",
    author: str = "Your Name",
    email: str = "you@example.com",
    license: str = "MIT",
    python_version: str = "3.9",
    no_ci: bool = False,
    no_git: bool = False,
    output_dir: str = "."
) -> Path:
    """创建项目结构
    
    TODO: 实现项目生成功能
    """
    # 1. 创建目录结构
    # 2. 生成 pyproject.toml
    # 3. 生成 README.md
    # 4. 生成 .gitignore
    # 5. 生成 Makefile
    # 6. 生成 requirements 目录
    # 7. 初始化 Git（可选）
    
    project_path = Path(output_dir) / project_name
    project_path.mkdir(parents=True, exist_ok=True)
    
    # TODO: 实现具体逻辑
    pass


def create_src_layout(project_path: Path, project_name: str):
    """创建 src layout 目录结构"""
    # TODO: 实现
    pass


def create_flat_layout(project_path: Path, project_name: str):
    """创建 flat layout 目录结构"""
    # TODO: 实现
    pass


def write_file(path: Path, content: str):
    """写入文件"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Python 项目脚手架生成器")
    parser.add_argument("project_name", help="项目名称")
    parser.add_argument("--layout", choices=["src", "flat"], default="src",
                       help="项目布局 (默认: src)")
    parser.add_argument("--author", default="Your Name", help="作者名称")
    parser.add_argument("--email", default="you@example.com", help="作者邮箱")
    parser.add_argument("--license", default="MIT", help="许可证类型")
    parser.add_argument("--python-version", default="3.9", help="最低 Python 版本")
    parser.add_argument("--no-ci", action="store_true", help="不生成 CI 配置")
    parser.add_argument("--no-git", action="store_true", help="不初始化 Git")
    parser.add_argument("--output-dir", default=".", help="输出目录")
    
    args = parser.parse_args()
    
    # TODO: 调用 create_project
    print(f"创建项目: {args.project_name}")
    print(f"布局: {args.layout}")
    print(f"作者: {args.author}")
    
    # project_path = create_project(
    #     args.project_name,
    #     layout=args.layout,
    #     author=args.author,
    #     email=args.email,
    #     license=args.license,
    #     python_version=args.python_version,
    #     no_ci=args.no_ci,
    #     no_git=args.no_git,
    #     output_dir=args.output_dir
    # )
    
    # print(f"\n项目创建成功: {project_path}")


if __name__ == "__main__":
    main()
