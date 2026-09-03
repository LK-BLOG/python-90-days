# Boss Challenge: 函数式数据管道
# Day 1 - 难度: ★★★★★
#
# 用函数参数系统构建灵活的数据处理管道。
# 参考 README.md 了解具体要求。

def pipeline(data, *operations, **config):
    """数据处理管道
    
    Args:
        data: 输入数据（列表）
        *operations: 处理操作函数
        **config: 全局配置
    
    Returns:
        处理后的数据
    """
    # TODO: 实现管道逻辑，依次执行每个操作
    pass


def op_filter(data, condition=None, key=None):
    """过滤操作"""
    # TODO: 实现过滤逻辑
    pass


def op_map(data, func=None, key=None):
    """映射操作"""
    # TODO: 实现映射逻辑
    pass


def op_sort(data, key=None, reverse=False):
    """排序操作"""
    # TODO: 实现排序逻辑
    pass


def op_group(data, key=None, agg=None):
    """分组聚合操作"""
    # TODO: 实现分组逻辑
    pass


def op_limit(data, n=10):
    """限制数量"""
    # TODO: 实现限制逻辑
    pass


def op_unique(data, key=None):
    """去重操作"""
    # TODO: 实现去重逻辑
    pass


class Pipeline:
    """支持链式调用的管道类"""
    
    def __init__(self, data):
        # TODO: 初始化
        pass
    
    def filter(self, **kwargs):
        # TODO: 添加过滤操作
        return self
    
    def map(self, **kwargs):
        # TODO: 添加映射操作
        return self
    
    def sort(self, **kwargs):
        # TODO: 添加排序操作
        return self
    
    def limit(self, n=10):
        # TODO: 添加限制操作
        return self
    
    def result(self):
        # TODO: 执行所有操作并返回结果
        pass


if __name__ == "__main__":
    # 基础测试数据
    students = [
        {"name": "Alice", "age": 20, "score": 85},
        {"name": "Bob", "age": 22, "score": 92},
        {"name": "Charlie", "age": 20, "score": 78},
        {"name": "Diana", "age": 21, "score": 95},
    ]
    
    print("Boss Challenge: 函数式数据管道")
    print("请实现所有 TODO 方法")
