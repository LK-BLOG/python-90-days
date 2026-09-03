# Day 14 - Challenge 5: 钻石继承调试
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 理解并解决钻石继承问题
# 参考 challenge.md

"""
钻石继承调试挑战 — 深入理解 Python 的菱形继承处理

经典问题:
    A
   / \
  B   C
   \ /
    D

B 和 C 都继承 A，D 同时继承 B 和 C。
调用 super() 时如何避免重复调用 A.__init__?
"""


class Base:
    """基类 A"""

    _init_order = []  # 类变量追踪初始化顺序

    def __init__(self, name: str = "Base"):
        # TODO: 设置 name，记录到 _init_order
        pass

    def who(self) -> str:
        # TODO: 返回 name
        pass


class Left(Base):
    """左侧 B"""

    def __init__(self, name: str = "Left", left_val: int = 0):
        # TODO: 调用 super().__init__
        # 设置 left_val
        pass

    def method_left(self) -> str:
        return f"Left({self.left_val})"


class Right(Base):
    """右侧 C"""

    def __init__(self, name: str = "Right", right_val: str = ""):
        # TODO: 调用 super().__init__
        # 设置 right_val
        pass

    def method_right(self) -> str:
        return f"Right({self.right_val})"


class Diamond(Left, Right):
    """菱形 D

    MRO 应该是: Diamond -> Left -> Right -> Base -> object
    super() 会按 MRO 顺序调用，每个类只被调用一次。
    """

    def __init__(self, name: str = "Diamond",
                 left_val: int = 0, right_val: str = ""):
        # TODO:
        # 1. 调用 super().__init__ (不要直接调用 Left/Right)
        # 2. super() 会自动按 MRO 调用 Left -> Right -> Base
        # 3. 设置自己的属性
        pass

    def full_info(self) -> str:
        """返回完整信息"""
        return (f"Diamond(name={self.name}, left={self.left_val}, "
                f"right={self.right_val})")


# ===== 调试工具 =====

def trace_init(cls, *args, **kwargs) -> list[str]:
    """追踪 __init__ 调用链

    Args:
        cls: 要实例化的类
        *args, **kwargs: 构造参数

    Returns:
        初始化顺序列表 ["Diamond.__init__", "Left.__init__", ...]
    """
    Base._init_order.clear()
    obj = cls(*args, **kwargs)
    return Base._init_order.copy()


def verify_mro() -> bool:
    """验证所有类的 MRO 是否正确

    Returns:
        MRO 是否一致
    """
    expected = ["Diamond", "Left", "Right", "Base"]
    actual = [c.__name__ for c in Diamond.__mro__ if c.__name__ != "object"]
    # TODO: 比较 expected 和 actual
    pass


def check_single_init(obj, cls) -> bool:
    """检查基类 __init__ 只被调用了一次"""
    # TODO: 用 trace_init 实例化，检查 Base 出现次数
    pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 钻石继承调试测试 ===")

    d = Diamond("MyDiamond", left_val=42, right_val="hello")
    print(d.full_info())
    print(f"MRO: {[c.__name__ for c in Diamond.__mro__]}")

    # 追踪初始化顺序
    trace = trace_init(Diamond, "Trace", 99, "world")
    print(f"初始化顺序: {trace}")

    # 验证
    print(f"MRO 验证: {'✅' if verify_mro() else '❌'}")

    print("✅ Challenge 05 完成")
