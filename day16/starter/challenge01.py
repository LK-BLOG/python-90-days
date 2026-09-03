# Day 16 - Challenge 1: 美观输出
# 难度: ⭐⭐⭐☆☆
#
# 要求: 实现 __repr__, __str__, __format__
# 参考 challenge.md

"""
美观输出挑战 — 让你的对象打印出来更专业

核心知识点:
- __repr__: 开发者友好，用于调试
- __str__: 用户友好，用于 print()
- __format__: 支持 format() 和 f-string 格式化
"""

from datetime import datetime


class Color:
    """颜色类 — 丰富的字符串表示"""

    # 颜色名称 -> RGB 映射
    PRESETS = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "white": (255, 255, 255),
        "black": (0, 0, 0),
    }

    def __init__(self, r: int, g: int, b: int, name: str = ""):
        # TODO: 验证 RGB 范围 0-255，设置属性
        self.r = r
        self.g = g
        self.b = b
        self.name = name or f"#{r:02x}{g:02x}{b:02x}"

    @classmethod
    def from_name(cls, name: str) -> "Color":
        """从颜色名称创建"""
        # TODO: 从 PRESETS 查找
        pass

    def __repr__(self) -> str:
        """开发者友好的表示

        Example:
            Color(r=255, g=0, b=0, name='red')
        """
        # TODO: 返回可重新创建对象的字符串
        pass

    def __str__(self) -> str:
        """用户友好的表示

        Example:
            red (255, 0, 0)
        """
        # TODO: 返回 "name (r, g, b)"
        pass

    def __format__(self, format_spec: str) -> str:
        """支持多种格式化

        格式说明:
            "hex"   -> "#ff0000"
            "rgb"   -> "rgb(255, 0, 0)"
            "hsl"   -> "hsl(0, 100%, 50%)"
            ""      -> 默认使用 __str__
            "css"   -> "red" (如果名称已知)
        """
        if format_spec == "hex":
            # TODO: 返回十六进制
            pass
        elif format_spec == "rgb":
            # TODO: 返回 rgb() 格式
            pass
        elif format_spec == "hsl":
            # TODO: 转换为 HSL
            pass
        elif format_spec == "css":
            # TODO: 如果是预设色则返回名称
            pass
        else:
            return str(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Color):
            return NotImplemented
        return (self.r, self.g, self.b) == (other.r, other.g, other.b)

    def __hash__(self) -> int:
        return hash((self.r, self.g, self.b))


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 美观输出测试 ===")

    red = Color(255, 0, 0, "red")
    print(f"repr: {repr(red)}")
    print(f"str:  {str(red)}")
    print(f"hex:  {red:hex}")
    print(f"rgb:  {red:rgb}")
    print(f"hsl:  {red:hsl}")

    custom = Color(128, 64, 200)
    print(f"custom: {custom}")
    print(f"custom hex: {custom:hex}")

    print("✅ Challenge 01 完成")
