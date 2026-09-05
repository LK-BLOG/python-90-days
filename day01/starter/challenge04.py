# Day 1 挑战四：函数选择器
# 难度：★★★★☆


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("除数不能是 0")
    return a / b


OPERATIONS = {
    # TODO：把 add、subtract、multiply、divide 放进这个字典。
    # "add": add,
}


def dispatch(action, a, b):
    """根据 action 调用对应函数。

    示例：
        dispatch("add", 3, 5)  # 8
    """
    # TODO：从 OPERATIONS 取出函数，再调用它。
    # 提示：func = OPERATIONS[action]
    pass


if __name__ == "__main__":
    print(dispatch("add", 3, 5))
    print(dispatch("multiply", 4, 7))
