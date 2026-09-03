# Day 24 - Challenge 5: 代码质量检查器
# 难度: ⭐⭐⭐
# 扫描 Python 项目，统计行数、检查文件大小、未使用import、缺少docstring，生成 Markdown 报告

import ast
import os
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class FileReport:
    """单个文件的检查报告"""
    path: str
    total_lines: int = 0
    code_lines: int = 0
    blank_lines: int = 0
    file_size_kb: float = 0.0
    unused_imports: list[str] = field(default_factory=list)
    missing_docstrings: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)


@dataclass
class ProjectReport:
    """项目整体报告"""
    root_dir: str
    files: list[FileReport] = field(default_factory=list)
    total_files: int = 0
    total_lines: int = 0
    total_code_lines: int = 0
    quality_score: float = 0.0


class CodeQualityChecker:
    """代码质量检查器

    扫描 Python 项目目录，生成质量报告。
    """

    def __init__(self, root_dir: str, max_file_size_kb: float = 500):
        """初始化

        Args:
            root_dir: 项目根目录
            max_file_size_kb: 文件大小警告阈值（KB）
        """
        self.root_dir = Path(root_dir)
        self.max_file_size_kb = max_file_size_kb

    def scan_file(self, file_path: Path) -> FileReport:
        """扫描单个 Python 文件

        Args:
            file_path: 文件路径

        Returns:
            FileReport 对象
        """
        # TODO: 统计行数（总行、代码行、空白行）
        # TODO: 检查文件大小
        # TODO: 用 AST 分析未使用的 import
        # TODO: 检查函数/类是否缺少 docstring
        ...

    def _find_unused_imports(self, tree: ast.Module) -> list[str]:
        """查找未使用的 import

        Args:
            tree: AST 语法树

        Returns:
            未使用的导入名列表
        """
        # TODO: 收集所有 import 的名称
        # TODO: 在 AST 中搜索这些名称是否被使用
        ...

    def _find_missing_docstrings(self, tree: ast.Module) -> list[str]:
        """查找缺少 docstring 的函数和类

        Args:
            tree: AST 语法树

        Returns:
            缺少 docstring 的函数/类名列表
        """
        # TODO: 遍历所有 FunctionDef 和 ClassDef
        # TODO: 检查第一个节点是否为 docstring
        ...

    def scan_project(self) -> ProjectReport:
        """扫描整个项目

        Returns:
            完整的项目报告
        """
        # TODO: 递归遍历所有 .py 文件
        # TODO: 汇总所有文件报告
        # TODO: 计算质量评分
        ...

    def generate_markdown(self, report: ProjectReport) -> str:
        """生成 Markdown 格式的质量报告

        Args:
            report: 项目报告

        Returns:
            Markdown 文本
        """
        # TODO: 生成包含以下内容的报告：
        # - 项目概览（文件数、总行数、代码行数）
        # - 各文件详情表格
        # - 未使用 import 汇总
        # - 缺少 docstring 汇总
        # - 质量评分和建议
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    checker = CodeQualityChecker(".")
    report = checker.scan_project()
    md = checker.generate_markdown(report)
    print(md)
