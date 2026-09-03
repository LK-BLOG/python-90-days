# -*- coding: utf-8 -*-
# 挑战一：参数变形器

def describe_args(*args, **kwargs):
    """
    描述传入的所有参数。
    返回格式化的字符串，包含位置参数和关键字参数的信息。
    """
    # TODO: 实现位置参数部分
    # 提示：遍历args，用type获取类型名，用repr获取值
    
    # TODO: 实现关键字参数部分
    # 提示：遍历kwargs.items()，格式化 key(type)=value
    
    # TODO: 拼接结果
    pass


# 测试代码
if __name__ == "__main__":
    print(describe_args(1, "hello", name="张三", age=25))
    print(describe_args())
    print(describe_args(3.14))
