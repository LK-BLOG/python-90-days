"""
Challenge 01: Debug 工具箱 - DebugKit
"""
import time
import functools
import traceback
import sys
from typing import Any, Callable, List, Optional
from collections import defaultdict


class DebugKit:
    """Debug 工具箱"""
    
    @staticmethod
    def timer(func: Callable) -> Callable:
        """计时装饰器
        
        TODO: 实现计时功能
        - 测量函数执行时间
        - 打印格式化时间
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: 实现
            pass
        return wrapper
    
    @staticmethod
    def memoize(func: Callable) -> Callable:
        """缓存装饰器
        
        TODO: 实现缓存功能
        - 缓存函数结果
        - 支持缓存清除
        """
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: 实现
            pass
        
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    
    @staticmethod
    def call_counter(func: Callable) -> Callable:
        """调用计数装饰器
        
        TODO: 实现调用计数
        - 记录调用次数
        - 记录参数
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: 实现
            pass
        
        wrapper.call_count = 0
        wrapper.calls = []
        return wrapper
    
    @staticmethod
    def binary_search(data: List[Any], condition: Callable) -> Optional[int]:
        """二分查找问题位置
        
        TODO: 实现二分查找
        - 找到第一个满足条件的位置
        - 返回索引或 None
        """
        pass
    
    @staticmethod
    def print_stack(max_depth: int = 10):
        """打印调用栈
        
        TODO: 实现调用栈打印
        - 显示函数调用链
        - 限制深度
        """
        pass
    
    @staticmethod
    def memory_profile(func: Callable) -> Callable:
        """内存分析装饰器
        
        TODO: 实现内存分析
        - 测量内存使用
        - 输出内存变化
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: 实现
            pass
        return wrapper


def test_timer():
    """测试计时装饰器"""
    @DebugKit.timer
    def slow_function():
        time.sleep(0.01)
        return "done"
    
    result = slow_function()
    assert result == "done"


def test_call_counter():
    """测试调用计数"""
    @DebugKit.call_counter
    def add(a, b):
        return a + b
    
    add(1, 2)
    add(3, 4)
    
    assert add.call_count == 2
    assert len(add.calls) == 2


if __name__ == "__main__":
    print("Debug 工具箱测试")
    test_timer()
    test_call_counter()
    print("测试通过！")
