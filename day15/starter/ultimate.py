# Day 15 - Ultimate: 封装终极挑战
# 难度: ⭐⭐⭐⭐⭐
#
# 要求: 设计一个带完整验证和缓存的 ORM 字段系统
# 参考 ultimate_challenge.md

"""
封装终极挑战 — 构建一个完整的声明式 ORM 字段系统

综合运用:
- 描述符
- 验证器工厂
- 缓存
- 链式 API
"""

from typing import Any


class Field:
    """增强版 ORM 字段"""

    def __init__(self, type_=None, required=False, default=None,
                 validators=None, label=None, help_text=""):
        self.type_ = type_
        self.required = required
        self.default = default
        self.validators = validators or []
        self.label = label
        self.help_text = help_text
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name
        if self.label is None:
            self.label = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj, value):
        value = self.validate(value)
        obj.__dict__[self.name] = value

    def validate(self, value):
        if value is None and self.required:
            raise ValueError(f"{self.label} 不能为空")
        if value is not None and self.type_ and not isinstance(value, self.type_):
            raise TypeError(f"{self.label} 类型错误: 期望 {self.type_.__name__}")
        for v in self.validators:
            value = v(value)
        return value

    def error_messages(self) -> list[str]:
        """返回所有可能的错误信息"""
        msgs = []
        if self.required:
            msgs.append(f"{self.label} 为必填项")
        if self.type_:
            msgs.append(f"{self.label} 必须是 {self.type_.__name__} 类型")
        return msgs


# ===== 验证器 =====

def range_validator(min_val=None, max_val=None):
    def v(x):
        if min_val is not None and x < min_val:
            raise ValueError(f"值不能小于 {min_val}")
        if max_val is not None and x > max_val:
            raise ValueError(f"值不能大于 {max_val}")
        return x
    return v


def length_validator(min_len=None, max_len=None):
    def v(x):
        if min_len is not None and len(x) < min_len:
            raise ValueError(f"长度不能小于 {min_len}")
        if max_len is not None and len(x) > max_len:
            raise ValueError(f"长度不能超过 {max_len}")
        return x
    return v


# ===== 模型 =====

class Product:
    name = Field(type_=str, required=True, validators=[length_validator(min_len=1, max_len=100)])
    price = Field(type_=float, required=True, validators=[range_validator(min_val=0.01)])
    stock = Field(type_=int, required=False, default=0, validators=[range_validator(min_val=0)])

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price}, stock={self.stock})"


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 封装终极挑战 ===")

    p = Product(name="iPhone", price=999.99)
    print(p)

    try:
        Product(name="", price=100)
    except ValueError as e:
        print(f"错误: {e}")

    print("✅ Ultimate 完成")
