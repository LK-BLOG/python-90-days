"""
Challenge 01: 依赖管理器 - DepTracker
"""
import os
import sys
import ast
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class ImportAnalyzer(ast.NodeVisitor):
    """AST 分析器：提取 Python 文件中的 import 语句"""
    
    def __init__(self):
        self.imports = set()
    
    def visit_Import(self, node):
        """处理 import xxx"""
        for alias in node.names:
            self.imports.add(alias.name.split(".")[0])
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """处理 from xxx import yyy"""
        if node.module:
            self.imports.add(node.module.split(".")[0])
        self.generic_visit(node)


def get_stdlib_modules() -> Set[str]:
    """获取标准库模块列表
    
    TODO: 实现标准库检测
    提示: 可以使用 sys.stdlib_module_names (Python 3.10+)
    或者硬编码常见标准库
    """
    # Python 3.10+ 直接可用
    if hasattr(sys, "stdlib_module_names"):
        return sys.stdlib_module_names
    
    # 低版本 Python 的备选方案
    # TODO: 实现一个标准库模块列表
    pass


def scan_imports(file_path: str) -> Set[str]:
    """扫描单个 Python 文件的 import
    
    TODO: 使用 ast 模块解析文件，提取所有 import
    """
    pass


def scan_directory(directory: str, exclude_dirs: List[str] = None) -> Dict[str, Set[str]]:
    """扫描整个目录
    
    TODO: 遍历目录下所有 .py 文件，收集所有 import
    返回: {文件路径: {import1, import2, ...}}
    """
    pass


def parse_requirements(filepath: str) -> List[Dict[str, str]]:
    """解析 requirements.txt
    
    TODO: 解析 requirements.txt，返回依赖列表
    格式: [{"name": "requests", "version": "2.28.1", "operator": "=="}, ...]
    """
    pass


def get_installed_packages() -> Dict[str, str]:
    """获取已安装的包
    
    TODO: 使用 pip 获取已安装包列表
    返回: {包名: 版本号}
    """
    pass


def analyze_dependencies(
    project_dir: str,
    requirements_file: str = None
) -> Dict:
    """分析项目依赖
    
    TODO: 综合分析项目依赖关系
    返回:
    - declared: 声明的依赖
    - used: 使用的依赖（来自 import）
    - stdlib: 标准库模块
    - missing: 未声明但使用的
    - unused: 声明但未使用的
    """
    pass


def generate_report(analysis: Dict) -> str:
    """生成 Markdown 格式的依赖报告
    
    TODO: 根据分析结果生成可读的报告
    """
    pass


def generate_requirements(analysis: Dict, output_file: str = "requirements.txt"):
    """生成 requirements.txt
    
    TODO: 根据分析结果生成 requirements.txt
    """
    pass


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python dep_tracker.py <项目目录> [requirements.txt]")
        sys.exit(1)
    
    project_dir = sys.argv[1]
    req_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # TODO: 实现依赖分析和报告生成
    print(f"分析项目: {project_dir}")
    # analysis = analyze_dependencies(project_dir, req_file)
    # report = generate_report(analysis)
    # print(report)


if __name__ == "__main__":
    main()
