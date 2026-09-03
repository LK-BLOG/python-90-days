# Day 25 - Challenge 5: 覆盖率分析器
# 难度: ⭐⭐⭐
# 解析 coverage.xml，生成 Markdown 报告，标记未覆盖代码，计算质量评分

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FileCoverage:
    """单个文件的覆盖率信息"""
    filename: str
    lines_valid: int = 0
    lines_covered: int = 0
    branches_valid: int = 0
    branches_covered: int = 0
    uncovered_lines: list[int] = field(default_factory=list)

    @property
    def line_rate(self) -> float:
        """行覆盖率百分比"""
        return self.lines_covered / self.lines_valid * 100 if self.lines_valid else 0.0

    @property
    def branch_rate(self) -> float:
        """分支覆盖率百分比"""
        return self.branches_covered / self.branches_valid * 100 if self.branches_valid else 0.0


@dataclass
class CoverageReport:
    """项目覆盖率报告"""
    total_lines_valid: int = 0
    total_lines_covered: int = 0
    total_branches_valid: int = 0
    total_branches_covered: int = 0
    files: list[FileCoverage] = field(default_factory=list)
    quality_score: float = 0.0
    quality_grade: str = ""

    @property
    def total_line_rate(self) -> float:
        return self.total_lines_covered / self.total_lines_valid * 100 if self.total_lines_valid else 0.0


class CoverageAnalyzer:
    """覆盖率分析器

    解析 coverage.xml 报告，生成 Markdown 格式的覆盖率报告。
    """

    def __init__(self, xml_path: str = "coverage.xml"):
        """初始化

        Args:
            xml_path: coverage.xml 文件路径
        """
        self.xml_path = Path(xml_path)

    def parse(self) -> CoverageReport:
        """解析 coverage.xml 文件

        Returns:
            CoverageReport 对象
        """
        # TODO: 使用 ET 解析 XML
        # TODO: 提取每个文件的覆盖率信息
        # TODO: 提取未覆盖的行号
        ...

    def _calculate_quality_score(self, report: CoverageReport) -> float:
        """计算质量评分（0-100）

        评分规则：
        - 行覆盖率权重 0.7
        - 分支覆盖率权重 0.3
        - 每个未覆盖文件扣分

        Args:
            report: 覆盖率报告

        Returns:
            0-100 的评分
        """
        # TODO: 实现评分算法
        ...

    def _get_grade(self, score: float) -> str:
        """根据评分返回等级

        Args:
            score: 质量评分

        Returns:
            等级字符串（A/B/C/D/F）
        """
        # TODO: A >= 90, B >= 80, C >= 70, D >= 60, F < 60
        ...

    def generate_markdown(self, report: CoverageReport) -> str:
        """生成 Markdown 格式的覆盖率报告

        Args:
            report: 覆盖率报告

        Returns:
            Markdown 文本
        """
        # TODO: 生成报告，包含：
        # - 总体覆盖率和等级
        # - 各文件覆盖率表格
        # - 未覆盖行号列表
        # - 改进建议
        ...

    def mark_uncovered(self, report: CoverageReport) -> str:
        """生成未覆盖代码的标记报告

        Args:
            report: 覆盖率报告

        Returns:
            标记了未覆盖行的源代码片段
        """
        # TODO: 读取源文件，标记未覆盖的行
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    analyzer = CoverageAnalyzer()
    if analyzer.xml_path.exists():
        report = analyzer.parse()
        md = analyzer.generate_markdown(report)
        print(md)
    else:
        print(f"未找到 {analyzer.xml_path}，请先运行 coverage run && coverage xml")
