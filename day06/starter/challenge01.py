# Day 6 挑战一：异常捕获 (★☆☆☆☆)
# 要求: 掌握 try/except/else/finally 的完整用法。


def safe_divide(a, b):
    """安全除法 —— 除数为零时返回 None 而非崩溃。
    
    Args:
        a: 被除数
        b: 除数
    Returns:
        商或 None
    """
    # TODO: 用 try/except 捕获 ZeroDivisionError
    pass


def safe_get(dct, key, default=None):
    """安全字典取值 —— 键不存在时返回默认值。
    
    Args:
        dct: 源字典
        key: 键名
        default: 默认值
    Returns:
        值或默认值
    """
    # TODO: 用 try/except 捕获 KeyError
    pass


def safe_int(value, default=0):
    """安全转整数 —— 转换失败返回默认值。
    
    Args:
        value: 待转换值
        default: 转换失败时的默认值
    Returns:
        int 或 default
    """
    # TODO: 捕获 ValueError
    pass


def read_number_from_user():
    """从用户输入读取一个数字，循环直到输入合法。
    
    Returns:
        float: 用户输入的数字
    """
    # TODO: 用 while + try/except 实现循环输入
    pass


def execute_with_finally(path):
    """演示 finally 的用法 —— 确保资源释放。
    
    Args:
        path: 文件路径
    Returns:
        文件内容或 None
    """
    f = None
    try:
        f = open(path, 'r', encoding='utf-8')
        return f.read()
    except FileNotFoundError:
        print(f"文件不存在: {path}")
        return None
    finally:
        # TODO: 无论成功与否都关闭文件
        pass


# ===== 测试 =====
if __name__ == "__main__":
    print(f"10 / 3 = {safe_divide(10, 3)}")
    print(f"10 / 0 = {safe_divide(10, 0)}")
    print(f"safe_int('abc') = {safe_int('abc')}")
    print(f"safe_int('42') = {safe_int('42')}")
