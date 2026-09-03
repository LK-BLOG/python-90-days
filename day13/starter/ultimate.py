# Day 13 - Ultimate: 类机制终极挑战
# 难度: ⭐⭐⭐⭐⭐
#
# 要求: 综合运用类属性、描述符、单例、Mixin 设计一个 ORM 框架核心
# 参考 ultimate_challenge.md

"""
ORM 框架核心终极挑战 — 迷你版 SQLAlchemy ORM

核心功能:
- 声明式字段定义（描述符）
- 模型基类
- 自动表名生成
- 实例创建和查询模拟
"""

from datetime import datetime


# ===== 字段描述符 =====

class Field:
    """ORM 字段基类 — 描述符实现"""

    _creation_counter = 0  # 记录字段声明顺序

    def __init__(self, column_type: str = "TEXT", primary_key: bool = False,
                 default=None, nullable: bool = True):
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
        self.nullable = nullable
        self.name = None
        self._creation_counter = Field._creation_counter
        Field._creation_counter += 1

    def __set_name__(self, owner, name):
        # TODO: 设置 self.name
        pass

    def __get__(self, obj, objtype=None):
        # TODO: 返回实例值或默认值
        pass

    def __set__(self, obj, value):
        # TODO: nullable 检查 -> 存入实例 __dict__
        pass


class IntegerField(Field):
    """整数字段"""

    def __init__(self, **kwargs):
        super().__init__(column_type="INTEGER", **kwargs)

    def __set__(self, obj, value):
        # TODO: 类型检查 (int) -> 调用父类 __set__
        pass


class StringField(Field):
    """字符串字段"""

    def __init__(self, max_length: int = 255, **kwargs):
        super().__init__(column_type=f"VARCHAR({max_length})", **kwargs)
        self.max_length = max_length


class DateTimeField(Field):
    """日期时间字段"""

    def __init__(self, auto_now: bool = False, **kwargs):
        super().__init__(column_type="DATETIME", **kwargs)
        self.auto_now = auto_now


# ===== 模型基类 =====

class ModelMeta(type):
    """模型元类 — 自动收集字段、生成表名"""

    def __new__(mcs, name, bases, namespace):
        # TODO:
        # 1. 收集所有 Field 实例 -> _fields 字典
        # 2. 如果没有指定表名，自动生成 (类名小写 + 's')
        # 3. 添加 _columns 列表（按声明顺序）
        pass


class Model(metaclass=ModelMeta):
    """ORM 模型基类"""

    id = IntegerField(primary_key=True)

    def __init__(self, **kwargs):
        """用关键字参数初始化字段"""
        # TODO: 遍历 _fields，从 kwargs 或 default 取值
        pass

    def save(self) -> dict:
        """模拟保存到数据库

        Returns:
            要插入的数据字典
        """
        # TODO: 返回 {field_name: value, ...}
        pass

    def __repr__(self) -> str:
        # TODO: 返回 TableName(id=1, name='Alice')
        pass


# ===== 用户模型示例 =====
class User(Model):
    """用户模型"""

    name = StringField(max_length=100, nullable=False)
    email = StringField(max_length=255, nullable=False)
    age = IntegerField(default=0)
    created_at = DateTimeField(auto_now=True)


# ---- 测试 ----
if __name__ == "__main__":
    print("=== ORM 框架终极挑战 ===")

    u = User(name="Alice", email="alice@test.com", age=25)
    print(u)
    print(f"表名: {User._tablename if hasattr(User, '_tablename') else '(未实现)'}")
    print(f"保存: {u.save()}")

    print("✅ Ultimate 完成")
