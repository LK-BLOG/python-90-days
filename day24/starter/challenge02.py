# Day 24 - Challenge 2: 项目脚手架生成器
# 难度: ⭐⭐⭐
# 输入项目名，自动生成标准项目结构

import os
from pathlib import Path
from typing import Optional


# 项目模板定义：相对路径 -> 文件内容（或 None 表示空文件）
PROJECT_TEMPLATE: dict[str, Optional[str]] = {
    "src/{name}/__init__.py": '"""Package {name}"""\n\n__version__ = "0.1.0"\n',
    "src/{name}/__main__.py": '"""Entry point for python -m {name}"""\n\ndef main() -> None:\n    print("Hello from {name}!")\n\nif __name__ == "__main__":\n    main()\n',
    "src/{name}/cli.py": None,
    "tests/__init__.py": None,
    "tests/test_cli.py": None,
    "pyproject.toml": None,
    "Makefile": None,
    ".gitignore": None,
    "README.md": None,
    "requirements/base.txt": None,
    "requirements/dev.txt": None,
    "requirements/test.txt": None,
}


class ProjectScaffolder:
    """项目脚手架生成器

    根据项目名自动生成标准的 Python 项目目录结构。
    """

    def __init__(self, base_dir: str = "."):
        """初始化生成器

        Args:
            base_dir: 项目生成的基础目录
        """
        self.base_dir = Path(base_dir)
        # TODO: 定义模板内容生成器映射
        self._generators: dict[str, callable] = {}

    def generate(self, project_name: str, force: bool = False) -> Path:
        """生成项目结构

        Args:
            project_name: 项目名称
            force: 是否覆盖已存在的文件

        Returns:
            生成的项目根目录路径
        """
        # TODO: 创建所有目录
        # TODO: 根据模板生成文件
        # TODO: 替换模板变量（{name} -> project_name）
        ...

    def _generate_pyproject(self, name: str) -> str:
        """生成 pyproject.toml 内容

        Args:
            name: 项目名

        Returns:
            pyproject.toml 文件内容
        """
        # TODO: 生成符合 PEP 621 的 pyproject.toml
        ...

    def _generate_makefile(self, name: str) -> str:
        """生成 Makefile 内容

        Args:
            name: 项目名

        Returns:
            Makefile 文件内容
        """
        # TODO: 生成包含 install/dev/test/lint/format/clean 目标的 Makefile
        ...

    def _generate_gitignore(self) -> str:
        """生成 .gitignore 内容"""
        # TODO: 返回 Python 项目标准 gitignore
        ...

    def list_structure(self, project_name: str) -> str:
        """预览将要生成的项目结构

        Args:
            project_name: 项目名

        Returns:
            目录树字符串
        """
        # TODO: 返回类似 tree 命令输出的字符串
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    scaffolder = ProjectScaffolder()
    project = scaffolder.generate("my_awesome_tool")
    print(f"项目已生成: {project}")
    print(scaffolder.list_structure("my_awesome_tool"))
