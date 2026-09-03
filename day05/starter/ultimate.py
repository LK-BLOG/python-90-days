# Day 5 Boss 挑战：CSV 数据分析器 (★★★★★)
# 难度: ★★★★★
# 要求: 构建完整的 CSV 数据分析和报告系统。


import csv
import io
import os
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional


class CSVAnalyzer:
    """CSV 数据分析器 —— 读取、分析、报告 CSV 数据。
    
    用法:
        >>> analyzer = CSVAnalyzer()
        >>> analyzer.load("sales.csv")
        >>> analyzer.describe()
        >>> analyzer.groupby("region").mean("revenue")
    
    支持功能:
        - 加载 CSV 文件（自动检测编码和分隔符）
        - 基础统计 (describe)
        - 分组聚合 (groupby)
        - 筛选过滤 (query)
        - 排序 (sort)
        - 导出 (to_csv, to_dict, to_markdown)
    """
    
    def __init__(self):
        """初始化分析器。"""
        self._data: List[Dict[str, str]] = []
        self._columns: List[str] = []
        self._dtypes: Dict[str, str] = {}
    
    def load(self, filepath=None, content=None, encoding="utf-8"):
        """加载 CSV 数据。
        
        Args:
            filepath: CSV 文件路径（和 content 二选一）
            content: CSV 文本内容
            encoding: 文件编码
        """
        # TODO: 从文件或字符串加载 CSV
        # TODO: 自动检测列名和数据类型
        pass
    
    def _detect_dtypes(self):
        """自动检测每列的数据类型。"""
        # TODO: 尝试将每列转换为 int/float，失败则保留 str
        pass
    
    def _coerce_types(self, value, dtype):
        """将值转换为指定类型。"""
        # TODO: 根据 dtype 转换值
        pass
    
    @property
    def columns(self):
        """返回列名列表。"""
        return self._columns
    
    @property
    def shape(self):
        """返回 (行数, 列数)。"""
        return (len(self._data), len(self._columns))
    
    def head(self, n=5):
        """返回前 n 行。"""
        return self._data[:n]
    
    def describe(self):
        """生成数据统计摘要。
        
        对数值列: count, mean, std, min, 25%, 50%, 75%, max
        对文本列: count, unique, top, freq
        
        Returns:
            dict: 每列的统计信息
        """
        # TODO: 对每列生成统计信息
        pass
    
    def query(self, condition):
        """按条件筛选行。
        
        Args:
            condition: 过滤函数，接收 dict 返回 bool
        
        Returns:
            CSVAnalyzer: 新实例（筛选后的数据）
        """
        # 返回新实例，不修改原始数据
        pass
    
    def groupby(self, column):
        """分组操作 —— 返回 GroupBy 对象。"""
        return GroupBy(self, column)
    
    def sort(self, column, ascending=True):
        """排序。"""
        pass
    
    def to_csv(self, filepath, encoding="utf-8"):
        """导出为 CSV 文件。"""
        pass
    
    def to_markdown(self):
        """导出为 Markdown 表格。"""
        pass


class GroupBy:
    """分组聚合对象。"""
    
    def __init__(self, analyzer, column):
        self._analyzer = analyzer
        self._column = column
        self._groups = defaultdict(list)
        # TODO: 按 column 分组数据
        pass
    
    def mean(self, value_column):
        """计算每组的平均值。"""
        # TODO: 对每组计算均值
        pass
    
    def sum(self, value_column):
        """计算每组的总和。"""
        pass
    
    def count(self):
        """统计每组的数量。"""
        pass
    
    def agg(self, func):
        """自定义聚合函数。"""
        pass


# ===== 测试 =====
if __name__ == "__main__":
    csv_content = """name,age,department,salary,join_date
Alice,25,Engineering,8000,2022-01-15
Bob,30,Engineering,12000,2020-06-01
Charlie,28,Marketing,9500,2021-03-20
Diana,35,Marketing,15000,2019-08-10
Eve,22,Engineering,7000,2023-02-28
Frank,40,Sales,11000,2018-11-05
Grace,27,Sales,8500,2022-07-12"""
    
    analyzer = CSVAnalyzer()
    analyzer.load(content=csv_content)
    
    print(f"数据形状: {analyzer.shape}")
    print(f"列名: {analyzer.columns}")
    print(f"\n前3行:")
    for row in analyzer.head(3):
        print(f"  {row}")
    
    print(f"\n统计摘要:")
    stats = analyzer.describe()
    for col, info in stats.items():
        print(f"  {col}: {info}")
    
    print(f"\n按部门平均工资:")
    groups = analyzer.groupby("department").mean("salary")
    for dept, avg in groups.items():
        print(f"  {dept}: {avg}")
    
    print(f"\nMarkdown:")
    print(analyzer.to_markdown())
