# Day 13 - Challenge 2: 方法类型大练习
# 难度: ⭐⭐⭐☆☆
#
# 要求: 实例方法、类方法、静态方法的综合运用
# 参考 challenge.md

"""
方法类型挑战 — 熟练使用三种方法类型

- 实例方法: 操作实例数据，第一个参数是 self
- 类方法: 操作类本身，第一个参数是 cls
- 静态方法: 与类相关但不依赖类/实例数据
"""

import re


class Temperature:
    """温度类 — 三种方法的综合练习

    属性:
        celsius: 摄氏温度
    """

    ABSOLUTE_ZERO = -273.15  # 绝对零度

    def __init__(self, celsius: float):
        """初始化温度

        Args:
            celsius: 摄氏温度

        Raises:
            ValueError: 低于绝对零度
        """
        # TODO: 检查绝对零度限制 -> 设置 celsius
        pass

    # ===== 实例方法 =====

    def to_fahrenheit(self) -> float:
        """摄氏转华氏

        公式: F = C * 9/5 + 32

        Returns:
            华氏温度
        """
        # TODO: 实现转换公式
        pass

    def to_kelvin(self) -> float:
        """摄氏转开尔文

        公式: K = C + 273.15
        """
        # TODO: 实现转换公式
        pass

    def is_freezing(self) -> bool:
        """是否低于冰点 (0°C)"""
        # TODO: return self.celsius < 0
        pass

    # ===== 类方法 =====

    @classmethod
    def from_fahrenheit(cls, fahrenheit: float) -> "Temperature":
        """从华氏温度创建实例

        Args:
            fahrenheit: 华氏温度

        Returns:
            Temperature 实例
        """
        # TODO: celsius = (f - 32) * 5/9 -> cls(celsius)
        pass

    @classmethod
    def from_string(cls, s: str) -> "Temperature":
        """从字符串创建实例

        支持格式: "36.5C" 或 "97.7F"

        Args:
            s: 温度字符串

        Raises:
            ValueError: 格式不正确

        Example:
            >>> t = Temperature.from_string("0C")
            >>> t.celsius
            0.0
        """
        # TODO: 用正则或字符串操作解析数字和单位
        # 根据 C/F 分别处理
        pass

    @classmethod
    def average(cls, *temps: "Temperature") -> "Temperature":
        """计算多个温度的平均值（类方法）"""
        # TODO: 计算平均摄氏温度，返回新实例
        pass

    # ===== 静态方法 =====

    @staticmethod
    def is_freezing_celsius(celsius: float) -> bool:
        """判断是否冰点以下（静态方法版）

        Args:
            celsius: 摄氏温度
        """
        # TODO: return celsius < 0
        pass

    @staticmethod
    def convert_formula(celsius: float) -> str:
        """返回转换公式的描述字符串"""
        # TODO: return f"{celsius}°C = {celsius*9/5+32}°F = {celsius+273.15}K"
        pass

    def __repr__(self) -> str:
        return f"Temperature({self.celsius}°C)"


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 方法类型测试 ===")

    t1 = Temperature(36.5)
    print(f"t1 = {t1}")
    print(f"转华氏: {t1.to_fahrenheit()}")  # 97.7
    print(f"转开尔文: {t1.to_kelvin()}")

    t2 = Temperature.from_fahrenheit(97.7)
    print(f"从华氏创建: {t2}")  # Temperature(36.5°C)

    t3 = Temperature.from_string("0C")
    print(f"从字符串创建: {t3}")
    print(f"是否冰点: {Temperature.is_freezing_celsius(t3.celsius)}")  # True

    avg = Temperature.average(t1, t2, t3)
    print(f"平均温度: {avg}")

    print("✅ Challenge 02 完成")
