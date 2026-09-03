# Day 3 挑战四：简单装饰器 (★★★★☆)
# 难度: ★★★★☆
# 要求: 手写装饰器实现日志和重试。

import time
import functools
import random


def log_calls(func):
    """日志装饰器 —— 记录函数调用信息。
    
    功能说明:
        在函数调用前后打印日志，包括:
        - 调用时间
        - 函数名
        - 传入参数
        - 返回值
        - 执行耗时
    
    示例:
        >>> @log_calls
        ... def add(a, b):
        ...     return a + b
        >>> add(3, 5)
        [2024-01-01 12:00:00] 调用 add(3, 5)
        [2024-01-01 12:00:00] 返回 add -> 8 (耗时: 0.001s)
        8
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: 步骤1 - 记录开始时间
        # TODO: 步骤2 - 打印调用日志（函数名 + 参数）
        # TODO: 步骤3 - 调用原函数
        # TODO: 步骤4 - 计算耗时并打印返回日志
        pass
    return wrapper


def retry(max_retries=3, delay=1.0, exceptions=(Exception,)):
    """重试装饰器 —— 函数失败时自动重试。
    
    功能说明:
        当被装饰函数抛出指定异常时，自动重试最多 max_retries 次。
        每次重试之间等待 delay 秒。
    
    参数:
        max_retries: 最大重试次数（默认 3 次，即共执行 4 次）
        delay: 重试间隔（秒）
        exceptions: 需要捕获的异常类型元组
    
    示例:
        >>> @retry(max_retries=3, delay=0.5, exceptions=(ValueError,))
        ... def unstable():
        ...     if random.random() < 0.7:
        ...         raise ValueError("随机失败")
        ...     return "成功！"
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: 实现重试逻辑
            # TODO: 捕获指定异常
            # TODO: 记录每次重试的日志
            pass
        return wrapper
    return decorator


def timer(func):
    """计时装饰器 —— 测量函数执行时间。"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: 使用 time.perf_counter() 精确计时
        pass
    return wrapper


def validate_types(*arg_types, **kwarg_types):
    """类型验证装饰器 —— 自动检查参数类型。
    
    Args:
        *arg_types: 位置参数的期望类型（按顺序）
        **kwarg_types: 关键字参数的期望类型
    
    示例:
        >>> @validate_types(int, int, mode=str)
        ... def power(a, b, mode="pow"):
        ...     return a ** b
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: 验证位置参数类型
            # TODO: 验证关键字参数类型
            # TODO: 类型不匹配时抛出 TypeError
            pass
        return wrapper
    return decorator


def rate_limit(calls_per_second=1):
    """限流装饰器 —— 限制函数调用频率。
    
    Args:
        calls_per_second: 每秒最大调用次数
    """
    def decorator(func):
        min_interval = 1.0 / calls_per_second
        last_called = [0.0]  # 使用列表存储可变状态
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: 计算距上次调用的时间间隔
            # TODO: 如果间隔不足，等待到允许调用
            # TODO: 调用函数并更新上次调用时间
            pass
        return wrapper
    return decorator


# ===== 测试 =====
if __name__ == "__main__":
    @log_calls
    def add(a, b):
        return a + b
    
    print("=== 日志装饰器 ===")
    result = add(3, 5)
    print(f"结果: {result}\n")
    
    @retry(max_retries=3, delay=0.1, exceptions=(ValueError,))
    def unreliable():
        if random.random() < 0.8:
            raise ValueError("随机失败！")
        return "成功！"
    
    print("=== 重试装饰器 ===")
    try:
        result = unreliable()
        print(f"结果: {result}")
    except ValueError as e:
        print(f"最终失败: {e}")
