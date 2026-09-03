"""
Day 25 练习：Debug + 测试基础

请完成以下练习：
1. 实现 Debug 工具
2. 编写 unittest 测试
3. 编写 pytest 测试
4. 使用 Mock
"""

import time
import logging
from functools import wraps
from typing import List, Any


# 练习 1：Debug 工具

def timer_decorator(func):
    """计时装饰器
    
    TODO: 实现计时装饰器
    - 测量函数执行时间
    - 打印执行时间
    - 返回函数结果
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: 实现计时逻辑
        pass
    return wrapper


def debug_print(func):
    """调试打印装饰器
    
    TODO: 实现调试装饰器
    - 打印函数名和参数
    - 打印返回值
    - 打印异常信息
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: 实现调试打印
        pass
    return wrapper


def binary_search_bug(data: List[Any], condition) -> int:
    """二分法查找问题位置
    
    TODO: 实现二分查找
    - 在 data 中找到第一个满足 condition 的位置
    - condition 返回 True 表示是"问题"数据
    - 返回问题开始的索引
    """
    pass


def print_call_stack(max_depth: int = 10):
    """打印调用栈
    
    TODO: 实现调用栈打印
    - 显示函数调用链
    - 限制最大深度
    """
    pass


# 练习 2：Logger 实现

class SimpleLogger:
    """简单的日志系统
    
    TODO: 实现以下功能
    - 多级别日志（DEBUG, INFO, WARNING, ERROR）
    - 输出到控制台和文件
    - 日志格式化
    - 日志过滤
    """
    
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    
    def __init__(self, name: str, level: int = INFO, log_file: str = None):
        self.name = name
        self.level = level
        self.log_file = log_file
        self.entries = []
    
    def _format_message(self, level: str, message: str) -> str:
        """格式化日志消息"""
        # TODO: 实现格式化
        # 格式: [时间] [级别] [名称] 消息
        pass
    
    def _write(self, message: str):
        """写入日志"""
        # TODO: 写入控制台和文件
        pass
    
    def debug(self, message: str):
        """调试日志"""
        pass
    
    def info(self, message: str):
        """信息日志"""
        pass
    
    def warning(self, message: str):
        """警告日志"""
        pass
    
    def error(self, message: str):
        """错误日志"""
        pass


# 练习 3：被测试的代码

class Stack:
    """栈实现"""
    
    def __init__(self):
        self._items = []
    
    def push(self, item):
        """压栈"""
        self._items.append(item)
    
    def pop(self):
        """弹栈"""
        if self.is_empty():
            raise IndexError("栈为空")
        return self._items.pop()
    
    def peek(self):
        """查看栈顶"""
        if self.is_empty():
            raise IndexError("栈为空")
        return self._items[-1]
    
    def is_empty(self):
        """是否为空"""
        return len(self._items) == 0
    
    def size(self):
        """栈大小"""
        return len(self._items)


class Queue:
    """队列实现"""
    
    def __init__(self):
        self._items = []
    
    def enqueue(self, item):
        """入队"""
        self._items.append(item)
    
    def dequeue(self):
        """出队"""
        if self.is_empty():
            raise IndexError("队列为空")
        return self._items.pop(0)
    
    def peek(self):
        """查看队首"""
        if self.is_empty():
            raise IndexError("队列为空")
        return self._items[0]
    
    def is_empty(self):
        """是否为空"""
        return len(self._items) == 0
    
    def size(self):
        """队列大小"""
        return len(self._items)


# 练习 4：测试代码

def test_stack_push():
    """测试压栈"""
    # TODO: 实现测试
    pass

def test_stack_pop():
    """测试弹栈"""
    # TODO: 实现测试
    pass

def test_stack_peek():
    """测试查看栈顶"""
    # TODO: 实现测试
    pass

def test_stack_empty():
    """测试空栈操作"""
    # TODO: 实现测试
    pass

def test_queue_enqueue():
    """测试入队"""
    # TODO: 实现测试
    pass

def test_queue_dequeue():
    """测试出队"""
    # TODO: 实现测试
    pass


if __name__ == "__main__":
    print("Day 25 练习 - Debug + 测试")
    
    # 测试 Debug 工具
    print("\n=== Debug 工具 ===")
    
    # 测试 Logger
    print("\n=== Logger ===")
    
    # 测试数据结构
    print("\n=== 数据结构 ===")
    stack = Stack()
    stack.push(1)
    stack.push(2)
    print(f"Stack peek: {stack.peek()}")
    print(f"Stack pop: {stack.pop()}")
    
    queue = Queue()
    queue.enqueue("a")
    queue.enqueue("b")
    print(f"Queue peek: {queue.peek()}")
    print(f"Queue dequeue: {queue.dequeue()}")
