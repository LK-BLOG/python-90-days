# -*- coding: utf-8 -*-
# 挑战四：参数验证器

def validate(func, rules, *args, **kwargs):
    """
    验证参数后调用函数。
    
    Args:
        func: 要调用的函数
        rules: 参数验证规则 {"param": {"type": type, "min": n, "max": n, "min_length": n}}
        *args, **kwargs: 参数
    
    Returns:
        函数结果或错误信息字符串
    """
    # TODO: 收集所有参数名和值
    # TODO: 检查type规则
    # TODO: 检查min/max范围
    # TODO: 检查min_length/max_length
    # TODO: 有错误返回错误字符串，全部通过调用函数
    pass


if __name__ == "__main__":
    def create_user(name, age, email):
        return f"{name}, {age}, {email}"

    rules = {
        "name": {"type": str, "min_length": 2},
        "age": {"type": int, "min": 0, "max": 150},
        "email": {"type": str}
    }
    print(validate(create_user, rules, 123, age=25, email="a@b.com"))
    print(validate(create_user, rules, "张", age=25, email="a@b.com"))
    print(validate(create_user, rules, "张三", age=200, email="a@b.com"))
    print(validate(create_user, rules, "张三", age=25, email="zhangsan@example.com"))
