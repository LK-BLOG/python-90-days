# Day 3 挑战二：nonlocal 计数器 (★★☆☆☆)
# 难度: ★★☆☆☆
# 要求: 用 nonlocal 实现多种计数器。


def make_counter(start=0):
    """创建一个基础计数器。
    
    功能说明:
        返回一个闭包，每次调用计数器加1并返回当前值。
    
    示例:
        >>> c = make_counter()
        >>> c()   # 1
        >>> c()   # 2
        >>> c()   # 3
    
    Args:
        start: 起始值，默认 0
    
    Returns:
        callable: 计数器函数，无参数，返回当前计数值
    """
    # TODO: 使用 nonlocal 实现计数器闭包
    pass


def make_step_counter(start=0, step=1):
    """创建一个可指定步长的计数器。
    
    功能说明:
        每次调用增加指定步长（可以是负数实现倒计时）。
    
    示例:
        >>> c = make_step_counter(start=0, step=5)
        >>> c()   # 5
        >>> c()   # 10
    
    Args:
        start: 起始值
        step: 步长（正数递增，负数递减）
    
    Returns:
        callable: 计数器函数
    """
    # TODO: 实现可变步长的计数器
    pass


def make_max_counter(start=0, maximum=10):
    """创建一个有上限的计数器。
    
    功能说明:
        计数到 maximum 后停止，返回 maximum。
    
    Args:
        start: 起始值
        maximum: 最大值上限
    
    Returns:
        callable: 计数器函数
    """
    # TODO: 实现带上限的计数器
    pass


def make_multi_counter(**counters):
    """创建多个命名计数器的集合。
    
    功能说明:
        返回一个函数，接收计数器名称，对该计数器加1并返回新值。
    
    示例:
        >>> mc = make_multi_counter(views=0, clicks=0, errors=0)
        >>> mc("views")     # 1
        >>> mc("clicks")    # 1
        >>> mc("views")     # 2
    
    Args:
            **counters: 计数器名称和初始值
    
    Returns:
        callable: 接受计数器名称的函数
    
    Raises:
        KeyError: 当计数器名称不存在时
    """
    # TODO: 使用 nonlocal 和闭包实现多个独立计数器
    pass


# ===== 测试 =====
if __name__ == "__main__":
    print("=== 基础计数器 ===")
    c = make_counter()
    for i in range(5):
        print(f"  第{i+1}次: {c()}")
    
    print("\n=== 步长计数器 ===")
    sc = make_step_counter(start=0, step=3)
    for i in range(5):
        print(f"  第{i+1}次: {sc()}")
    
    print("\n=== 上限计数器 ===")
    mc = make_max_counter(start=0, maximum=5)
    for i in range(8):
        print(f"  第{i+1}次: {mc()}")
    
    print("\n=== 多命名计数器 ===")
    analytics = make_multi_counter(views=0, clicks=0, errors=0)
    analytics("views")
    analytics("views")
    analytics("clicks")
    analytics("errors")
    analytics("views")
    print(f"  状态: views={analytics('views')}, clicks={analytics('clicks')}, errors={analytics('errors')}")
