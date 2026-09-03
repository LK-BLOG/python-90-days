# Day 3 Boss 挑战：计数器工厂系统 (★★★★★)
# 难度: ★★★★★
# 要求: 用闭包实现不同计数策略。


import functools
import time
from collections import defaultdict


class CounterFactory:
    """计数器工厂 —— 创建各种类型的计数器。
    
    功能说明:
        使用闭包和装饰器模式，提供不同策略的计数器：
        - 基础计数器
        - 带重置的计数器
        - 带窗口的滑动计数器
        - 带回调的计数器
        - 带阈值告警的计数器
    
    用法:
        >>> factory = CounterFactory()
        >>> c1 = factory.make("basic")
        >>> c1.tick(); c1.tick()
        >>> print(c1.value)  # 2
    """
    
    def __init__(self):
        """初始化工厂，注册所有计数器类型。"""
        # TODO: 初始化计数器类型注册表
        self._registry = {}
        # TODO: 注册内置计数器类型
        self._register_builtins()
    
    def _register_builtins(self):
        """注册内置计数器类型。"""
        # TODO: 注册 "basic" 基础计数器
        # TODO: 注册 "resettable" 可重置计数器
        # TODO: 注册 "window" 滑动窗口计数器
        # TODO: 注册 "alert" 告警计数器
        pass
    
    def register(self, name, factory_func):
        """注册自定义计数器类型。
        
        Args:
            name: 计数器类型名称
            factory_func: 工厂函数，返回计数器实例
        """
        self._registry[name] = factory_func
    
    def make(self, counter_type, **kwargs):
        """创建指定类型的计数器。
        
        Args:
            counter_type: 计数器类型名称
            **kwargs: 传递给计数器的配置参数
        
        Returns:
            计数器实例
        """
        # TODO: 从注册表查找并创建计数器
        pass
    
    def make_decorator(self, counter_type, **kwargs):
        """创建装饰器版本的计数器（自动统计函数调用次数）。
        
        Args:
            counter_type: 计数器类型名称
            **kwargs: 计数器配置参数
        
        Returns:
            callable: 装饰器函数
        """
        def decorator(func):
            counter = self.make(counter_type, **kwargs)
            
            @functools.wraps(func)
            def wrapper(*args, **kw):
                counter.tick()
                return func(*args, **kw)
            
            wrapper.counter = counter
            return wrapper
        return decorator


class BasicCounter:
    """基础计数器 —— 最简单的计数器。"""
    
    def __init__(self, start=0):
        # TODO: 初始化计数值
        pass
    
    def tick(self, n=1):
        """增加计数。"""
        # TODO: 计数加 n
        pass
    
    @property
    def value(self):
        """返回当前计数值。"""
        pass


class WindowCounter:
    """滑动窗口计数器 —— 只统计最近 N 秒内的调用。"""
    
    def __init__(self, window_seconds=60):
        # TODO: 初始化窗口大小和时间戳列表
        pass
    
    def tick(self):
        """记录一次调用。"""
        # TODO: 添加当前时间戳
        # TODO: 清理超出窗口的时间戳
        pass
    
    @property
    def value(self):
        """返回窗口内的调用次数。"""
        pass


class AlertCounter:
    """告警计数器 —— 达到阈值时触发回调。"""
    
    def __init__(self, threshold=10, callback=None):
        # TODO: 初始化阈值和回调函数
        pass
    
    def tick(self):
        """增加计数，超过阈值时触发回调。"""
        # TODO: 计数加1
        # TODO: 检查是否超过阈值
        # TODO: 超过则调用回调函数
        pass
    
    @property
    def value(self):
        pass


# ===== 测试 =====
if __name__ == "__main__":
    factory = CounterFactory()
    
    print("=== 基础计数器 ===")
    c = factory.make("basic")
    c.tick(); c.tick(); c.tick()
    print(f"  计数: {c.value}")  # 3
    
    print("\n=== 滑动窗口计数器 ===")
    wc = factory.make("window", window_seconds=2)
    wc.tick(); wc.tick(); wc.tick()
    print(f"  窗口内计数: {wc.value}")  # 3
    
    print("\n=== 告警计数器 ===")
    alerts = []
    ac = factory.make("alert", threshold=3, callback=lambda v: alerts.append(f"告警: 计数达到{v}"))
    ac.tick(); ac.tick(); ac.tick()
    print(f"  计数: {ac.value}")
    print(f"  告警记录: {alerts}")
    
    print("\n=== 装饰器模式 ===")
    @factory.make_decorator("basic")
    def greet(name):
        print(f"  你好, {name}!")
    
    greet("Alice")
    greet("Bob")
    print(f"  调用次数: {greet.counter.value}")
