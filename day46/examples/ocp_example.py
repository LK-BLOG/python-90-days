\"\"\"开闭原则示例 — 策略模式\"\"\"

from abc import ABC, abstractmethod


# ===== 违反OCP =====
class DiscountCalculatorBad:
    \"\"\"反模式：每加一种类型就要改代码\"\"\"

    def calculate(self, customer_type: str, amount: float) -> float:
        if customer_type == \"regular\":
            return amount * 0.9
        elif customer_type == \"premium\":
            return amount * 0.8
        elif customer_type == \"vip\":
            return amount * 0.7
        else:
            raise ValueError(f\"Unknown type: {customer_type}\")


# ===== 遵循OCP =====
class DiscountStrategy(ABC):
    \"\"\"折扣策略抽象\"\"\"

    @abstractmethod
    def get_discount(self) -> float:
        \"\"\"返回折扣比例（0-1）\"\"\"
        ...

    def apply(self, amount: float) -> float:
        return amount * (1 - self.get_discount())


class RegularDiscount(DiscountStrategy):
    def get_discount(self) -> float:
        return 0.1


class PremiumDiscount(DiscountStrategy):
    def get_discount(self) -> float:
        return 0.2


class VipDiscount(DiscountStrategy):
    def get_discount(self) -> float:
        return 0.3


class SeasonalDiscount(DiscountStrategy):
    \"\"\"新增类型不需要修改任何已有代码\"\"\"

    def __init__(self, extra: float = 0.05):
        self.extra = extra

    def get_discount(self) -> float:
        return 0.1 + self.extra


class DiscountCalculator:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def calculate(self, amount: float) -> float:
        return self.strategy.apply(amount)


# 使用示例
if __name__ == \"__main__\":
    for name, strategy in [
        (\"Regular\", RegularDiscount()),
        (\"Premium\", PremiumDiscount()),
        (\"VIP\", VipDiscount()),
        (\"Seasonal\", SeasonalDiscount(0.1)),
    ]:
        calc = DiscountCalculator(strategy)
        result = calc.calculate(1000)
        print(f\"{name}: {result:.2f}\")
