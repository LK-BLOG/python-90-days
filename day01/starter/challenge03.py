# Day 1 挑战三：函数调度器 (★★★☆☆)
# 难度: ★★★☆☆
# 要求: 根据关键字参数中的 action 值调用对应的操作函数。

# ===== 基础运算函数 =====

def add(a, b):
    """两数相加。
    
    Args:
        a: 第一个加数
        b: 第二个加数
    
    Returns:
        两数之和
    """
    return a + b


def subtract(a, b):
    """两数相减。
    
    Args:
        a: 被减数
        b: 减数
    
    Returns:
        两数之差
    """
    return a - b


def multiply(a, b):
    """两数相乘。
    
    Args:
        a: 第一个因数
        b: 第二个因数
    
    Returns:
        两数之积
    """
    return a * b


def divide(a, b):
    """两数相除。
    
    Args:
        a: 被除数
        b: 除数
    
    Returns:
        两数之商（浮点数）
    
    Raises:
        ValueError: 当除数为零时
    """
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b


# 操作注册表：action名称 -> 函数
OPERATIONS = {
    # TODO: 把上面四个函数注册到这里，格式: "action名": 函数引用
    # 提示: "add": add, "subtract": subtract, ...
}


def dispatch(action, a, b, **kwargs):
    """根据 action 分派到对应的函数并执行。
    
    功能说明:
        从 OPERATIONS 注册表中查找 action 对应的函数，
        调用该函数并返回结果。
    
    示例:
        >>> dispatch("add", 3, 5)
        8
        >>> dispatch("multiply", 4, 7)
        28
    
    Args:
        action: 操作名称（字符串），必须在 OPERATIONS 中注册
        a: 第一个操作数
        b: 第二个操作数
        **kwargs: 额外参数（传递给目标函数，可选）
    
    Returns:
        操作结果
    
    Raises:
        ValueError: 未知的操作名称（action 不在 OPERATIONS 中）
        TypeError: 函数调用参数不匹配
    """
    # TODO: 步骤1 - 检查 action 是否存在于 OPERATIONS 中
    # TODO: 步骤2 - 获取对应的函数
    # TODO: 步骤3 - 调用函数并返回结果
    pass


# ===== 测试 =====
if __name__ == "__main__":
    print(dispatch("add", 3, 5))           # 期望: 8
    print(dispatch("multiply", 4, 7))      # 期望: 28
    print(dispatch("divide", 10, 3))       # 期望: 3.333...
    print(dispatch("subtract", 100, 42))   # 期望: 58
