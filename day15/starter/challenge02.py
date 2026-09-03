# Day 15 - Challenge 2: 数据验证描述符
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 实现通用验证框架
# 参考 challenge.md

"""
数据验证描述符挑战 — 构建声明式验证框架

核心知识点:
- 描述符链式验证
- __set_name__ 自动命名
- 自定义验证规则
"""

from typing import Any, Callable


class Validated:
    """通用验证描述符 — 支持链式验证规则"""

    def __init__(self, *validators: Callable):
        """
        Args:
            *validators: 验证函数列表
                每个函数签名为 (value) -> value (通过则返回值，失败则 raise)
        """
        # TODO: 存储验证器列表
        self.validators = validators
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f"_validated_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # TODO: 从 obj.__dict__ 取值，不存在则返回 None
        pass

    def __set__(self, obj, value):
        # TODO: 依次执行每个 validator
        # 全部通过后存入 obj.__dict__[self.storage_name]
        pass


# ===== 验证器工厂 =====

def required(message: str = ""):
    """非空验证器"""
    def validator(value):
        # TODO: None 或空字符串则抛出 ValueError
        pass
    return validator


def min_value(min_val: float, message: str = ""):
    """最小值验证器"""
    def validator(value):
        # TODO: value < min_val 则抛出 ValueError
        pass
    return validator


def max_value(max_val: float, message: str = ""):
    """最大值验证器"""
    def validator(value):
        # TODO: value > max_val 则抛出 ValueError
        pass
    return validator


def type_check(expected_type: type, message: str = ""):
    """类型验证器"""
    def validator(value):
        # TODO: not isinstance(value, expected_type) 则抛出 TypeError
        pass
    return validator


def one_of(*allowed: Any, message: str = ""):
    """枚举验证器"""
    def validator(value):
        # TODO: value not in allowed 则抛出 ValueError
        pass
    return validator


# ===== 使用示例 =====

class UserForm:
    """用户表单 — 用声明式验证"""

    username = Validated(
        type_check(str, "用户名必须是字符串"),
        required("用户名不能为空"),
    )

    age = Validated(
        type_check(int, "年龄必须是整数"),
        min_value(0, "年龄不能为负"),
        max_value(150, "年龄不能超过150"),
    )

    role = Validated(
        type_check(str),
        one_of("admin", "user", "guest", message="无效的角色"),
    )

    def __init__(self, username: str, age: int, role: str = "user"):
        # TODO: 通过 property 赋值触发验证
        pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 数据验证描述符测试 ===")

    form = UserForm("alice", 25, "admin")
    print(f"username: {form.username}")
    print(f"age: {form.age}")

    try:
        UserForm("", 25)  # username required
    except ValueError as e:
        print(f"验证失败: {e}")

    try:
        UserForm("bob", -1)  # age < 0
    except ValueError as e:
        print(f"验证失败: {e}")

    try:
        UserForm("carol", 30, "superadmin")  # role not in one_of
    except ValueError as e:
        print(f"验证失败: {e}")

    print("✅ Challenge 02 完成")
