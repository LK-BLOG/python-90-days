# Day 5 挑战四：数据转换管道 (★★★★☆)
# 难度: ★★★★☆
# 要求: 构建可组合的数据转换管道。


import csv
import json
from functools import reduce
from typing import Any, Callable, List


class TransformPipeline:
    """数据转换管道 —— 支持链式数据变换。
    
    功能说明:
        将多个转换步骤串联，每个步骤是一个函数:
        数据 -> 步骤1 -> 步骤2 -> ... -> 步骤N -> 结果
    
    用法:
        >>> pipe = TransformPipeline()
        >>> result = (pipe
        ...     .add(lambda data: [x for x in data if x > 0])
        ...     .add(lambda data: [x * 2 for x in data])
        ...     .execute([-1, 0, 1, 2, 3]))
        >>> print(result)  # [2, 4, 6]
    """
    
    def __init__(self):
        """初始化空管道。"""
        self._steps: List[Callable] = []
        self._name: str = "Pipeline"
    
    def add(self, transform, name=None):
        """添加一个转换步骤。
        
        Args:
            transform: 转换函数，接收数据返回数据
            name: 步骤名称（用于调试）
        
        Returns:
            self: 支持链式调用
        """
        # TODO: 存储步骤
        pass
    
    def execute(self, data):
        """执行管道，依次应用所有转换步骤。
        
        Args:
            data: 输入数据
        
        Returns:
            转换后的数据
        """
        # TODO: 使用 reduce 或循环依次应用步骤
        pass
    
    def compose(self, other_pipeline):
        """组合两个管道。
        
        Args:
            other_pipeline: 另一个 TransformPipeline
        
        Returns:
            TransformPipeline: 新管道（先执行 self，再执行 other）
        """
        # TODO: 合并两个管道的步骤
        pass
    
    def __repr__(self):
        step_names = [getattr(s, '__name__', f'step_{i}') 
                      for i, s in enumerate(self._steps)]
        return f"{' -> '.join(step_names) or 'empty'}"


# ===== 预定义的转换函数 =====

def csv_to_dicts(csv_text):
    """将 CSV 文本转为字典列表。"""
    # TODO: 使用 csv.DictReader 解析
    pass


def filter_rows(predicate):
    """创建行过滤器（工厂函数）。
    
    Args:
        predicate: 过滤条件函数，接收 dict 返回 bool
    
    Returns:
        Callable: 过滤转换函数
    """
    # TODO: 返回过滤函数
    pass


def select_columns(*columns):
    """创建列选择器。
    
    Args:
        *columns: 要保留的列名
    
    Returns:
        Callable: 列选择转换函数
    """
    # TODO: 返回选择函数
    pass


def add_column(name, func):
    """创建列添加器。
    
    Args:
        name: 新列名
        func: 计算函数，接收行 dict 返回列值
    
    Returns:
        Callable: 添加列的转换函数
    """
    # TODO: 返回添加列函数
    pass


def sort_by(key, reverse=False):
    """创建排序器。
    
    Args:
        key: 排序键函数
        reverse: 是否降序
    
    Returns:
        Callable: 排序转换函数
    """
    # TODO: 返回排序函数
    pass


def aggregate_by(group_key, agg_func, value_key):
    """创建分组聚合器。
    
    Args:
        group_key: 分组键
        agg_func: 聚合函数
        value_key: 聚合值键
    
    Returns:
        Callable: 聚合转换函数
    """
    # TODO: 返回聚合函数
    pass


# ===== 测试 =====
if __name__ == "__main__":
    # 示例数据
    csv_data = """name,age,salary,department
Alice,25,8000,Engineering
Bob,30,12000,Engineering
Charlie,28,9500,Marketing
Diana,35,15000,Marketing
Eve,22,7000,Engineering"""
    
    # 使用管道处理数据
    result = (TransformPipeline()
        .add(csv_to_dicts, "解析CSV")
        .add(filter_rows(lambda r: int(r["salary"]) > 8000), "过滤低薪")
        .add(select_columns("name", "salary", "department"), "选择列")
        .add(add_column("bonus", lambda r: str(int(r["salary"]) * 0.1)), "加奖金列")
        .execute(csv_data))
    
    print("管道处理结果:")
    for row in result:
        print(f"  {row}")
    
    # 数值管道测试
    num_result = (TransformPipeline()
        .add(lambda data: [x for x in data if x > 0], "过滤正数")
        .add(lambda data: [x ** 2 for x in data], "平方")
        .add(lambda data: [x for x in data if x > 10], "过滤>10")
        .execute([-5, -2, 1, 2, 3, 4, 5]))
    print(f"\n数值管道: {num_result}")
