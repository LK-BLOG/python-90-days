# Day 12 - Challenge 3: 包测试
# 难度: ⭐⭐⭐☆☆
#
# 要求: 为包编写单元测试，配置测试环境
# 参考 challenge.md

"""
包测试挑战 — 为自己的包编写全面的测试

核心知识点:
- pytest 的使用
- 测试夹具 (fixtures)
- 参数化测试
- 测试覆盖率
"""

import pytest
import os
import tempfile


# ===== 被测代码 =====

class Calculator:
    """简易计算器类

    Attributes:
        history: 运算历史记录
    """

    def __init__(self):
        self.history: list[dict] = []

    def add(self, a: float, b: float) -> float:
        """加法"""
        # TODO: 计算结果，记录到 history，返回结果
        pass

    def subtract(self, a: float, b: float) -> float:
        """减法"""
        # TODO: 类似 add
        pass

    def multiply(self, a: float, b: float) -> float:
        """乘法"""
        # TODO: 类似 add
        pass

    def divide(self, a: float, b: float) -> float:
        """除法

        Raises:
            ZeroDivisionError: 除数为 0 时抛出
        """
        # TODO: 检查除数 -> 计算 -> 记录 -> 返回
        pass

    def clear_history(self) -> None:
        """清空历史"""
        self.history.clear()


# ===== 测试用例 =====

class TestCalculator:
    """计算器测试套件"""

    def setup_method(self):
        """每个测试方法前执行"""
        # TODO: 创建新的 Calculator 实例
        pass

    def test_add(self):
        """测试加法"""
        # TODO: assert cal.add(2, 3) == 5
        pass

    def test_subtract(self):
        """测试减法"""
        # TODO: assert cal.subtract(10, 3) == 7
        pass

    def test_multiply(self):
        """测试乘法"""
        # TODO: assert cal.multiply(4, 5) == 20
        pass

    def test_divide(self):
        """测试除法"""
        # TODO: assert cal.divide(10, 3) == pytest.approx(3.333)
        pass

    def test_divide_by_zero(self):
        """测试除以零"""
        # TODO: with pytest.raises(ZeroDivisionError):
        #       cal.divide(1, 0)
        pass

    def test_history_recorded(self):
        """测试历史记录"""
        # TODO: 执行多次运算，检查 history 长度和内容
        pass

    def test_clear_history(self):
        """测试清空历史"""
        # TODO: 运算后清空，检查 history 为空
        pass


# ===== 参数化测试 =====

@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add_parametrized(a, b, expected):
    """参数化加法测试"""
    # TODO: 创建计算器，验证 add(a, b) == expected
    pass


# ===== Fixture 测试 =====

@pytest.fixture
def temp_file():
    """创建临时文件的 fixture"""
    # TODO: 创建临时文件，yield 路径，测试后清理
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("test content\n")
        path = f.name
    yield path
    os.unlink(path)


def test_file_operations(temp_file):
    """测试文件操作（使用 fixture）"""
    # TODO: 读取 temp_file，验证内容
    pass


# ---- 主入口 ----
if __name__ == "__main__":
    print("=== 包测试挑战 ===")
    print("运行: pytest challenge03.py -v")
    pytest.main([__file__, "-v"])
