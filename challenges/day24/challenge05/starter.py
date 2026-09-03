"""
Challenge 05: 代码质量检查器 - QualityGate
"""
import os
import sys
import ast
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict


@dataclass
class FileStats:
    """文件统计"""
    path: str
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    functions: int = 0
    classes: int = 0


@dataclass
class QualityIssue:
    """质量问题"""
    file: str
    line: int
    severity: str  # error, warning, info
    message: str
    rule: str


@dataclass
class ProjectReport:
    """项目报告"""
    project_name: str
    scan_time: str
    files: List[FileStats] = field(default_factory=list)
    issues: List[QualityIssue] = field(default_factory=list)
    
    @property
    def total_files(self) -> int:
        return len(self.files)
    
    @property
    def total_lines(self) -> int:
        return sum(f.total_lines for f in self.files)
    
    @property
    def total_code_lines(self) -> int:
        return sum(f.code_lines for f in self.files)
    
    @property
    def total_comments(self) -> int:
        return sum(f.comment_lines for f in self.files)
    
    @property
    def total_blanks(self) -> int:
        return sum(f.blank_lines for f in self.files)


class ImportAnalyzer(ast.NodeVisitor):
    """AST 分析器：检测未使用的 import"""
    
    def __init__(self):
        self.imports = {}  # {name: (line, module)}
        self.used_names = set()
    
    def visit_Import(self, node):
        # TODO: 记录 import 语句
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        # TODO: 记录 from ... import 语句
        self.generic_visit(node)
    
    def visit_Name(self, node):
        # TODO: 记录变量名使用
        self.generic_visit(node)
    
    def get_unused_imports(self) -> List[Tuple[str, int]]:
        """获取未使用的 import"""
        # TODO: 对比 import 和使用
        pass


class FunctionAnalyzer(ast.NodeVisitor):
    """AST 分析器：分析函数质量"""
    
    def __init__(self, max_lines: int = 50, max_args: int = 5):
        self.max_lines = max_lines
        self.max_args = max_args
        self.issues = []
    
    def visit_FunctionDef(self, node):
        # TODO: 检查函数长度
        # TODO: 检查参数数量
        # TODO: 检查 docstring
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        # TODO: 异步函数同样检查
        self.generic_visit(node)


def count_lines(filepath: str) -> FileStats:
    """统计文件行数"""
    # TODO: 实现行数统计
    # 区分代码行、注释行、空行
    pass


def check_unused_imports(filepath: str) -> List[QualityIssue]:
    """检查未使用的 import"""
    # TODO: 使用 AST 分析
    pass


def check_missing_docstrings(filepath: str) -> List[QualityIssue]:
    """检查缺少 docstring 的函数/类"""
    # TODO: 使用 AST 检查
    pass


def check_function_length(filepath: str, max_lines: int = 50) -> List[QualityIssue]:
    """检查函数长度"""
    # TODO: 使用 AST 获取函数行数
    pass


def check_too_many_args(filepath: str, max_args: int = 5) -> List[QualityIssue]:
    """检查参数过多"""
    # TODO: 使用 AST 检查
    pass


def check_complexity(filepath: str, max_branches: int = 10) -> List[QualityIssue]:
    """检查复杂度（分支数量）"""
    # TODO: 使用 AST 统计 if/elif/for/while 等
    pass


def scan_project(
    project_dir: str,
    exclude_dirs: List[str] = None,
    max_function_lines: int = 50,
    max_function_args: int = 5
) -> ProjectReport:
    """扫描项目"""
    # TODO: 遍历项目目录
    # TODO: 收集统计信息
    # TODO: 运行所有检查
    # TODO: 生成报告
    pass


def generate_markdown_report(report: ProjectReport) -> str:
    """生成 Markdown 格式报告"""
    # TODO: 实现报告生成
    # 包含: 统计信息、问题列表、建议、评分
    pass


def calculate_score(report: ProjectReport) -> int:
    """计算质量评分（0-100）"""
    # TODO: 基于问题严重程度计算分数
    pass


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python quality_gate.py <项目目录>")
        sys.exit(1)
    
    project_dir = sys.argv[1]
    
    print(f"扫描项目: {project_dir}")
    print("=" * 50)
    
    # 扫描项目
    # report = scan_project(project_dir)
    
    # 生成报告
    # report_md = generate_markdown_report(report)
    # print(report_md)
    
    # 保存报告
    # output_file = "quality_report.md"
    # Path(output_file).write_text(report_md, encoding="utf-8")
    # print(f"\n报告已保存: {output_file}")


if __name__ == "__main__":
    main()
