"""TDD 红绿重构演示"""

# === Step 1: Red - 写测试（函数不存在）===
# 运行测试 → 失败（NameError）

# === Step 2: Green - 写最少代码让测试通过 ===
class Calculator:
    """简易计算器 - TDD 产物"""

    def __init__(self):
        self.history = []

    def add(self, a: float, b: float) -> float:
        result = a + b
        self.history.append(('add', a, b, result))
        return result

    def subtract(self, a: float, b: float) -> float:
        result = a - b
        self.history.append(('subtract', a, b, result))
        return result

    def multiply(self, a: float, b: float) -> float:
        result = a * b
        self.history.append(('multiply', a, b, result))
        return result

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("除数不能为零")
        result = a / b
        self.history.append(('divide', a, b, result))
        return result

    def get_last_result(self) -> float:
        if not self.history:
            raise IndexError("没有计算历史")
        return self.history[-1][3]

    def clear_history(self):
        self.history.clear()


# === Step 3: Refactor - 重构 ===
# Calculator 类已经很简洁，暂时不需要重构

# === 对应的 pytest 测试 ===
# test_calculator.py 内容:
"""
import pytest
from tdd_demo import Calculator

@pytest.fixture
def calc():
    return Calculator()

class TestAdd:
    def test_positive(self, calc):
        assert calc.add(1, 2) == 3

    def test_negative(self, calc):
        assert calc.add(-1, -2) == -3

    def test_zero(self, calc):
        assert calc.add(0, 0) == 0

class TestDivide:
    def test_normal(self, calc):
        assert calc.divide(10, 2) == 5.0

    def test_by_zero(self, calc):
        with pytest.raises(ValueError):
            calc.divide(1, 0)

    def test_float(self, calc):
        assert calc.divide(1, 3) == pytest.approx(0.333, rel=1e-2)

class TestHistory:
    def test_history_recorded(self, calc):
        calc.add(1, 2)
        calc.multiply(3, 4)
        assert len(calc.history) == 2

    def test_clear_history(self, calc):
        calc.add(1, 2)
        calc.clear_history()
        assert len(calc.history) == 0

    def test_empty_history_error(self, calc):
        with pytest.raises(IndexError):
            calc.get_last_result()
"""

if __name__ == "__main__":
    calc = Calculator()
    print(f"2 + 3 = {calc.add(2, 3)}")
    print(f"10 / 3 = {calc.divide(10, 3):.4f}")
    print(f"Last: {calc.get_last_result()}")
