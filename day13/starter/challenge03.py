# Day 13 - Challenge 3: 描述符验证
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 用描述符实现通用属性验证
# 参考 challenge.md

"""
描述符验证挑战 — 用描述符 (Descriptor) 实现声明式属性验证

核心知识点:
- 描述符协议: __get__, __set__, __delete__
- __set_name__: 自动获取属性名
- 数据描述符 vs 非数据描述符
"""


class ValidatedField:
    """通用验证描述符

    在类级别声明，在实例级别验证和存储。

    Attributes:
        min_value: 最小值约束
        max_value: 最大值约束
        required: 是否必填
        type_check: 类型检查（None 表示不检查）
        default: 默认值
    """

    def __init__(self, min_value=None, max_value=None,
                 required=False, type_check=None, default=None):
        # TODO: 初始化验证参数
        self.min_value = min_value
        self.max_value = max_value
        self.required = required
        self.type_check = type_check
        self.default = default

    def __set_name__(self, owner, name):
        """自动获取属性名（Python 3.6+）

        Args:
            owner: 所属类
            name: 属性名
        """
        # TODO: 设置 self.name = name
        # 提示: 用一个存储属性名，如 f"_validated_{name}"
        pass

    def __get__(self, obj, objtype=None):
        """获取属性值

        Args:
            obj: 实例（为 None 时返回描述符本身）
            objtype: 所属类
        """
        # TODO: obj 为 None 返回 self，否则从实例 __dict__ 取值
        pass

    def __set__(self, obj, value):
        """设置属性值（带验证）

        Args:
            obj: 实例
            value: 新值

        Raises:
            ValueError: 验证失败时抛出
            TypeError: 类型不匹配时抛出
        """
        # TODO: 依次检查:
        # 1. required 和 value is None
        # 2. type_check
        # 3. min_value / max_value
        # 4. 通过则存入 obj.__dict__
        pass

    def _validate(self, value):
        """执行验证逻辑"""
        if value is None and self.required:
            raise ValueError(f"{self.name} is required")
        if value is not None and self.type_check is not None:
            if not isinstance(value, self.type_check):
                raise TypeError(
                    f"{self.name} must be {self.type_check.__name__}, "
                    f"got {type(value).__name__}"
                )
        if value is not None and self.min_value is not None:
            if value < self.min_value:
                raise ValueError(f"{self.name} must be >= {self.min_value}")
        if value is not None and self.max_value is not None:
            if value > self.max_value:
                raise ValueError(f"{self.name} must be <= {self.max_value}")


class Product:
    """商品类 — 使用描述符验证"""

    name = ValidatedField(required=True, type_check=str)
    price = ValidatedField(min_value=0.01, type_check=float)
    stock = ValidatedField(min_value=0, type_check=int, default=0)
    description = ValidatedField(type_check=str, default="")

    def __init__(self, name: str, price: float, stock: int = 0, description: str = ""):
        # TODO: 直接赋值，验证由描述符自动处理
        pass

    def __repr__(self) -> str:
        return f"Product(name={self.name!r}, price={self.price}, stock={self.stock})"

    def is_available(self) -> bool:
        """是否有库存"""
        return self.stock > 0


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 描述符验证测试 ===")

    p = Product("iPhone", 999.99, 100)
    print(p)

    # 正常赋值
    p.stock = 50
    print(f"更新库存: {p.stock}")

    # 验证失败
    try:
        Product("", 999.99, 100)  # name required
    except ValueError as e:
        print(f"验证失败: {e}")

    try:
        Product("iPhone", -1, 100)  # price < 0.01
    except ValueError as e:
        print(f"验证失败: {e}")

    try:
        Product("iPhone", 999.99, "很多")  # stock 类型错误
    except TypeError as e:
        print(f"类型错误: {e}")

    print("✅ Challenge 03 完成")
