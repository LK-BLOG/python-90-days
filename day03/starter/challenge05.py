# Day 3 挑战五 (Boss)：计数器工厂系统 (★★★★★)
# 要求: 用闭包实现不同计数策略。

import time
import functools
from collections import defaultdict


class CounterFactory:
    """计数器工厂 —— 创建各种类型的计数器。"""
    
    def __init__(self):
        self._registry = {}
        self._register_builtins()
    
    def _register_builtins(self):
        """注册内置计数器类型: basic / resettable / window / alert。"""
        # TODO: 注册 4 种内置计数器
        pass
    
    def register(self, name, factory_func):
        """注册自定义计数器类型。"""
        self._registry[name] = factory_func
    
    def make(self, counter_type, **kwargs):
        """创建指定类型的计数器。"""
        # TODO: 从注册表查找并创建
        pass
    
    def make_decorator(self, counter_type, **kwargs):
        """创建装饰器版本的计数器（统计函数调用次数）。"""
        def decorator(func):
            counter = self.make(counter_type, **kwargs)
            @functools.wraps(func)
            def wrapper(*a, **kw):
                counter.tick()
                return func(*a, **kw)
            wrapper.counter = counter
            return wrapper
        return decorator


class BasicCounter:
    """基础计数器 —— 最简单的自增计数。"""
    def __init__(self, start=0):
        self._value = start
    def tick(self, n=1):
        self._value += n
    @property
    def value(self):
        return self._value
    def reset(self):
        self._value = 0


class WindowCounter:
    """滑动窗口计数器 —— 只统计最近 N 秒内的调用。"""
    def __init__(self, window_seconds=60):
        self._window = window_seconds
        self._timestamps = []
    def tick(self):
        now = time.time()
        self._timestamps.append(now)
        cutoff = now - self._window
        self._timestamps = [t for t in self._timestamps if t > cutoff]
    @property
    def value(self):
        return len(self._timestamps)


class AlertCounter:
    """告警计数器 —— 达到阈值时触发回调。"""
    def __init__(self, threshold=10, callback=None):
        self._count = 0
        self._threshold = threshold
        self._callback = callback
    def tick(self):
        self._count += 1
        if self._count >= self._threshold and self._callback:
            self._callback(self._count)
    @property
    def value(self):
        return self._count


class RateCounter:
    """速率计数器 —— 计算每秒调用频率（TPS/QPS）。"""
    def __init__(self, window_seconds=10):
        self._window = window_seconds
        self._timestamps = []
    def tick(self):
        self._timestamps.append(time.time())
        cutoff = time.time() - self._window
        self._timestamps = [t for t in self._timestamps if t > cutoff]
    @property
    def value(self):
        return len(self._timestamps)
    @property
    def rate(self):
        if not self._timestamps:
            return 0.0
        elapsed = time.time() - self._timestamps[0]
        return len(self._timestamps) / elapsed if elapsed > 0 else 0.0


# ===== 测试 =====
if __name__ == "__main__":
    factory = CounterFactory()
    
    print("=== 基础计数器 ===")
    c = factory.make("basic")
    c.tick(); c.tick(); c.tick()
    print(f"  计数: {c.value}")
    c.reset()
    print(f"  重置后: {c.value}")
    
    print("\n=== 窗口计数器 ===")
    wc = factory.make("window", window_seconds=2)
    wc.tick(); wc.tick(); wc.tick()
    print(f"  窗口内: {wc.value}")
    
    print("\n=== 告警计数器 ===")
    alerts = []
    ac = factory.make("alert", threshold=3,
                       callback=lambda v: alerts.append(f"告警:{v}"))
    ac.tick(); ac.tick(); ac.tick()
    print(f"  计数: {ac.value}, 告警: {alerts}")
    
    print("\n=== 速率计数器 ===")
    rc = factory.make("rate", window_seconds=5)
    for _ in range(5):
        rc.tick()
    print(f"  调用次数: {rc.value}, 速率: {rc.rate:.1f}/s")
    
    print("\n=== 装饰器模式 ===")
    @factory.make_decorator("basic")
    def greet(name):
        print(f"  你好, {name}!")
    greet("Alice"); greet("Bob")
    print(f"  调用次数: {greet.counter.value}")
