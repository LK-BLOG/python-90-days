# Day 15 - Challenge 1: 温度转换器 (property)
# 难度: ⭐⭐⭐☆☆
#
# 要求: 用 property 实现智能温度属性
# 参考 challenge.md

"""
温度转换器挑战 — 用 @property 实现智能属性访问

核心知识点:
- @property / @x.setter / @x.deleter
- 属性访问控制
- 计算属性缓存
"""


class Temperature:
    """智能温度类 — 内部存摄氏度，支持华氏/开尔文访问

    Attributes:
        _celsius: 内部存储的摄氏温度
    """

    ABSOLUTE_ZERO_C = -273.15

    def __init__(self, celsius: float = 0.0):
        self._celsius = 0.0
        self.celsius = celsius  # 通过 property 设值（带验证）

    @property
    def celsius(self) -> float:
        """摄氏温度（property getter）"""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """设置摄氏温度（property setter，带验证）

        Raises:
            ValueError: 低于绝对零度
        """
        # TODO: 验证 >= ABSOLUTE_ZERO_C -> 赋值
        pass

    @property
    def fahrenheit(self) -> float:
        """华氏温度（计算属性）"""
        # TODO: return self._celsius * 9/5 + 32
        pass

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        """设置华氏温度（自动转摄氏度）"""
        # TODO: celsius = (value - 32) * 5/9 -> self.celsius = celsius
        pass

    @property
    def kelvin(self) -> float:
        """开尔文温度（计算属性）"""
        # TODO: return self._celsius + 273.15
        pass

    @kelvin.setter
    def kelvin(self, value: float) -> None:
        """设置开尔文温度"""
        # TODO: celsius = value - 273.15 -> self.celsius
        pass

    @property
    def is_freezing(self) -> bool:
        """只读属性：是否冰点以下"""
        return self._celsius < 0

    @property
    def is_boiling(self) -> bool:
        """只读属性：是否沸点以上"""
        return self._celsius >= 100

    @property
    def description(self) -> str:
        """只读描述"""
        status = "冰点下" if self.is_freezing else "沸点上" if self.is_boiling else "常温"
        return f"{self._celsius}°C ({status})"

    def __repr__(self) -> str:
        return f"Temperature({self._celsius}°C)"


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 温度转换器测试 ===")

    t = Temperature(36.5)
    print(f"摄氏: {t.celsius}°C")
    print(f"华氏: {t.fahrenheit}°F")
    print(f"开尔文: {t.kelvin}K")
    print(f"描述: {t.description}")

    t.fahrenheit = 212
    print(f"\n设华氏 212 -> 摄氏: {t.celsius}°C")

    t.kelvin = 0
    print(f"设开尔文 0 -> 摄氏: {t.celsius}°C (绝对零度)")

    print(f"冰点: {t.is_freezing}, 沸点: {t.is_boiling}")

    try:
        t.celsius = -300  # 超过绝对零度
    except ValueError as e:
        print(f"错误: {e}")

    print("✅ Challenge 01 完成")
