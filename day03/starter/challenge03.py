# Day 3 挑战三：缓存工厂 (★★★☆☆)
# 难度: ★★★☆☆
# 要求: 实现带 TTL 的缓存闭包。


import time
import functools


def make_cache(ttl=60, maxsize=128):
    """创建一个带 TTL（生存时间）的缓存装饰器。
    
    功能说明:
        返回一个装饰器，被装饰的函数结果会被缓存 ttl 秒。
        超过 ttl 秒后缓存过期，下次调用会重新计算。
        同时限制最大缓存条目数（LRU 淘汰）。
    
    用法:
        @make_cache(ttl=30, maxsize=100)
        def expensive_computation(n):
            time.sleep(1)
            return n * n
    
    Args:
        ttl: 缓存过期时间（秒），默认 60
        maxsize: 最大缓存条目数，默认 128
    
    Returns:
        callable: 装饰器函数
    """
    def decorator(func):
        # TODO: 初始化缓存存储
        # 提示: cache = {}  # {args_key: (result, timestamp)}
        # TODO: 使用 functools.wraps 保留原函数的元信息
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: 步骤1 - 生成缓存键（将 args + kwargs 转为可哈希的键）
            # TODO: 步骤2 - 检查缓存是否存在且未过期
            # TODO: 步骤3 - 缓存命中则直接返回
            # TODO: 步骤4 - 缓存未命中则调用函数，存入缓存
            # TODO: 步骤5 - 如果缓存满，淘汰最旧的条目
            pass
        return wrapper
    return decorator


def make_lru_cache(maxsize=128):
    """创建一个 LRU（最近最少使用）缓存装饰器。
    
    功能说明:
        不带 TTL，但限制缓存大小，超过时淘汰最久未使用的条目。
    
    Args:
        maxsize: 最大缓存条目数
    
    Returns:
        callable: 装饰器函数
    """
    def decorator(func):
        # TODO: 使用 OrderedDict 或自定义数据结构实现 LRU
        # TODO: 添加 cache_info() 方法返回缓存统计
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: 实现 LRU 缓存逻辑
            pass
        
        # TODO: 添加缓存管理方法
        wrapper.cache_clear = lambda: None  # TODO: 实现清空缓存
        wrapper.cache_info = lambda: {}    # TODO: 实现统计信息
        
        return wrapper
    return decorator


def make_cache_with_stats(ttl=60, maxsize=128):
    """创建带详细统计信息的缓存装饰器。
    
    功能说明:
        除了基本缓存功能外，还记录:
        - 命中次数 (hits)
        - 未命中次数 (misses)
        - 当前缓存大小 (size)
        - 最大缓存大小 (maxsize)
    
    Returns:
        callable: 装饰器函数，被装饰函数拥有 .cache_stats() 方法
    """
    def decorator(func):
        # TODO: 初始化缓存和统计计数器
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: 实现缓存逻辑 + 统计
            pass
        
        def cache_stats():
            """返回缓存统计信息字典。"""
            # TODO: 返回 {"hits": ..., "misses": ..., "size": ..., "maxsize": ...}
            pass
        
        wrapper.cache_stats = cache_stats
        wrapper.cache_clear = lambda: None  # TODO: 实现
        
        return wrapper
    return decorator


# ===== 测试 =====
if __name__ == "__main__":
    @make_cache(ttl=2, maxsize=3)
    def slow_add(a, b):
        """模拟慢速计算。"""
        print(f"  计算 {a} + {b} ...")
        time.sleep(0.1)
        return a + b
    
    print("=== TTL 缓存测试 ===")
    print(f"结果: {slow_add(1, 2)}")   # 计算
    print(f"结果: {slow_add(1, 2)}")   # 缓存命中
    print(f"结果: {slow_add(3, 4)}")   # 计算
    print(f"结果: {slow_add(1, 2)}")   # 缓存命中
    
    print(f"\n等待缓存过期（2秒）...")
    time.sleep(2.5)
    print(f"结果: {slow_add(1, 2)}")   # 重新计算
