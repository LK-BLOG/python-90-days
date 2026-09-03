from typing import Optional

class TokenCounter:
    """你的Token计数器实现"""

    def __init__(self, method: str = "approximate"):
        pass

    def count(self, text: str) -> int:
        pass

    def remaining(self, used: int, budget: int = 4096) -> int:
        pass

    def fits_budget(self, text: str, budget: int = 4096) -> bool:
        pass


if __name__ == "__main__":
    counter = TokenCounter("approximate")
    print(counter.count("测试文本"))
