# -*- coding: utf-8 -*-
# Day 2 挑战三：函数工厂 (★★★☆☆)
# 难度: ★★★☆☆
# 要求: 实现函数工厂生成比较器和验证器。


def make_greeting(prefix="你好"):
    """问候语工厂 —— 生成带固定前缀的问候函数。
    
    功能说明:
        返回一个闭包函数，该函数接收名字并返回问候语字符串。
    
    示例:
        >>> hello = make_greeting("你好")
        >>> hello("张三")
        "你好, 张三!"
        >>> hi = make_greeting("Hi")
        >>> hi("Alice")
        "Hi, Alice!"
    
    Args:
        prefix: 问候前缀，默认 "你好"
    
    Returns:
        callable: 接收名字参数的问候函数
    """
    # TODO: 返回一个闭包，捕获 prefix 变量
    def inner(name):
        # TODO: 拼接 prefix 和 name 并返回
        pass
    return inner


def make_comparator(key_func, reverse=False):
    """比较器工厂 —— 生成自定义比较函数。
    
    功能说明:
        返回一个比较函数，可用作 sorted() 的 key 参数。
    
    示例:
        >>> by_length = make_comparator(len)
        >>> sorted(["bb", "a", "ccc"], key=by_length)
        ["a", "bb", "ccc"]
    
    Args:
        key_func: 提取比较键的函数
        reverse: 是否反转排序
    
    Returns:
        callable: 排序键函数
    """
    # TODO: 返回适配 sorted() key 参数的函数
    pass


def make_validator(**rules):
    """验证器工厂 —— 生成数据验证函数。
    
    功能说明:
        根据传入的规则生成一个验证函数，验证数据是否符合规则。
    
    支持的规则:
        - type: 期望类型
        - min: 最小值
        - max: 最大值
        - min_length: 最小长度
        - max_length: 最大长度
        - required: 是否必填
    
    示例:
        >>> check_age = make_validator(type=int, min=0, max=150)
        >>> check_age(25)     # 返回 (True, "")
        >>> check_age(-5)     # 返回 (False, "age 必须 >= 0")
    
    Args:
        **rules: 验证规则
    
    Returns:
        callable: 验证函数，接收一个值，返回 (bool, str) 元组
    """
    # TODO: 返回一个闭包验证函数
    def inner(value, field_name="value"):
        # TODO: 实现验证逻辑
        # TODO: 返回 (是否通过, 错误信息)
        pass
    return inner


def make_converter(convert_func, error_msg="转换失败"):
    """转换器工厂 —— 生成安全的类型转换函数。
    
    功能说明:
        生成一个带异常处理的转换函数。
    
    Args:
        convert_func: 转换函数（如 int, float, str）
        error_msg: 转换失败时的错误信息
    
    Returns:
        callable: 转换函数，返回 (成功?, 结果/错误信息)
    """
    # TODO: 返回带 try/except 的转换函数
    pass


# ===== 测试 =====
if __name__ == "__main__":
    # 测试问候语工厂
    hello = make_greeting("你好")
    hi = make_greeting("Hi")
    print(hello("张三"))       # 你好, 张三!
    print(hi("Alice"))        # Hi, Alice!
    
    # 测试验证器工厂
    check_age = make_validator(type=int, min=0, max=150)
    check_name = make_validator(type=str, min_length=1, max_length=50)
    
    print(f"\ncheck_age(25):  {check_age(25)}")      # (True, "")
    print(f"check_age(-5):  {check_age(-5)}")        # (False, "...")
    print(f"check_name(''): {check_name('')}")       # (False, "...")
    
    # 测试比较器工厂
    students = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 20}]
    by_age = make_comparator(lambda s: s["age"])
    print(f"\n排序: {sorted(students, key=by_age)}")
