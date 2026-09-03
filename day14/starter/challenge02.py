# Day 14 - Challenge 2: MRO 分析器
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 理解 C3 MRO，分析多继承调用顺序
# 参考 challenge.md

"""
MRO 分析器挑战 — 理解 C3 线性化算法

核心知识点:
- Python MRO (Method Resolution Order)
- super() 在多继承中的行为
- C3 线性化算法
"""


class A:
    def method(self):
        return "A"

    def who_am_i(self) -> str:
        return "I am A"


class B(A):
    def method(self):
        return "B -> " + super().method()

    def who_am_i(self) -> str:
        return "I am B (extends A)"


class C(A):
    def method(self):
        return "C -> " + super().method()

    def who_am_i(self) -> str:
        return "I am C (extends A)"


class D(B, C):
    """菱形继承: D -> B, C -> A"""
    def method(self):
        return "D -> " + super().method()


class E(C, B):
    """反向菱形: E -> C, B -> A"""
    def method(self):
        return "E -> " + super().method()


# ===== MRO 分析器 =====

def analyze_mro(cls) -> dict:
    """分析一个类的 MRO

    Args:
        cls: 要分析的类

    Returns:
        {
            "class": 类名,
            "mro_list": MRO 列表（类名字符串）,
            "mro_depth": MRO 深度,
            "direct_parents": 直接父类列表,
            "is_diamond": 是否存在菱形继承
        }
    """
    mro = cls.__mro__
    # TODO: 分析 MRO 列表，提取信息
    pass


def trace_method_call(cls, method_name: str) -> list[str]:
    """追踪方法调用链

    通过 MRO 顺序，模拟 super() 调用链。

    Args:
        cls: 要追踪的类
        method_name: 方法名

    Returns:
        调用顺序列表 ["D", "B", "C", "A"]

    Example:
        >>> trace_method_call(D, "method")
        ["D", "B", "C", "A"]
    """
    # TODO: 遍历 MRO，找到包含 method_name 的类
    # 注意: 第一个是 object，排除
    pass


def validate_mro_consistency(cls) -> list[str]:
    """验证 MRO 的一致性

    检查:
    1. 每个父类在 MRO 中只出现一次
    2. 子类在父类之前
    3. 如果多个父类有公共祖先，保持单调性

    Returns:
        违规信息列表（空 = 一致）
    """
    violations = []
    mro = cls.__mro__
    # TODO: 逐项检查
    return violations


# ---- 测试 ----
if __name__ == "__main__":
    print("=== MRO 分析器测试 ===")

    # D 的 MRO
    print(f"D.mro = {[c.__name__ for c in D.__mro__]}")
    print(f"D().method() = {D().method()}")

    # 分析
    for cls in [A, B, C, D, E]:
        info = analyze_mro(cls) or {}
        print(f"{cls.__name__}: mro={[c.__name__ for c in cls.__mro__]}")

    # 追踪调用链
    print(f"D 调用链: {trace_method_call(D, 'method')}")
    print(f"E 调用链: {trace_method_call(E, 'method')}")

    # 验证一致性
    for cls in [D, E]:
        violations = validate_mro_consistency(cls)
        print(f"{cls.__name__} 一致性: {'✅' if not violations else violations}")

    print("✅ Challenge 02 完成")
