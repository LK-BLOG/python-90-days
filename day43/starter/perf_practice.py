# Day 43 性能优化骨架
import time
import cProfile

# TODO: 分析并优化以下函数
def process_data(data: list) -> list:
    '''处理数据 - TODO: 找到性能瓶颈并优化'''
    result = []
    for item in data:
        if item not in result:  # O(n) 查找
            result.append(item ** 2)
    return sorted(result, reverse=True)

def find_common(list1: list, list2: list) -> list:
    '''找到两个列表的共同元素 - TODO: 优化'''
    common = []
    for item in list1:
        if item in list2 and item not in common:
            common.append(item)
    return common

# TODO: 用 cProfile 分析
# TODO: 用 timeit 验证优化效果
# TODO: 优化后性能提升至少 10x
