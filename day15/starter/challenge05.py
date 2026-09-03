# Day 15 - Challenge 5: ORM 字段系统
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 实现字段验证链
# 参考 challenge.md

"""
ORM 字段系统挑战 — 实现声明式字段 + 验证链

核心知识点:
- 字段描述符
- 验证链 (chain of responsibility)
- 默认值、必填、自定义验证
"""

from typing import Any, Callable


class Field:
    """ORM 字段基类

    支持:
        - 类型检查
        - 默认值
        - 必填标记
        - 自定义验证器链
    """

    def __init__(self, type_: type = None, required: bool = False,
                 default: Any = None, validators: list = None):
        self.type_ = type_
        self.required = required
        self.default = default
        self.validators = validators or []
        self.name = None
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f"_field_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # TODO: 从 obj.__dict__ 取值，返回默认值
        pass

    def __set__(self, obj, value):
        # TODO: 执行所有验证器 -> 通过则存入
        pass

    def validate(self, value: Any) -> Any:
        """执行完整验证链

        Raises:
            TypeError: 类型不匹配
            ValueError: 验证失败
        """
        # TODO: 检查 required -> 检查类型 -> 执行每个 validator
        pass


class TextField(Field):
    """文本字段"""

    def __init__(self, max_length: int = 255, min_length: int = 0, **kwargs):
        super().__init__(type_=str, **kwargs)
        self.max_length = max_length
        self.min_length = min_length


class IntegerField(Field):
    """整数字段"""

    def __init__(self, min_val: int = None, max_val: int = None, **kwargs):
        super().__init__(type_=int, **kwargs)
        self.min_val = min_val
        self.max_val = max_val


class EmailField(Field):
    """邮箱字段"""

    def __init__(self, **kwargs):
        super().__init__(type_=str, **kwargs)
        self.validators.append(self._validate_email)

    @staticmethod
    def _validate_email(value: str) -> str:
        """内置邮箱格式验证"""
        if "@" not in value or "." not in value:
            raise ValueError(f"无效的邮箱格式: {value}")
        return value


# ===== 使用示例 =====
class Article:
    """文章模型 — 声明式字段"""

    title = TextField(max_length=200, required=True)
    content = TextField(min_length=10, required=True)
    author = TextField(max_length=50, required=True)
    views = IntegerField(min_val=0, default=0)
    email = EmailField(required=True)

    def __init__(self, **kwargs):
        # TODO: 用字段描述符赋值
        pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== ORM 字段系统测试 ===")

    art = Article(title="Hello", content="x" * 20, author="alice", email="a@b.com")
    print(f"标题: {art.title}, 浏览: {art.views}")

    try:
        Article(title="", content="short", author="bob", email="bad")
    except (ValueError, TypeError) as e:
        print(f"验证失败: {e}")

    print("✅ Challenge 05 完成")
